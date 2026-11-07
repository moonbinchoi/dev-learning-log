"""render-sections.py의 상대 경로 치환을 확인한다. 사용: python docs/learning/test_render_sections.py"""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("render_sections", pathlib.Path(__file__).parent / "render-sections.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)

lessons = pathlib.Path("C:/t/lessons")
assets = (lessons / "../assets").resolve().as_uri()
html = ('<link href="../assets/style.css"><img src="../assets/images/a.png">'
        '<img src="../assets/diagrams/b.svg"><a href="../reference/glossary.html">')
out = render.absolutize(html, lessons)
assert f'href="{assets}/style.css"' in out
assert f'src="{assets}/images/a.png"' in out
assert f'src="{assets}/diagrams/b.svg"' in out
assert '"../assets/' not in out
assert 'href="../reference/glossary.html"' in out  # 링크는 찍는 데 쓰지 않으므로 그대로
print("OK")
