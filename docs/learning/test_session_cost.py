"""session-cost.py의 비용 계산·범위 자르기·Opus 이유·오류 줄을 확인한다. 사용: python docs/learning/test_session_cost.py"""
import contextlib
import importlib.util
import io
import json
import os
import pathlib
import tempfile

spec = importlib.util.spec_from_file_location("session_cost", pathlib.Path(__file__).parent / "session-cost.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
cost, report, main = sc.cost, sc.report, sc.main

OPUS, SONNET = "claude-opus-5-5", "claude-sonnet-5-5"
CMD = "python docs/learning/session-cost.py"
n = 0


def call(model, usage, content=(), ts="2026-11-09T01:00:00Z", mid=None):
    global n
    n += 1
    return {"type": "assistant", "timestamp": ts,
            "message": {"id": mid or f"m{n}", "model": model, "usage": usage, "content": list(content)}}


def result(tid, text, ts):
    return {"type": "user", "timestamp": ts,
            "message": {"content": [{"type": "tool_result", "tool_use_id": tid, "content": text}]}}


def agent_use(tid, prompt):
    return {"type": "tool_use", "id": tid, "name": "Agent", "input": {"prompt": prompt, "description": "d"}}


def bash_use(tid):
    return {"type": "tool_use", "id": tid, "name": "Bash", "input": {"command": CMD}}


def write(dirpath, main_rows, subs=()):
    """subs: (rows, meta 또는 None) 목록. 메인 기록 경로를 돌려준다."""
    d = pathlib.Path(dirpath)
    p = d / "S.jsonl"
    p.write_text("\n".join(r if isinstance(r, str) else json.dumps(r, ensure_ascii=False) for r in main_rows), encoding="utf-8")
    sd = d / "S" / "subagents"
    sd.mkdir(parents=True, exist_ok=True)
    for i, (rows, meta) in enumerate(subs):
        (sd / f"agent-{i}.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
        if meta is not None:
            (sd / f"agent-{i}.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return p


def lines(p):
    return report(p).splitlines()


def test_cost_price_table():
    assert cost(OPUS, {"input_tokens": 1_000_000}) == 4.0
    assert cost(SONNET, {"output_tokens": 1_000_000}) == 10.0
    assert cost(OPUS, {"cache_read_input_tokens": 1_000_000}) == 0.20
    assert abs(cost("claude-haiku-5-5", {"input_tokens": 200_000}) - 0.10) < 1e-9  # 장문 가격


def test_report_main_subagent_reason(tmp):
    p = write(tmp, [call(SONNET, {"output_tokens": 100_000}, [agent_use("tu1", "Summary: x\nOpus-reason: 내용 검토\n")])],
              [([call(OPUS, {"input_tokens": 1_000_000})], {"agentType": "reviewer", "description": "Review lesson", "toolUseId": "tu1"})])
    out = lines(p)
    assert out[0] == "합계 $5.00 (메인 $1.00 · 서브에이전트 $4.00) · Opus 비중 80.0%", out
    assert out[1] == '- reviewer "Review lesson" $4.00 — 이유: 내용 검토', out


def test_missing_reason(tmp):
    p = write(tmp, [call(SONNET, {"output_tokens": 1}, [agent_use("tu1", "Summary: x")])],
              [([call(OPUS, {"input_tokens": 1_000_000})], {"agentType": "reviewer", "description": "R", "toolUseId": "tu1"})])
    assert lines(p)[1].endswith("— 이유: 이유 없음"), lines(p)


def test_main_opus_line(tmp):
    p = write(tmp, [call(OPUS, {"input_tokens": 1_000_000})])
    assert "- 메인 $4.00 — 이유: 메인 모델" in lines(p), lines(p)


def test_cut_after_last_successful_report(tmp):
    p = write(tmp, [
        call(SONNET, {"output_tokens": 100_000}, ts="2026-11-09T01:00:00Z"),
        call(SONNET, {"output_tokens": 1}, [bash_use("b1")], ts="2026-11-09T02:00:00Z"),
        result("b1", "합계 $1.00 (메인 $1.00 · 서브에이전트 $0.00) · Opus 비중 0.0%", "2026-11-09T02:00:01Z"),
        call(SONNET, {"output_tokens": 0}, [bash_use("b2")], ts="2026-11-09T03:00:00Z"),
        result("b2", "비용 계산 불가: x", "2026-11-09T03:00:01Z"),
        call(SONNET, {"output_tokens": 200_000}, ts="2026-11-09T04:00:00Z"),
    ])
    assert lines(p)[0].startswith("합계 $2.00 "), lines(p)


def test_empty_range(tmp):
    p = write(tmp, [
        call(SONNET, {"output_tokens": 100_000}, [bash_use("b1")], ts="2026-11-09T02:00:00Z"),
        result("b1", "합계 $1.00 (메인 $1.00 · 서브에이전트 $0.00) · Opus 비중 0.0%", "2026-11-09T02:00:01Z"),
    ])
    assert lines(p)[0] == "합계 $0.00 (메인 $0.00 · 서브에이전트 $0.00) · Opus 비중 0.0%", lines(p)


def test_dedupes_message_id(tmp):
    p = write(tmp, [call(SONNET, {"output_tokens": 50_000}, mid="same"), call(SONNET, {"output_tokens": 100_000}, mid="same")])
    assert lines(p)[0].startswith("합계 $1.00 "), lines(p)


def test_skips_bad_lines(tmp):
    p = write(tmp, [call(SONNET, {"output_tokens": 100_000}), "{not json"])
    assert lines(p)[0].startswith("합계 $1.00 "), lines(p)


def test_subagent_without_meta(tmp):
    p = write(tmp, [call(SONNET, {"output_tokens": 0})], [([call(OPUS, {"input_tokens": 1_000_000})], None)])
    out = lines(p)
    assert out[0].startswith("합계 $4.00 "), out
    assert out[1] == '- ? "?" $4.00 — 이유: 이유 없음', out


def test_subagent_sidechain_rows_count(tmp):  # 서브에이전트 기록은 모든 줄이 isSidechain이다
    row = call(OPUS, {"input_tokens": 1_000_000})
    row["isSidechain"] = True
    p = write(tmp, [call(SONNET, {"output_tokens": 0})], [([row], None)])
    assert lines(p)[0].startswith("합계 $4.00 "), lines(p)


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(argv)
    return code, buf.getvalue()


def test_error_without_env():
    old = os.environ.pop("CLAUDE_CODE_SESSION_ID", None)
    try:
        assert run_main([]) == (1, "비용 계산 불가: CLAUDE_CODE_SESSION_ID 없음\n")
    finally:
        if old is not None:
            os.environ["CLAUDE_CODE_SESSION_ID"] = old


def test_error_missing_file(tmp):
    code, out = run_main([str(pathlib.Path(tmp) / "nope.jsonl")])
    assert code == 1 and out.startswith("비용 계산 불가: 기록 파일 없음"), out


def test_error_broken_meta(tmp):  # 반쯤 쓰인 meta.json도 실패 한 줄로 낸다
    p = write(tmp, [call(SONNET, {"output_tokens": 1})], [([call(OPUS, {"input_tokens": 1})], None)])
    (pathlib.Path(tmp) / "S" / "subagents" / "agent-0.meta.json").write_text("{half", encoding="utf-8")
    code, out = run_main([str(p)])
    assert code == 1 and out.startswith("비용 계산 불가: ") and out.count("\n") == 1, out


def test_real_sonnet_arm():  # 기록이 없으면 건너뛴다
    p = pathlib.Path.home() / ".claude/projects/E--Study-model-test-2026-11-07-sonnet/6ab26202-b980-40be-a1a5-2e11d234e473.jsonl"
    if p.exists():
        assert lines(p)[0] == "합계 $12.44 (메인 $8.03 · 서브에이전트 $4.41) · Opus 비중 30.5%", lines(p)[0]


for name, fn in list(globals().items()):
    if name.startswith("test_"):
        if fn.__code__.co_argcount:
            with tempfile.TemporaryDirectory() as t:
                fn(t)
        else:
            fn()
print("ok")
