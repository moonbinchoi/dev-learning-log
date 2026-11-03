"""D2 도식을 레슨용 SVG와 에디터 탭용 PNG로 만든다.

사용: python docs/learning/render-diagram.py <그림.d2> [레슨.html]
결과: 같은 폴더의 <그림>.svg, <그림>.png. 레슨을 주면 `<!-- d2:그림 -->`와 `<!-- /d2 -->` 사이를 SVG로 바꾼다.

SVG는 인라인으로 넣어야 style.css의 단계 강조가 닿는다. 임베드 폰트를 빼서 크기를 줄이고, 색 hex를
`var(--c-<hex>, #<hex>)`로 바꿔 다크 색을 style.css 한 곳에서 정한다. PNG는 라이트 색 그대로다.
"""
import pathlib
import re
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D2 = ROOT / ".tools/d2/d2.exe"
FONT = r"C:\Windows\Fonts"
FLAGS = [f"--font-regular={FONT}\\malgun.ttf", f"--font-bold={FONT}\\malgunbd.ttf", f"--font-italic={FONT}\\malgun.ttf"]


def adapt(svg):
    svg = re.sub(r"@font-face\s*\{[^}]*\}", "", svg)
    # 색은 속성(fill="#...")과 D2의 CSS 규칙(fill:#...) 두 형식으로 나온다
    return re.sub(r'(?<![\w-])(fill|stroke)(="|:\s*)#([0-9a-fA-F]{6})',
                  lambda m: f"{m[1]}{m[2]}var(--c-{m[3].lower()}, #{m[3].lower()})", svg)


def embed(page, name, svg):
    # shortcut: 같은 이름의 표시가 두 번 있으면 첫 번째만 바꾼다. 한 레슨에서 같은 그림을 두 번 쓰게 되면 표시를 나눈다
    head, mark, rest = page.partition(f"<!-- d2:{name} -->")
    body, end, tail = rest.partition("<!-- /d2 -->")
    if not mark or not end:
        sys.exit(f"레슨에 <!-- d2:{name} --> ... <!-- /d2 --> 표시가 없다")
    return f"{head}{mark}\n{svg}\n{end}{tail}"


def main(source, lesson=None):
    sys.stdout.reconfigure(encoding="utf-8")
    source = pathlib.Path(source).resolve()
    want = tomllib.loads((ROOT / "versions.toml").read_text(encoding="utf-8"))["versions"]["d2"]
    got = subprocess.run([D2, "--version"], capture_output=True, encoding="utf-8").stdout.strip()
    if got != f"v{want}":
        sys.exit(f"d2 버전이 versions.toml과 다르다: {got}, 기대값 v{want}")
    svg, png = source.with_suffix(".svg"), source.with_suffix(".png")
    for out in (svg, png):
        # 절대 경로로 넘기면 D2가 `...@lesson-theme` import를 찾지 못한다
        done = subprocess.run([D2, *FLAGS, source.name, out.name], cwd=source.parent, capture_output=True, encoding="utf-8")
        if done.returncode:
            sys.exit(done.stderr)
    text = adapt(svg.read_text(encoding="utf-8"))
    svg.write_text(text, encoding="utf-8")
    if lesson:
        lesson = pathlib.Path(lesson)
        lesson.write_text(embed(lesson.read_text(encoding="utf-8"), source.stem, text), encoding="utf-8")
    width = re.search(r'viewBox="\S+ \S+ (\d+)', text)[1]
    print(f"{svg.name} {len(text) // 1024}KB, 폭 {width}, {png.name}")


if __name__ == "__main__":
    main(*sys.argv[1:])
