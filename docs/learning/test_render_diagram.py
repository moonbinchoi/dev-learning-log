"""render-diagram.py의 SVG 변환과 레슨 삽입을 확인한다. 사용: python docs/learning/test_render_diagram.py"""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("render_diagram", pathlib.Path(__file__).parent / "render-diagram.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)

out = render.adapt('<style>@font-face { src: url("data:x") } .fill-N1{fill:#0A0F25;}</style>'
                   '<rect fill="#dae8fc" stroke="#6C8EBF" stop-fill="#111111" fill="none"/>')
assert "font-face" not in out
assert ".fill-N1{fill:var(--c-0a0f25, #0a0f25);}" in out
assert 'fill="var(--c-dae8fc, #dae8fc)"' in out
assert 'stroke="var(--c-6c8ebf, #6c8ebf)"' in out
assert 'stop-fill="#111111"' in out and 'fill="none"' in out

page = "<p>앞</p><!-- d2:flow -->\n옛 그림\n<!-- /d2 --><p>뒤</p>"
assert render.embed(page, "flow", "<svg/>") == "<p>앞</p><!-- d2:flow -->\n<svg/>\n<!-- /d2 --><p>뒤</p>"
assert render.embed(render.embed(page, "flow", "<a/>"), "flow", "<b/>").count("<a/>") == 0
try:
    render.embed(page, "other", "<svg/>")
except SystemExit:
    pass
else:
    raise AssertionError("표시가 없으면 멈춰야 한다")
print("OK")
