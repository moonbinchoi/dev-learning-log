"""render-sections.py의 base 경로·높이 측정·경고를 확인한다. 사용: python docs/learning/test_render_sections.py"""
import contextlib
import importlib.util
import io
import pathlib
import struct
import tempfile
import zlib

spec = importlib.util.spec_from_file_location("render_sections", pathlib.Path(__file__).parent / "render-sections.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)


def make_png(w, h):
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    rows = b"".join(b"\x00" + b"\xff\x00\x00" * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def png_height(path):
    return struct.unpack(">I", path.read_bytes()[20:24])[0]


class Out(io.StringIO):
    def reconfigure(self, **kw):  # main()이 stdout을 UTF-8로 바꾸려 부른다
        pass


def run(tmp, body, **patch):
    """레슨을 만들어 render.main으로 찍고 (out 폴더, 출력 문자열)을 돌려준다."""
    tmp = pathlib.Path(tmp)
    (tmp / "lessons").mkdir(parents=True)
    (tmp / "assets" / "images").mkdir(parents=True)
    (tmp / "assets" / "style.css").write_text(".tall{height:3000px}", encoding="utf-8")
    # 단색 PNG. height 속성 없이 쓰므로 로드 전에는 높이를 모른다
    (tmp / "assets" / "images" / "tall.png").write_bytes(make_png(100, 3500))
    lesson = tmp / "lessons" / "t.html"
    lesson.write_text("<html><head><link rel='stylesheet' href='../assets/style.css'></head>"
                      f"<body><main>{body}</main></body></html>", encoding="utf-8")
    saved = {k: getattr(render, k) for k in patch}
    for k, v in patch.items():
        setattr(render, k, v)
    buf = Out()
    try:
        with contextlib.redirect_stdout(buf):
            render.main(lesson, tmp / "out")
    finally:
        for k, v in saved.items():
            setattr(render, k, v)
    return tmp / "out", buf.getvalue()


# 잘라 낸 페이지는 <head> 바로 뒤의 <base href>로 상대 경로를 푼다
lessons = pathlib.Path("C:/t/lessons")
page = render.add_base("<html><head><link href='../assets/style.css'></head><body></body></html>", lessons)
assert page.startswith(f'<html><head><base href="{lessons.as_uri()}/">')
# <header>는 <head>가 아니다. <head>가 없으면 맨 앞에 넣는다
page = render.add_base("<!-- <header> --><html><head lang='ko'><title>t</title></head></html>", lessons)
assert f"<head lang='ko'><base href=" in page and "<header><base" not in page
assert render.add_base("<p>x</p>", lessons).startswith("<base href=")

with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)

    # 이미지는 height 속성이 없어도 로드된 뒤 높이로 통째로 찍힌다(작은따옴표 src 포함)
    out, text = run(tmp / "a", "<h2>A</h2><p>short</p><h2>B</h2><img src='../assets/images/tall.png'><p>END</p>")
    for mode in ("light", "dark"):
        assert png_height(out / f"02-{mode}.png") >= 3500, mode
    assert png_height(out / "01-light.png") <= 2000  # 짧은 절은 기존 크기 이하
    assert png_height(out / "01-dark.png") <= 2400
    assert "WARN" not in text, text
    assert '<base href="' in (out / "02.html").read_text(encoding="utf-8")

    # stylesheet도 base로 풀린다
    out, _ = run(tmp / "b", "<h2>A</h2><div class='tall'></div>")
    assert png_height(out / "01-light.png") >= 3000

    # 높이를 못 쟀을 때는 WARN으로 절 번호와 모드를 알린다
    out, text = run(tmp / "c", "<h2>A</h2><p>x</p>", MEASURE="")
    assert "WARN 01 light" in text and "WARN 01 dark" in text, text

    # 높이가 브라우저 한계를 넘으면 WARN
    out, text = run(tmp / "d", "<h2>A</h2><div class='tall'></div>", MAX_HEIGHT=2500)
    assert "WARN 01 light" in text and "WARN 01 dark" in text, text
print("OK")
