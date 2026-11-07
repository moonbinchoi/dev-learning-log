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


def absolutize(html, lesson_dir):
    # 잘라 낸 파일은 out_dir에 놓이므로 stylesheet·이미지의 상대 경로를 절대 file URL로 바꾼다
    assets = (pathlib.Path(lesson_dir) / "../assets").resolve().as_uri()
    return html.replace('"../assets/', f'"{assets}/')


def main(lesson, out, *only):
    sys.stdout.reconfigure(encoding="utf-8")
    lesson, out = pathlib.Path(lesson).resolve(), pathlib.Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    html = absolutize(lesson.read_text(encoding="utf-8"), lesson.parent)
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
        page.write_text(head + "<main>" + sec + "</main>" + tail, encoding="utf-8")
        jobs.append((i, title, page))

    def shoot(i, page, mode):
        png = out / f"{i:02d}-{mode}.png"
        # 실행마다 프로필을 따로 줘야 연속 실행이 앞 실행에 넘어가지 않는다
        profile = out / f"profile-{i:02d}-{mode}"
        png.unlink(missing_ok=True)
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                            f"--user-data-dir={profile}", *MODES[mode],
                            f"--screenshot={png}", page.as_uri()],
                           capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            return False
        return png.exists()

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as pool:
        futures = [(i, title, {m: pool.submit(shoot, i, page, m) for m in MODES})
                   if page else (i, title, None) for i, title, page in jobs]
        for i, title, fs in futures:
            if fs is None:
                print(f"{i:02d} {title} (건너뜀)")
                continue
            missing = [m for m, f in fs.items() if not f.result()]
            print(f"{i:02d} {title}" + (f" MISSING {missing}" if missing else ""))


if __name__ == "__main__":
    main(*sys.argv[1:])
