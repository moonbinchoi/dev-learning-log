"""레슨 HTML을 h2·h3 절마다 잘라 headless Chrome으로 찍는다.

사용: python render-sections.py <lesson.html> <out_dir> [절 번호 ...]
결과: <out_dir>/<번호>-light.png (1000px), <번호>-dark.png (500px). 절마다 `번호 제목` 한 줄을 출력한다.
절 번호를 주면 그 절만 찍는다. 00은 첫 제목 앞(제목·부제)이다.

한 장으로 긴 페이지를 찍으면 축소돼 표 안 글자를 볼 수 없어서 절마다 따로 찍는다.
"""
import os
import pathlib
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MODES = {
    "light": ["--window-size=1000,2000"],
    "dark": ["--window-size=500,2400", "--force-dark-mode",
             "--blink-settings=preferredColorScheme=0"],
}
# 절 높이를 이미지가 로드된 뒤 DOM에 적어 둔다(--dump-dom으로 읽는다). 본문 안(</main> 바로 뒤)에 넣는다
MEASURE = ("<script>addEventListener('load', () => "
           "document.documentElement.dataset.h = document.documentElement.scrollHeight)</script>")
# 이 Chrome에서 80000px 창도 그대로 찍혔다(2017년 16384 보고는 해당 없음). 그 이상은 검증하지 않았다
MAX_HEIGHT = 80000


def add_base(html, lesson_dir):
    # 잘라 낸 파일은 out_dir에 놓이므로 <base>로 stylesheet·이미지의 상대 경로를 레슨 폴더 기준으로 푼다
    # check-layout.py와 같은 규칙: 첫 <head ...> 바로 뒤, 없으면 문서 맨 앞
    base = f'<base href="{pathlib.Path(lesson_dir).as_uri()}/">'
    html, n = re.subn(r"<head(?:\s[^>]*)?>", lambda m: m.group(0) + base, html, count=1, flags=re.I)
    return html if n else base + html


def main(lesson, out, *only):
    sys.stdout.reconfigure(encoding="utf-8")
    lesson, out = pathlib.Path(lesson).resolve(), pathlib.Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    html = add_base(lesson.read_text(encoding="utf-8"), lesson.parent)
    head, rest = html.split("<main>", 1)
    body, tail = rest.split("</main>", 1)
    sections = re.split(r"(?=<h[23][ >])", body)
    jobs = []
    for i, sec in enumerate(sections):
        h = re.match(r"<h[23][^>]*>(.*?)</h[23]>", sec, re.S)
        title = re.sub(r"<[^>]+>", "", h.group(1)) if h else "(머리)"
        if only and f"{i:02d}" not in only:
            jobs.append((i, title, None))
            continue
        page = out / f"{i:02d}.html"
        page.write_text(head + "<main>" + sec + "</main>" + MEASURE + tail, encoding="utf-8")
        jobs.append((i, title, page))

    def shoot(i, page, mode):
        png = out / f"{i:02d}-{mode}.png"
        # 실행마다 프로필을 따로 줘야 연속 실행이 앞 실행에 넘어가지 않는다
        profile = out / f"profile-{i:02d}-{mode}"
        png.unlink(missing_ok=True)
        try:
            # --screenshot은 창만큼만 찍으므로 먼저 --dump-dom으로 절 높이를 재서 창을 늘린다
            size = MODES[mode][0]
            dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                                  f"--user-data-dir={profile}", size, "--dump-dom", page.as_uri()],
                                 capture_output=True, timeout=60).stdout.decode("utf-8", "replace")
            m = re.search(r'data-h="(\d+)"', dom)
            width, height = map(int, size.split("=")[1].split(","))
            warn = None
            if not m:
                warn = "높이를 재지 못해 기본 창 크기로 찍음"
            elif int(m.group(1)) > MAX_HEIGHT:
                warn = f"높이 {m.group(1)}px가 한계 {MAX_HEIGHT}px를 넘어 잘릴 수 있음"
            window = f"--window-size={width},{min(MAX_HEIGHT, max(height, int(m.group(1)))) if m else height}"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                            f"--user-data-dir={profile}", window, *MODES[mode][1:],
                            f"--screenshot={png}", page.as_uri()],
                           capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            return False, None
        return png.exists(), warn

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as pool:
        futures = [(i, title, {m: pool.submit(shoot, i, page, m) for m in MODES})
                   if page else (i, title, None) for i, title, page in jobs]
        for i, title, fs in futures:
            if fs is None:
                print(f"{i:02d} {title} (건너뜀)")
                continue
            res = {m: f.result() for m, f in fs.items()}
            missing = [m for m, r in res.items() if not r[0]]
            print(f"{i:02d} {title}" + (f" MISSING {missing}" if missing else ""))
            for m, r in res.items():
                if r[1]:
                    print(f"WARN {i:02d} {m}: {r[1]}")


if __name__ == "__main__":
    main(*sys.argv[1:])
