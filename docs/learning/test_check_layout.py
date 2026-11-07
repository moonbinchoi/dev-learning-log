"""check-layout.py의 검사를 픽스처 HTML로 확인한다. 사용: python docs/learning/test_check_layout.py"""
import pathlib
import struct
import subprocess
import sys
import tempfile
import zlib

HERE = pathlib.Path(__file__).parent
LONG = "word " * 300
WRAP = "very long link text " * 8
FIXTURE = f"""<!doctype html><html><head><meta charset="utf-8"><title>t</title><style>
body{{background:#fff;color:#111}}a{{color:inherit}}code{{overflow-wrap:anywhere}}
@media (prefers-color-scheme: dark){{body{{background:#121212;color:#eee}}.dk{{color:#555}}}}
</style></head><body>
<h2>overlap-case</h2>
<p style="margin:0">first</p><p style="margin:0;position:relative;top:-1em">second</p>
<h2>clip-case</h2>
<div style="height:40px;overflow:hidden">1<br>2<br>3<br>4<br>5</div>
<h2>p-overflow-case</h2>
<p style="white-space:nowrap">{LONG}</p>
<h2>svg-overflow-case</h2>
<svg width="1200" height="20"></svg>
<h2>light-contrast-case</h2>
<p style="color:#777">light</p>
<h2>dark-contrast-case</h2>
<p class="dk">dark</p>
<h2>svg-rect-case</h2>
<svg width="200" height="30"><rect width="200" height="30" fill="#fff"/><text x="10" y="20" fill="#ccc">svg</text></svg>
<h2>grouped-case</h2>
<p class="muted" style="color:#888">a</p><p class="muted" style="color:#888">b</p><p class="muted" style="color:#888">c</p>
<h2>unparsed-case</h2>
<p style="color: color(display-p3 0.5 0.5 0.5)">p3</p>
<h2>control-pass</h2>
<p style="color:#767676;background:#fff">pass</p>
<h2>control-large</h2>
<p style="font-size:24px;color:#949494;background:#fff">large</p>
<h2>control-bold</h2>
<p style="font-weight:700;font-size:19px;color:#949494;background:#fff">bold</p>
<h2>pseudo-case</h2>
<style>.lbl::before{{content:"예측";color:#999}}</style><p class="lbl">pseudo</p>
<h2>control-pre</h2>
<pre>{LONG}</pre>
<h2>control-wrap</h2>
<p><a href="#">{WRAP}</a> <code>x</code></p>
<h2>control-table</h2>
<table style="border-collapse:collapse"><tr><td style="border:1px solid #111">a</td><td style="border:1px solid #111">b</td></tr><tr><td style="border:1px solid #111">c</td><td style="border:1px solid #111">d</td></tr></table>
<h2>code-break-case</h2>
<table style="border-collapse:collapse;width:300px"><tr><td style="border:1px solid #111">k</td><td style="border:1px solid #111"><code>org.springframework.web.servlet.config.annotation.WebMvcConfigurer</code></td></tr></table>
<h2>control-code-space</h2>
<table style="border-collapse:collapse;width:300px"><tr><td style="border:1px solid #111">k</td><td style="border:1px solid #111"><code>{WRAP}</code></td></tr></table>
<h2>code-break-space-case</h2>
<table style="border-collapse:collapse;width:300px"><tr><td style="border:1px solid #111">k</td><td style="border:1px solid #111"><code>org.springframework.web.servlet.HandlerInterceptor x</code></td></tr></table>
<h2>relative-img-case</h2>
<div style="width:400px"><img src="../assets/images/wide.png"></div>
<h2>bottom-case</h2>
<div style="height:3000px"></div>
<p style="color:#808080">bottom</p>
</body></html>"""

BOTH = ("light-1000", "dark-500")
LIGHT, DARK = ("light-1000",), ("dark-500",)
# (모드, 절, 검사, 측정값 칸에 들어갈 글)
EXPECT = [
    (BOTH, "overlap-case", "overlap", "겹침 "),
    (BOTH, "clip-case", "clip-y", ""),
    (BOTH, "p-overflow-case", "overflow", ""),
    (BOTH, "svg-overflow-case", "overflow", ""),
    (BOTH, "code-break-case", "code-break", ""),
    (BOTH, "code-break-space-case", "code-break", ""),
    (BOTH, "relative-img-case", "overflow", ""),
    (LIGHT, "light-contrast-case", "contrast", "4.48:1 < 4.5:1"),
    (DARK, "dark-contrast-case", "contrast", "2.51:1 < 4.5:1"),
    (DARK, "svg-rect-case", "contrast", "1.61:1"),
    (LIGHT, "bottom-case", "contrast", "3.95:1"),
    (LIGHT, "grouped-case", "contrast", "3.54:1"),
    (LIGHT, "unparsed-case", "contrast", "색 해석 불가"),
    (LIGHT, "pseudo-case", "contrast", "2.85:1 < 4.5:1"),
]
# (모드, 절): 이 절의 줄이 있으면 안 된다
FORBID = [(BOTH, "control-pass"), (BOTH, "control-large"), (BOTH, "control-bold"), (DARK, "control-pre"),
          (BOTH, "control-wrap"), (BOTH, "control-table"),
          (BOTH, "control-code-space")]


def wide_png(w=1200, h=10):
    """w x h 단색 PNG 바이트."""
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    raw = (b"\x00" + b"\x80\x80\x80" * w) * h
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def main():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        (pathlib.Path(tmp) / "assets/images").mkdir(parents=True)
        (pathlib.Path(tmp) / "assets/images/wide.png").write_bytes(wide_png())
        (pathlib.Path(tmp) / "lesson").mkdir()
        page = pathlib.Path(tmp) / "lesson/fixture.html"
        page.write_text(FIXTURE, encoding="utf-8")
        out = subprocess.run([sys.executable, str(HERE / "check-layout.py"), str(page)],
                             capture_output=True, encoding="utf-8", timeout=180)
    rows = [l.split(" | ", 4) + ["", ""] for l in out.stdout.splitlines()]
    errors = [f"실행 실패: {out.stderr.strip()[-300:]}"] if out.returncode else []
    for modes, sec, check, measure in EXPECT:
        for mode in modes:
            if not any(r[:3] == [mode, sec, check] and measure in r[4] for r in rows):
                errors.append(f"빠짐: {mode} | {sec} | {check} | {measure}")
    for modes, sec in FORBID:
        for r in rows:
            if r[0] in modes and r[1] == sec:
                errors.append("나오면 안 됨: " + " | ".join(r[:5]))
    g = [r for r in rows if r[1:3] == ["grouped-case", "contrast"]]
    n = len(g)
    if n != 1 or " 외 2개" not in g[0][3]:
        errors.append(f"grouped-case contrast 줄이 {n}개이거나 요소 칸에 외 2개가 없다 (기대 1개)")
    assert not errors, "\n" + "\n".join(errors) + "\n--- 출력 ---\n" + out.stdout
    print("OK")


if __name__ == "__main__":
    main()
