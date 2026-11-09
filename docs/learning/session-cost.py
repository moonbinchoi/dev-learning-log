"""세션 비용과 Opus 사용 이유를 보여 준다. 사용: python docs/learning/session-cost.py [transcript.jsonl]

인자가 없으면 CLAUDE_CODE_SESSION_ID의 기록을 읽는다. 이 스크립트가 앞서 성공적으로
보고한(결과가 "합계"로 시작한) 마지막 호출 뒤만 센다. 규칙: operating-rules.md "준비 세션 모델".
"""
import json
import os
import pathlib
import re
import sys

# $/MTok: 입력, 출력, 5분 쓰기, 1시간 쓰기, 캐시 읽기 (docs/research/token-audit-2026-11/scripts/common.py와 같다)
P = {"opus": (4, 20, 5, 8, 0.20), "sonnet": (2, 10, 2.5, 4, 0.20),
     "haiku": (0.10, 0.50, 0.125, 0.20, 0.01), "haiku_long": (0.50, 2.50, 0.625, 1.0, 0.05)}
PROJECT = pathlib.Path.home() / ".claude" / "projects" / "e--Study-Inflearn"
REASON = re.compile(r"^Opus-reason:\s*(.+)$", re.MULTILINE)


def cost(model, u):
    f = next((k for k in ("opus", "sonnet", "haiku") if k in model), "opus")  # 모르는 모델은 비싼 쪽으로 센다
    cc = u.get("cache_creation") or {}
    w5, w1 = cc.get("ephemeral_5m_input_tokens", 0), cc.get("ephemeral_1h_input_tokens", 0)
    tot_w = u.get("cache_creation_input_tokens", 0)
    if w5 + w1 != tot_w:
        w5 = tot_w - w1  # 나뉘지 않은 쓰기는 5분으로 본다
    i, o, r = u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("cache_read_input_tokens", 0)
    if f == "haiku" and i + tot_w + r > 100_000:
        f = "haiku_long"
    p = P[f]
    return (i * p[0] + o * p[1] + w5 * p[2] + w1 * p[3] + r * p[4]) / 1e6


def records(path):
    for line in open(path, encoding="utf-8"):
        try:
            yield json.loads(line)
        except ValueError:
            continue


def calls(rows, main=True):
    """메시지 id 하나를 한 번만: {id: {ts, model, usage, content}}. usage는 마지막 줄 값.
    서브에이전트 기록은 모든 줄이 isSidechain이라, 메인 기록에서만 그 줄을 뺀다."""
    seen = {}
    for d in rows:
        m = d.get("message") or {}
        if d.get("type") != "assistant" or (main and d.get("isSidechain")) or not m.get("id") or not m.get("usage"):
            continue
        if m.get("model", "").startswith("<"):
            continue
        c = seen.setdefault(m["id"], {"ts": d.get("timestamp", ""), "model": m["model"], "content": []})
        c["usage"] = m["usage"]
        c["content"] += m.get("content") or []
    return seen


def text_of(content):
    if isinstance(content, str):
        return content
    return " ".join(x.get("text", "") for x in content or [] if isinstance(x, dict))


def report(main_path):
    main_path = pathlib.Path(main_path)
    rows = list(records(main_path))
    main_calls = calls(rows)
    uses = {x["id"]: (x, c["ts"]) for c in main_calls.values() for x in c["content"] if x.get("type") == "tool_use"}
    cut = ""
    for d in rows:
        if d.get("type") != "user" or not isinstance((d.get("message") or {}).get("content"), list):
            continue
        for x in d["message"]["content"]:
            u = uses.get(x.get("tool_use_id")) if x.get("type") == "tool_result" else None
            if u and u[0].get("name") == "Bash" and "session-cost.py" in u[0]["input"].get("command", "") \
                    and text_of(x.get("content")).lstrip().startswith("합계"):
                cut = max(cut, d.get("timestamp", ""))

    main_total = main_opus = 0.0
    for c in main_calls.values():
        if c["ts"] > cut:
            x = cost(c["model"], c["usage"])
            main_total += x
            main_opus += x if "opus" in c["model"] else 0

    subs = []
    for f in sorted((main_path.parent / main_path.stem / "subagents").glob("agent-*.jsonl")):
        sc = calls(records(f), main=False)
        if not sc:
            continue
        mp = f.with_suffix(".meta.json")
        meta = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
        use = uses.get(meta.get("toolUseId"))
        start = use[1] if use else min(c["ts"] for c in sc.values())
        if start <= cut:
            continue
        total = sum(cost(c["model"], c["usage"]) for c in sc.values())
        opus = sum(cost(c["model"], c["usage"]) for c in sc.values() if "opus" in c["model"])
        m = REASON.search(use[0]["input"].get("prompt", "")) if use else None
        subs.append((start, meta, total, opus, m.group(1).strip() if m else "이유 없음"))
    subs.sort(key=lambda s: s[0])

    sub_total = sum(s[2] for s in subs)
    total = main_total + sub_total
    share = 100 * (main_opus + sum(s[3] for s in subs)) / total if total else 0.0
    out = [f"합계 ${total:.2f} (메인 ${main_total:.2f} · 서브에이전트 ${sub_total:.2f}) · Opus 비중 {share:.1f}%"]
    if main_opus:
        out.append(f"- 메인 ${main_opus:.2f} — 이유: 메인 모델")
    for _, meta, _, opus, reason in subs:
        if opus:
            out.append(f'- {meta.get("agentType", "?")} "{meta.get("description", "?")}" ${opus:.2f} — 이유: {reason}')
    return "\n".join(out)


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if argv:
        path = pathlib.Path(argv[0])
    else:
        sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
        if not sid:
            print("비용 계산 불가: CLAUDE_CODE_SESSION_ID 없음")
            return 1
        path = PROJECT / f"{sid}.jsonl"
    if not path.exists():
        print(f"비용 계산 불가: 기록 파일 없음 ({path})")
        return 1
    try:
        text = report(path)
    except Exception as e:  # 세션 끝 보고는 실패도 한 줄로 낸다(R10)
        print(f"비용 계산 불가: {type(e).__name__}: {e}")
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
