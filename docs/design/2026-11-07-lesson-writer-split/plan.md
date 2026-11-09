# 준비 세션 메인을 Sonnet으로 Implementation Plan
Status: approved

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 준비 세션이 트랙별 준비 모드에 따라 Sonnet(또는 Opus) 메인으로 돌고, 준비·강의 세션이 끝날 때 비용·Opus 사용 이유를 보여 주고 다음 준비 모드와 회차 피드백을 받아 기록한다.

**Architecture:** 비용 계산은 새 스크립트 `docs/learning/session-cost.py` 하나가 맡는다. 모드별 규칙과 세션 끝 보고는 `docs/learning/operating-rules.md`의 새 절 "준비 세션 모델" 하나에 모으고, 준비·강의 세션 규칙은 그 절을 가리키는 줄만 더한다. 상태는 트랙 폴더의 `prep-mode.txt`와 `feedback.md` 두 파일이다.

**Tech Stack:** Python 3.14 표준 라이브러리. 테스트는 이 폴더의 관례대로 assert 스크립트(`python docs/learning/test_*.py`).

**Spec:** `docs/design/2026-11-07-lesson-writer-split/spec.md`

## Global Constraints

- 준비 모드 값: `judgment`, `rules`, `opus`. 없거나 틀리면 `judgment`.
- 파일: `lecture/<track>/prep-mode.txt`(한 줄 값 하나), `lecture/<track>/feedback.md`(표 머리 `| 회차 | 준비 모델 | 준비 모드 | 강의 내용 | 자료 | 의견 |`, 제목 `# 회차 피드백`).
- 피드백 칸: `?` 아직 묻지 않음, `-` 넘김, 평가는 `좋음` / `보통` / `아쉬움`.
- 비용 출력 첫 줄: `합계 $X (메인 $A · 서브에이전트 $B) · Opus 비중 N.N%`. 오류: `비용 계산 불가: <이유>`, 종료 코드 1.
- 가격($/MTok, 입력·출력·5분 쓰기·1시간 쓰기·캐시 읽기): opus (4, 20, 5, 8, 0.20), sonnet (2, 10, 2.5, 4, 0.20), haiku (0.10, 0.50, 0.125, 0.20, 0.01), 입력 합 100,000 초과 haiku (0.50, 2.50, 0.625, 1.0, 0.05).
- `docs/learning/lesson-review.md`는 고치지 않는다.
- 커밋은 `CLAUDE.md` `## Git` 절차(경로별 add·commit, 사용자 확인, 한국어 메시지)로 한다.

## Review Focus

- 깨진 JSON 줄이 섞인 기록: 그 줄만 건너뛰고 계산한다 → Task 1 `test_skips_bad_lines`.
- `.meta.json`이 없는 서브에이전트: 종류·설명을 `?`로 두고 비용은 센다 → Task 1 `test_subagent_without_meta`.
- 호출이 하나도 없는 범위(직전 보고 바로 뒤에 다시 돌림): 합계 $0.00, 비중 0.0%로 나누기 오류 없이 낸다 → Task 1 `test_empty_range`.
- 스트리밍으로 같은 메시지 id가 여러 줄에 나옴: 한 번만, 마지막 usage로 센다 → Task 1 `test_dedupes_message_id`.
- 실패한 앞선 호출(`비용 계산 불가`)은 범위를 자르지 않는다 → Task 1 `test_cut_after_last_successful_report`.

---

### Task 1: 세션 비용 스크립트

Covers: R7, R8, R9, R10

**Files:**
- Create: `docs/learning/session-cost.py`
- Test: `docs/learning/test_session_cost.py`

**Interfaces:**
- Produces: CLI `python docs/learning/session-cost.py [transcript.jsonl]` → stdout 보고, 종료 코드 0/1. 모듈 함수 `cost(model: str, usage: dict) -> float`, `report(main_path: pathlib.Path) -> str`, `main(argv: list[str]) -> int`.
- Task 2가 CLI 이름과 출력 첫 줄 형식을 쓴다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`test_render_sections.py`처럼 `importlib`로 `session-cost.py`를 읽고, `tempfile`에 가짜 기록을 만든다. 가짜 기록 `<tmp>/S.jsonl`과 `<tmp>/S/subagents/agent-a.jsonl`·`agent-a.meta.json`. 레코드 모양은 실제 기록과 같다: `{"type":"assistant","timestamp":..,"message":{"id":..,"model":..,"usage":{..},"content":[..]}}`, 도구 결과는 `{"type":"user","timestamp":..,"message":{"content":[{"type":"tool_result","tool_use_id":..,"content":"..."}]}}`.

```python
def test_cost_price_table():
    assert cost("claude-opus-5-5", {"input_tokens": 1_000_000}) == 4.0
    assert cost("claude-sonnet-5-5", {"output_tokens": 1_000_000}) == 10.0
    assert cost("claude-opus-5-5", {"cache_read_input_tokens": 1_000_000}) == 0.20
    assert cost("claude-haiku-5-5", {"input_tokens": 200_000}) == 0.10  # 장문 가격

def test_report_main_subagent_reason():
    # 메인: sonnet 출력 100k 토큰($1.00) + Agent tool_use id "tu1", prompt에 "Opus-reason: 내용 검토"
    # 서브: meta {"agentType":"reviewer","description":"Review lesson","toolUseId":"tu1"}, opus 입력 1M($4.00)
    lines = report(main).splitlines()
    assert lines[0] == "합계 $5.00 (메인 $1.00 · 서브에이전트 $4.00) · Opus 비중 80.0%"
    assert lines[1] == '- reviewer "Review lesson" $4.00 — 이유: 내용 검토'

def test_missing_reason():  # prompt에 Opus-reason 없음
    assert report(main).splitlines()[1].endswith("— 이유: 이유 없음")

def test_main_opus_line():  # 메인 opus 입력 1M
    assert "- 메인 $4.00 — 이유: 메인 모델" in report(main).splitlines()

def test_cut_after_last_successful_report():
    # t1 호출($1) → t2 Bash "python docs/learning/session-cost.py" 결과 "합계 $1.00 ..."
    # → t3 Bash 같은 명령 결과 "비용 계산 불가: x" → t4 호출($2)
    assert report(main).splitlines()[0].startswith("합계 $2.00")

def test_empty_range():  # 성공 보고 뒤 호출 없음
    assert report(main).splitlines()[0] == "합계 $0.00 (메인 $0.00 · 서브에이전트 $0.00) · Opus 비중 0.0%"

def test_dedupes_message_id():  # 같은 id 두 줄, 둘째 줄 usage가 최종
    ...  # 합계가 둘째 usage 한 번 값

def test_skips_bad_lines():  # 중간에 "{not json" 줄
    ...  # 나머지로 계산, 예외 없음

def test_subagent_without_meta():
    ...  # 서브 opus 호출이 '- ? "?" $4.00 — 이유: 이유 없음'으로 나오고 합계에 들어감

def test_error_without_env():  # CLAUDE_CODE_SESSION_ID 지우고 인자 없이
    assert main([]) == 1  # stdout == "비용 계산 불가: CLAUDE_CODE_SESSION_ID 없음\n"

def test_error_missing_file():
    assert main([str(tmp / "nope.jsonl")]) == 1  # stdout이 "비용 계산 불가: 기록 파일 없음"으로 시작

def test_real_sonnet_arm():  # 파일이 없으면 건너뛴다
    p = pathlib.Path.home() / ".claude/projects/E--Study-model-test-2026-11-07-sonnet/6ab26202-b980-40be-a1a5-2e11d234e473.jsonl"
    if p.exists():
        assert report(p).splitlines()[0] == "합계 $12.44 (메인 $8.03 · 서브에이전트 $4.41) · Opus 비중 30.5%"
```

파일 끝에서 테스트 함수를 모두 부르고 `ok`를 출력한다.

- [ ] **Step 2: 실패를 확인한다**

Run: `python docs/learning/test_session_cost.py`
Expected: FAIL (`session-cost.py` 없음)

- [ ] **Step 3: `docs/learning/session-cost.py`를 만든다**

- `cost`: Global Constraints의 가격표와 `docs/research/token-audit-2026-11/scripts/common.py`의 `cost()` 식을 옮긴다(5분/1시간 쓰기 분리, 나머지 쓰기는 5분으로). 연구 폴더를 import하지 않는다.
- 기록 읽기: 줄마다 `json.loads`, 실패 줄은 건너뛴다. `isSidechain`이 참인 레코드와 `model`이 `<`로 시작하는 응답은 뺀다. 메시지 id로 묶고 마지막 usage를 쓴다.
- 범위: 메인 기록에서 `command`에 `session-cost.py`가 들어 있는 Bash tool_use를 찾고, 그 tool_result 텍스트가 `합계`로 시작하는 것 중 마지막 결과 레코드의 timestamp를 자르는 시각으로 쓴다. 메인 호출과 Agent tool_use(서브에이전트 시작 시각)는 그 시각보다 뒤인 것만 센다.
- 서브에이전트: 메인 경로 `<dir>/<stem>.jsonl`이면 `<dir>/<stem>/subagents/agent-*.jsonl`. meta의 `toolUseId`로 메인의 Agent 입력 `prompt`를 찾아 `^Opus-reason:\s*(.+)$`(MULTILINE)을 읽는다. 호출에 `opus` 모델이 하나라도 있으면 Opus 서브에이전트이고, 그 줄의 비용은 Opus 비용이다.
- 출력: 금액 소수 둘째 자리, 비중 소수 첫째 자리. 줄 순서는 메인 Opus 줄, 서브에이전트 시작 순.
- `main`: 인자가 없으면 `CLAUDE_CODE_SESSION_ID`로 `Path.home()/".claude/projects/e--Study-Inflearn/<id>.jsonl"`을 쓴다. stdout은 UTF-8.

- [ ] **Step 4: 통과를 확인한다**

Run: `python docs/learning/test_session_cost.py`
Expected: `ok`

- [ ] **Step 5: 커밋한다**

`CLAUDE.md` `## Git` 절차로 `docs/learning/session-cost.py`, `docs/learning/test_session_cost.py`. 메시지: `세션 비용과 Opus 사용 이유를 보여 주는 스크립트를 추가한다`

### Task 2: "준비 세션 모델" 절과 준비 세션 규칙

Covers: R1, R2, R3, R4, R5, R6, R11, R12, R15, R16, R17, R18

**Files:**
- Modify: `docs/learning/operating-rules.md` (준비 세션 규칙 1·5·10번, `## 레슨 설계` 바로 앞에 새 절)

**Interfaces:**
- Consumes: Task 1의 CLI와 출력 첫 줄 형식.
- Produces: 절 제목 `## 준비 세션 모델`과 하위 `### 세션 끝 보고`, `### 피드백 기록`. Task 3이 이 제목을 가리킨다.

- [ ] **Step 1: 새 절을 쓴다**

`## 준비 세션 모델`에 담을 것:
- 모드 파일·기본값·틀린 값 처리(`status.md` `Open judgments`에 `- prep-mode.txt 값 "<값>" → 선택: judgment`), 사용자가 직접 고쳐도 된다는 줄, 모드를 바꿔도 다른 규칙과 파일은 바뀌지 않는다는 줄.
- 표 `| 모드 | 메인 | Opus를 쓰는 곳 |`: `judgment` Sonnet, reviewer·analyst를 부를 때마다 `model`을 `opus`나 `sonnet`으로 주고 메인이 고른다. `rules` Sonnet, `lesson-review.md` 1단계 내용 검토의 reviewer와 worker·explorer·source-reader가 BLOCKED를 돌려준 뒤 판단을 맡기는 analyst만 Opus, 나머지는 Sonnet 이하. `opus` Opus, 전역 오케스트레이션 규칙 그대로.
- 메인 모델 판별: 시스템 프롬프트의 모델 ID에 `opus`면 Opus, `sonnet`이면 Sonnet, 그 밖은 어느 모드와도 맞지 않는다. 다시 여는 방법은 강의 세션 규칙 0번과 같다(`claude --model sonnet|opus`, 또는 `/model` 선택 창 그 줄의 `s`).
- 메인이 Opus를 고른 호출에는 `Model-lock: opus`를 넣는다. 이 절이 전역 규칙의 "프로젝트 규칙이 모델을 정함"에 해당한다는 한 줄.
- Opus로 돌 서브에이전트 브리프에는 준비·강의 세션 모두 `Opus-reason: <한 줄>`을 넣는다.

`### 세션 끝 보고`: 커밋 확인 메시지에 이 순서로 담고, 답을 파일에 적은 뒤 커밋한다.
1. (강의 세션만) 강의 세션 규칙 7번의 피드백 질문.
2. `python docs/learning/session-cost.py` 출력. 실패하면 그 한 줄만. 준비 모드 `judgment`·`rules`인 준비 세션에서 비중이 50.0%를 넘으면 첫 줄 끝에 ` — Opus 비중 목표(50%) 초과`.
3. 다음 준비 세션 방식: "메인이 판단해 Opus 사용" / "규칙으로 고정(내용 검토와 막혔을 때 판단만 Opus)" / "Opus로 되돌리기" = `judgment` / `rules` / `opus`. 답이 있으면 `prep-mode.txt`에 쓰고 커밋 대상에 넣고, 없으면 그대로 둔다.
4. 커밋 확인.

`### 피드백 기록`: `feedback.md` 형식(Global Constraints), 없으면 만든다, 회차 칸은 `status.md` `Round` 값, 한 회차 한 행.

- [ ] **Step 2: 준비 세션 규칙을 고친다**

- 1번: "그 밖에는 끝의 커밋 확인 말고 사용자에게 묻지 않는다"를 "그 밖에는 끝의 커밋 확인과, 같은 메시지의 모드 질문(\"준비 세션 모델\")말고 묻지 않는다"로. 이어서 "트랙이 정해지면 파일을 쓰기 전에 \"준비 세션 모델\"대로 모드를 읽고, 메인 모델이 그 모드의 모델이 아니면 다시 여는 방법을 알리고 멈춘다."
- 5번 5단계: `status.md`에 결과를 적을 때 `feedback.md`에 `Round` 행을 만들거나 갱신해 준비 모델(`sonnet`/`opus`)과 1번에서 읽은 모드를 적고 평가 칸 셋은 `?`로 둔다.
- 10번: 커밋 확인을 "준비 세션 모델"의 "세션 끝 보고"로 한다. 커밋 대상에 `feedback.md`와(바뀌었으면) `prep-mode.txt`가 들어간다.

- [ ] **Step 3: 확인한다**

Run: `grep -c "prep-mode.txt" docs/learning/operating-rules.md && grep -n "^## 준비 세션 모델\|^### 세션 끝 보고\|^### 피드백 기록\|Opus-reason\|Model-lock" docs/learning/operating-rules.md && git diff --stat HEAD -- docs/learning/lesson-review.md`
Expected: 첫 숫자 3 이상, 세 제목과 두 키워드 줄이 나오고, lesson-review.md diff는 비어 있다(R15).

R3(위임 예외 "준비 세션에서 조사 직후 같은 맥락에서 하는 레슨 작성...")·R17 문구가 남았는지 `git diff HEAD -- docs/learning/operating-rules.md`로 눈으로 본다. 1번의 질문 예외 말고 지운 줄이 없어야 한다.

- [ ] **Step 4: 커밋한다**

`CLAUDE.md` `## Git` 절차로 `docs/learning/operating-rules.md`. 메시지: `준비 세션 모델 절을 두고 준비 세션이 모드를 읽고 세션 끝에 비용을 보고하게 한다`

### Task 3: 강의 세션 규칙

Covers: R6, R7, R11, R13, R14

**Files:**
- Modify: `docs/learning/operating-rules.md` (강의 세션 규칙 2·7번)

**Interfaces:**
- Consumes: Task 2의 `## 준비 세션 모델` / `### 세션 끝 보고` / `### 피드백 기록`.

- [ ] **Step 1: 규칙을 고친다**

- 2번 끝에 한 줄: 그 회차를 준비한 모델과 모드는 채팅에 말하지 않는다.
- 7번 정리 대상 목록 뒤: `feedback.md`와 `prep-mode.txt`는 정리 대상이 아니다.
- 7번 끝: 정리를 마치면 커밋 확인을 "준비 세션 모델"의 "세션 끝 보고"로 한다. 맨 앞 피드백 질문은 "강의 내용"과 "자료(레슨 HTML·도식)"를 각각 좋음 / 보통 / 아쉬움으로, 한 줄 의견은 선택으로 묻는다. 답은 `feedback.md`의 그 회차 행에, 답하지 않은 칸은 `-`로 적는다. 행이 없으면 준비 모델·모드를 `?`로 두고 만든다.

- [ ] **Step 2: 확인한다**

Run: `grep -n "feedback.md" docs/learning/operating-rules.md`
Expected: 강의 세션 규칙 7번 안 줄(정리 제외, 피드백 기록)과 Task 2의 줄이 함께 나온다.

- [ ] **Step 3: 커밋한다**

`CLAUDE.md` `## Git` 절차로 `docs/learning/operating-rules.md`. 메시지: `강의 세션 마무리에 회차 피드백과 비용 보고를 더한다`

## Final verification

```bash
python docs/learning/test_session_cost.py && python docs/learning/session-cost.py ~/.claude/projects/E--Study-model-test-2026-11-07-sonnet/6ab26202-b980-40be-a1a5-2e11d234e473.jsonl | head -1
```
Expected:
```
ok
합계 $12.44 (메인 $8.03 · 서브에이전트 $4.41) · Opus 비중 30.5%
```
규칙(R1~R6, R11~R18)은 다음 실제 `/prepare-lesson`과 강의 마무리에서 확인한다: 시작 때 모드 확인, 커밋 확인 메시지의 비용·모드 질문(강의 세션은 피드백 질문 먼저), `feedback.md` 행과 `prep-mode.txt` 값.

## After implementation

- 루트 저장소는 `main` 하나이고 원격 PR 흐름이 없다. mattpocock-skills:pr로 본문을 쓰고, Evidence에 Final verification 출력을 넣고 `docs/design/2026-11-07-lesson-writer-split/`를 링크해 마지막 커밋 메시지 본문으로 쓴다.
- 실제 준비·강의 세션에서 규칙이 확인되면 intent.md, spec.md, plan.md를 `Status: implemented`로 바꾼다.
