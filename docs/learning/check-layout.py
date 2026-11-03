"""레슨 HTML의 배치 문제를 DOM 숫자로 검사한다. 스크린샷 없이 텍스트로 결과를 낸다.

사용: python check-layout.py <lesson.html>
결과: 위반마다 한 줄 `모드 | 절 [> N단계] | 검사 | 요소 | 측정값`. 위반이 없으면 `OK`.

검사 (라이트 1000px, 다크 500px):
- page-scroll: 페이지 가로 스크롤
- overflow: 1000px의 pre·td·th·p·li·figure, 500px의 td·th·p·li·figure에서 내용이 칸을 넘친다 (500px pre의 가로 스크롤은 허용). img·svg는 부모의 오른쪽 끝을 넘는지로 잰다
- code-break: 표 칸 안 코드가 두 줄 이상으로 끊긴다
- overlap: 글자를 가진 두 요소(서로 포함 관계 아님)의 영역이 가로·세로 모두 1px를 넘게 겹친다
- clip-y: overflow-y가 visible이 아닌 요소의 내용이 세로로 잘린다
- contrast: 글자색과 글자 밑 배경색의 WCAG 대비가 기준(4.5:1, 큰 글자 3:1)에 못 미친다. ::before·::after의 문자열 content도 잰다. 같은 색 조합은 한 줄로 묶고 요소 칸 끝에 ` 외 N개`를 붙인다

측정값 칸의 예: `1200 > 984px`, `겹침 WxHpx`, `4.48:1 < 4.5:1`.
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MODES = {
    "light-1000": (["--window-size=1000,2000"], "pre, td, th, p, li, figure"),
    "dark-500": (["--window-size=500,2400", "--force-dark-mode",
                  "--blink-settings=preferredColorScheme=0"], "td, th, p, li, figure"),
}
# load 뒤 결과를 <pre id="layout-result">에 써 두면 --dump-dom이 그 DOM을 내보낸다
JS = """<script>
addEventListener('load', () => {
  const heads = [...document.querySelectorAll('h2, h3')];
  const where = el => {
    const h = heads.filter(h => h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING).pop();
    const li = el.closest('ol.steps > li');
    const step = li ? ' > ' + (li.parentNode.start + [...li.parentNode.children].indexOf(li)) + '단계' : '';
    return (h ? h.textContent.trim() : '(머리)') + step;
  };
  const name = el => el.tagName.toLowerCase() + ' "' + el.textContent.trim().replace(/\\s+/g, ' ').slice(0, 40) + '"';
  const out = [];
  const d = document.documentElement;
  if (d.scrollWidth > innerWidth) out.push('(페이지) | page-scroll | html | ' + d.scrollWidth + ' > ' + innerWidth + 'px');
  for (const el of document.querySelectorAll(__OVERFLOW__))
    if (el.scrollWidth > el.clientWidth) out.push(where(el) + ' | overflow | ' + name(el) + ' | ' + el.scrollWidth + ' > ' + el.clientWidth + 'px');
  // img·svg는 scrollWidth를 믿을 수 없어 부모의 오른쪽 끝과 비교한다
  for (const el of document.querySelectorAll('img, svg')) {
    const right = el.getBoundingClientRect().right, pr = el.parentElement.getBoundingClientRect().right;
    if (right > pr + 1) out.push(where(el) + ' | overflow | ' + name(el) + ' | ' + Math.round(right) + ' > ' + Math.round(pr) + 'px');
  }
  // 키 칸·헤더의 코드는 끊기면 안 된다. 다른 칸은 한 줄로 칸에 들어가는데도 끊겼을 때만 잡는다
  for (const el of document.querySelectorAll('td code, th code')) {
    const rects = [...el.getClientRects()];
    if (rects.length < 2) continue;
    const cell = el.closest('td, th'), cs = getComputedStyle(cell);
    const room = cell.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const width = rects.reduce((s, r) => s + r.width, 0);
    if (cell.matches('th, td:first-child') || width <= room)
      out.push(where(el) + ' | code-break | ' + name(el) + ' | ' + Math.round(width) + '/' + Math.round(room) + 'px');
  }
  // 글자를 직접 가진 보이는 요소와 SVG text
  const texts = [...document.querySelectorAll('body *')].filter(el => {
    if (el.closest('script, style, noscript') || getComputedStyle(el).visibility === 'hidden') return false;
    const r = el.getClientRects()[0];
    if (!r || !r.width || !r.height) return false;
    return el instanceof SVGElement ? el.localName === 'text'
      : [...el.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim());
  });
  // ponytail: O(n^2) 쌍 비교. 글자 요소가 수천 개를 넘어 느려지면 격자 버킷으로 후보를 줄인다
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    if (a.contains(b) || b.contains(a)) continue;
    let best = null;
    for (const p of a.getClientRects()) for (const q of b.getClientRects()) {
      const w = Math.min(p.right, q.right) - Math.max(p.left, q.left), h = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (w > 1 && h > 1 && (!best || w * h > best.w * best.h)) best = {w, h};
    }
    if (best) out.push(where(a) + ' | overlap | ' + name(a) + ' ↔ ' + name(b) + ' | 겹침 ' + Math.round(best.w) + 'x' + Math.round(best.h) + 'px');
  }
  for (const el of document.querySelectorAll('body *'))
    if (getComputedStyle(el).overflowY !== 'visible' && el.scrollHeight - el.clientHeight > 1)
      out.push(where(el) + ' | clip-y | ' + name(el) + ' | ' + el.scrollHeight + ' > ' + el.clientHeight + 'px');
  const parse = s => {
    const m = s.match(/^rgba?\\(([^)]+)\\)$/);
    if (!m) return null;
    const v = m[1].split(/[\\s,\\/]+/).map(parseFloat);
    return {r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1};
  };
  const mix = (c, base) => ({r: c.a * c.r + (1 - c.a) * base.r, g: c.a * c.g + (1 - c.a) * base.g, b: c.a * c.b + (1 - c.a) * base.b, a: 1});
  const lum = c => [c.r, c.g, c.b].map(v => (v /= 255) <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)
    .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
  const groups = new Map();
  const SHAPES = ['rect', 'circle', 'ellipse', 'path', 'polygon', 'polyline'];
  // ::before·::after는 문자열 content가 있을 때만 대상이다. 배경은 호스트 요소에서 구한다
  const items = texts.map(el => [el, '']);
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getClientRects()[0];
    if (el instanceof SVGElement || el.closest('script, style, noscript') || !r || !r.width || !r.height) continue;
    for (const ps of ['::before', '::after']) {
      const c = getComputedStyle(el, ps).content;
      if (c.startsWith('"') && c.length > 2) items.push([el, ps]);
    }
  }
  for (const [el, ps] of items) {
    el.scrollIntoView({block: 'center'});
    const svg = el instanceof SVGElement, cs = getComputedStyle(el, ps || null), fgRaw = svg ? cs.fill : cs.color;
    if (fgRaw === 'none') continue;
    const r = el.getClientRects()[0];
    // 글자 시작 쪽 점을 잰다 (잘림 컨테이너 안에 남도록). 화면 밖이면 화면 안으로 당긴다
    const x = Math.max(0, Math.min(r.left + Math.min(r.width / 2, 20), innerWidth - 1)), y = Math.max(0, Math.min(r.top + r.height / 2, innerHeight - 1));
    const list = document.elementsFromPoint(x, y);
    let bad = null, base = {r: 255, g: 255, b: 255, a: 1};  // ponytail: 배경 이미지·그라디언트는 무시하고 흰색으로 본다
    const stack = [];
    for (const e of list.slice(Math.max(list.indexOf(el), 0))) {
      const shape = e instanceof SVGElement && e.localName !== 'svg';
      if (shape && !SHAPES.includes(e.localName)) continue;
      const v = getComputedStyle(e)[shape ? 'fill' : 'backgroundColor'], c = parse(v);
      if (!c) { if (v !== 'none') bad = v; if (bad) break; continue; }
      if (c.a === 0) continue;
      if (c.a >= 1) { base = c; break; }
      stack.push(c);
    }
    const fg = parse(fgRaw);
    let measure;
    if (bad || !fg) measure = '색 해석 불가: ' + (fg ? bad : fgRaw);
    else {
      for (const c of stack.reverse()) base = mix(c, base);
      const f = mix(fg, base), l1 = lum(f), l2 = lum(base);
      const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      const px = parseFloat(cs.fontSize), big = px >= 24 || (px >= 18.66 && parseInt(cs.fontWeight) >= 700), min = big ? 3 : 4.5;
      if (ratio >= min) continue;
      measure = ratio.toFixed(2) + ':1 < ' + min + ':1';
    }
    const key = fgRaw + '|' + [base.r, base.g, base.b].map(Math.round) + '|' + measure;
    if (groups.has(key)) groups.get(key).n++;
    else groups.set(key, {n: 0, measure, line: where(el) + ' | contrast | ' + (ps ? el.tagName.toLowerCase() + ps + ' "' + cs.content.slice(1, -1) + '"' : name(el))});
  }
  for (const g of groups.values()) out.push(g.line + (g.n ? ' 외 ' + g.n + '개' : '') + ' | ' + g.measure);
  const pre = document.createElement('pre');
  pre.id = 'layout-result';
  pre.textContent = out.join('\\n');
  document.body.append(pre);
});
</script>"""


def main(lesson):
    sys.stdout.reconfigure(encoding="utf-8")
    lesson = pathlib.Path(lesson).resolve()
    page = lesson.read_text(encoding="utf-8")
    # 사본은 다른 폴더에 쓰므로 상대 경로 stylesheet를 절대 file URL로 바꾼다
    css = (lesson.parent / "../assets/style.css").resolve().as_uri()
    page = page.replace('href="../assets/style.css"', f'href="{css}"')
    lines = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        for mode, (flags, overflow) in MODES.items():
            copy = pathlib.Path(tmp) / f"{mode}.html"
            copy.write_text(page.replace("</body>", JS.replace("__OVERFLOW__", repr(overflow)) + "</body>"),
                            encoding="utf-8")
            # 실행마다 프로필을 따로 줘야 연속 실행이 앞 실행에 넘어가지 않는다
            dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                                  f"--user-data-dir={tmp}/profile-{mode}", *flags,
                                  "--dump-dom", copy.as_uri()],
                                 capture_output=True, encoding="utf-8", timeout=60).stdout
            m = re.search(r'<pre id="layout-result">(.*?)</pre>', dom, re.S)
            if not m:
                sys.exit(f"{mode}: 검사 결과를 받지 못했다 (Chrome 출력 {len(dom)}자)")
            lines += [f"{mode} | {l}" for l in html.unescape(m.group(1)).splitlines()]
    print("\n".join(lines) or "OK")


if __name__ == "__main__":
    main(sys.argv[1])
