"""레슨 산문의 AI 문체 패턴을 센다. 판단 재료일 뿐 자동 불합격 기준이 아니다.

사용: python .tools/im-not-ai/check-korean.py <파일>...
결과: 파일마다 `파일 | 글자 수 | 패턴 수 | 1천 자당 | 패턴별 개수`, 이어서 찾을 수 있는 문장을 `  패턴 | 문장`으로 쓴다.
`risk_band`와 `route_hint`는 쓰지 않는다. 길이에 좌우되고, AI 문체 표본도 low가 나온다.
도구가 동작하지 않으면 1로 끝난다.
"""
import html
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import tempfile

VENDOR = pathlib.Path(__file__).resolve().parent / "upstream"


def prose(path):
    """코드와 태그를 뺀 산문만 남긴다. 코드 조각은 문장이 끊기지 않게 낱말 하나로 바꾼다."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    if str(path).endswith(".html"):
        text = re.sub(r"(?is)<(style|script|svg|pre|head|nav)\b.*?</\1>", "\n", text)
        text = re.sub(r"(?is)<code\b[^>]*>.*?</code>", "코드", text)
        text = re.sub(r"(?i)</(p|li|tr|h\d|div|td|th|figcaption)>", "\n", text)
        text = html.unescape(re.sub(r"<[^>]+>", "", text))
    else:
        text = re.sub(r"(?s)```.*?```", "\n", text)
        text = re.sub(r"!\[[^\]]*\]\(.*?\)", "", text)
        text = re.sub(r"`[^`\n]+`", "코드", text)
        text = re.sub(r"(?m)^[ \t]*(#+|[-*]|>)[ \t]*", "", text).replace("**", "")
    return re.sub(r"\n{2,}", "\n\n", text).strip()


def load_shim(vendor):
    spec = importlib.util.spec_from_file_location(
        "prepare_monolith_input", vendor / "scripts" / "prepare_monolith_input.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scan(text, vendor=VENDOR):
    """레포의 사전 점수 도구를 돌려 패턴별 개수와 걸린 문장을 돌려준다."""
    with tempfile.TemporaryDirectory() as tmp:
        run = pathlib.Path(tmp) / "run"
        run.mkdir()
        (run / "01_input.txt").write_text(text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-I", str(vendor / "scripts" / "prepare_monolith_input.py"),
             "--run-dir", str(run), "--genre", "report"],
            cwd=tmp, capture_output=True,
        )
        metrics_file = run / "00_metrics.json"
        # 도구는 지표 계산이 실패해도 0으로 끝나므로 오류 파일까지 본다
        if result.returncode or (run / "00_metrics.error").exists() or not metrics_file.exists():
            raise RuntimeError(result.stderr.decode("utf-8", "replace")[-500:] or "지표 계산 실패")
        data = json.loads(metrics_file.read_text(encoding="utf-8"))

    shim = load_shim(vendor)
    counts = dict(data["route_signals"]["v26_tells"])
    for block, keys in ((data["metrics"], shim._ROUTE_TELL_KEYS_V16),
                        (data["v2_metrics"], shim._ROUTE_TELL_KEYS_V2)):
        counts.update({key: int(block[key]) for key in keys if block.get(key)})
    hits = []
    for name, pattern in shim._V26_ROUTE_PATTERNS:
        for match in pattern.finditer(text):
            start = text.rfind("\n", 0, match.start()) + 1
            end = text.find("\n", match.end())
            hits.append((name, text[start:end if end >= 0 else None].strip()[:120]))
    return {
        "chars": data["char_count"],
        "tells": data["route_signals"]["lexical_tell_count"],
        "counts": counts,
        "hits": hits,
    }


def main(paths):
    sys.stdout.reconfigure(encoding="utf-8")
    for path in paths:
        result = scan(prose(path))
        per_k = result["tells"] / max(result["chars"], 1) * 1000
        print(f"{path} | {result['chars']}자 | {result['tells']}건 | {per_k:.2f}/1k | "
              f"{json.dumps(result['counts'], ensure_ascii=False)}")
        for name, line in result["hits"]:
            print(f"  {name} | {line}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
