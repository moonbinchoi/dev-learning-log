# Spec: 준비 세션 메인을 Sonnet으로
From: intent.md · Status: approved

## Requirements
- R1 (← G1, G4). WHEN 준비 세션이 트랙을 확정하면(인자 `<track>`, 없으면 사용자에게 묻는 지금 방식) THE SYSTEM SHALL 파일을 쓰기 전에 그 트랙의 준비 모드를 읽는다. 값은 `judgment`, `rules`, `opus` 중 하나다. 파일이 없거나 값이 셋 중 하나가 아니면 `judgment`로 보고, 값이 틀린 경우 `status.md` `Open judgments`에 적는다.
- R2 (← G1, G4). IF 메인 모델이 준비 모드가 요구하는 모델이 아니면 THEN THE SYSTEM SHALL 파일을 쓰기 전에 요구 모델로 다시 여는 방법을 알리고 멈춘다. 요구 모델은 `judgment`·`rules`이면 Sonnet, `opus`이면 Opus다.
- R3 (← G1). WHILE 준비 세션이 돌면 THE SYSTEM SHALL 레슨 작성, 그 레슨의 검토 지적 수정, 용어집 갱신을 서브에이전트에 맡기지 않고 메인이 한다.
- R4 (← G2). WHILE 준비 모드가 `judgment`이면 THE SYSTEM SHALL 기본 모델이 Opus인 에이전트(reviewer, analyst)를 부를 때마다 모델을 `opus`나 `sonnet`으로 명시한다. 어느 쪽인지는 메인이 판단한다.
- R5 (← G2). WHILE 준비 모드가 `rules`이면 THE SYSTEM SHALL 다음 두 곳에만 Opus를 쓰고, 나머지 호출은 모두 Sonnet 이하로 부른다: (1) `lesson-review.md` 1단계 내용 검토의 reviewer, (2) worker·explorer·source-reader가 BLOCKED를 돌려준 뒤 메인이 판단을 맡기는 analyst.
- R6 (← G2, G7). WHEN 준비·강의 세션이 Opus로 돌 서브에이전트를 부르면 THE SYSTEM SHALL 그 브리프에 `Opus-reason: <한 줄>`을 넣는다.
- R7 (← G7). WHEN 준비·강의 세션이 커밋 확인 멈춤에 이르면 THE SYSTEM SHALL 같은 메시지에서 그 세션의 합계 비용을 메인과 서브에이전트로 나눠 보여 준다.
- R8 (← G7). WHEN R7의 비용을 보여 줄 때 THE SYSTEM SHALL Opus 비중을 함께 보여 준다.
- R9 (← G7). WHEN R7의 비용을 보여 줄 때 THE SYSTEM SHALL Opus로 돈 호출마다 에이전트 종류, 호출 설명(Agent 호출의 description), 비용, `Opus-reason`(없으면 "이유 없음")을 한 줄씩 보여 준다.
- R10 (← G7). IF 비용을 계산하지 못하면 THEN THE SYSTEM SHALL R7~R9 대신 이유를 한 줄로 알린다.
- R11 (← G7, G4). WHEN 준비·강의 세션이 커밋 확인 멈춤에 이르면 THE SYSTEM SHALL 같은 메시지에서 다음 준비 세션의 방식을 "메인이 판단해 Opus 사용" / "규칙으로 고정(내용 검토와 막혔을 때 판단만 Opus)" / "Opus로 되돌리기" 중에서 묻는다. 이 셋은 각각 `judgment` / `rules` / `opus`다. 선택지는 현재 모드와 상관없이 값을 가리키고, 현재 모드는 보여 주지 않는다(2026-11-09 사용자 결정: "지금 방식 유지"라는 이름은 `rules`·`opus` 트랙을 `judgment`로 바꿔 버린다). 답이 있으면 준비 모드를 그 값으로 바꾸고 커밋 대상에 넣는다. 답이 없으면 바꾸지 않는다.
- R12 (← G3). WHEN 준비 세션이 `status.md`에 결과를 적을 때 THE SYSTEM SHALL 피드백 기록에 `Round` 값의 행을 만들거나(있으면 갱신) 메인 모델과 R1에서 읽은 준비 모드를 적고, 평가 칸에는 `?`(아직 묻지 않음)를 적는다.
- R13 (← G3). WHEN 강의 세션이 마무리 정리(강의 세션 규칙 7번)를 끝내면 THE SYSTEM SHALL 커밋 확인 멈춤 메시지의 맨 앞에서 "강의 내용"과 "자료(레슨 HTML·도식)"를 각각 좋음 / 보통 / 아쉬움으로 묻고, 한 줄 의견은 선택으로 받는다. 답은 그 회차 행에 적고, 답하지 않은 칸은 `-`(넘김)로 둔다. 행이 없으면 준비 모델·모드를 `?`로 두고 만든다.
- R14 (← G3). WHILE 강의 세션이 돌면 THE SYSTEM SHALL 그 회차를 준비한 모델이나 모드를 채팅에 말하지 않는다.
- R15 (← G5). 준비 세션의 레슨 검토는 `lesson-review.md`의 체크리스트, 내용→시각 2단계 검토, 출처 인용 기준을 그대로 따르고, 통과하지 못하면 `status.md`에 `Review: passed`를 적지 않는다. 이 밖의 수치 품질 기준은 두지 않는다.
- R16 (← G6). IF 준비 모드가 `judgment`나 `rules`인 준비 세션의 Opus 비중이 50.0%를 넘으면 THEN THE SYSTEM SHALL R8 옆에 "Opus 비중 목표(50%) 초과"를 붙인다.
- R17 (← G7, Constraints). 준비 세션은 트랙 확정과, 커밋 확인 멈춤에서 함께 하는 R11 질문 말고는 사용자에게 묻지 않는다. R2의 안내는 질문이 아니라 멈춤이다.
- R18 (← G4). 준비 모드 값을 바꾸는 일(R11, 또는 사용자가 파일을 직접 고침)은 다른 운영 규칙이나 파일을 바꾸지 않는다.

## Design
- **준비 모드**: `lecture/<track>/prep-mode.txt`, 한 줄에 값 하나. 트랙 폴더에 두므로 준비·강의 세션의 쓰기 범위 안이다(준비 세션은 "쓰기는 자기 트랙 폴더에서만", 공유 파일 `docs/` 등은 강의가 아닌 세션에서만 고친다). 사용자는 언제든 이 파일을 직접 고쳐 되돌릴 수 있다. 모드별 규칙은 `docs/learning/operating-rules.md`에 "준비 세션 모델" 절 하나로 모은다.
- **메인 모델 판별**(R2): 메인은 시스템 프롬프트에 적힌 자기 모델 ID를 본다. `opus`를 포함하면 Opus, `sonnet`을 포함하면 Sonnet이고, 그 밖(Haiku 등)은 어느 요구 모델과도 맞지 않는다. 다시 여는 방법은 강의 세션 규칙 0번과 같다. `claude --model sonnet|opus`로 새로 열거나 `/model` 선택 창에서 그 줄의 `s`(이 세션만)를 누른다. 스킬 frontmatter의 `model`은 그 턴에만 적용되므로 쓰지 않는다. 준비 세션 규칙 1번 바로 뒤에 둔다.
- **Opus 고정**: 전역 Jev 라우터는 브리프 Summary를 보고 모델을 낮출 수 있다. 그래서 R4·R5에서 메인이 `opus`를 고른 호출에는 `Model-lock: opus` 줄도 넣는다. 전역 규칙이 Model-lock을 허용하는 조건 "프로젝트 규칙이 모델을 정함"을 "준비 세션 모델" 절이 채운다.
- **피드백 기록**(R12·R13): `lecture/<track>/feedback.md`. 없으면 `# 회차 피드백` 제목과 표 머리 `| 회차 | 준비 모델 | 준비 모드 | 강의 내용 | 자료 | 의견 |`로 만든다. 한 회차에 한 행이고, 회차 칸은 `status.md` `Round` 값이다. 준비 모델 칸은 `sonnet`/`opus`다. 준비 폴더 `prep/NN/`은 강의 마무리 정리에서 지워지므로, 모델 정보는 준비 세션이 미리 적는다. 이 파일과 `prep-mode.txt`는 마무리 정리 대상에서 뺀다.
- **비용 스크립트**(R7~R10, R16): `docs/learning/session-cost.py [transcript.jsonl]`.
  - 입력: 인자가 없으면 환경 변수 `CLAUDE_CODE_SESSION_ID`(Claude Code가 Bash에 넣어 줌, 2026-11-09 확인)로 `~/.claude/projects/e--Study-Inflearn/<id>.jsonl`을 읽는다. 서브에이전트는 `<id>/subagents/agent-*.jsonl`과 같은 이름의 `.meta.json`(`agentType`, `description`, `toolUseId`)에서 읽는다. 인자는 다른 폴더에서 돈 기록을 시험할 때 쓴다.
  - 범위: 메인 기록에서 이 스크립트를 부른 앞선 Bash 호출 중 결과가 `합계`로 시작한 마지막 호출 뒤부터 센다. 그런 호출이 없으면 세션 처음부터 센다. 실패한 시도 뒤에 다시 돌려도 범위는 그대로다. 서브에이전트는 `toolUseId`의 Agent 호출 시각으로 범위를 정한다.
  - 계산: 응답 하나를 API 메시지 id 하나로 한 번만 센다. 모델 이름에 `opus`가 있으면 Opus 비용이다. 가격표와 계산식은 `docs/research/token-audit-2026-11/scripts/common.py`의 `P`, `cost()`를 옮겨 쓴다($/MTok, 입력·출력·5분 쓰기·1시간 쓰기·캐시 읽기). 연구 폴더 코드를 불러 쓰지는 않는다. Opus 비중은 Opus 비용 ÷ 합계다.
  - 출력: 첫 줄 `합계 $X (메인 $A · 서브에이전트 $B) · Opus 비중 N.N%`. 이어서 Opus로 돈 호출마다 `- <agentType> "<description>" $C — 이유: <Opus-reason 또는 이유 없음>`을 쓴다. `Opus-reason`은 그 Agent 호출 입력의 prompt에서 읽는다. 메인이 Opus면 `- 메인 $A — 이유: 메인 모델`을 쓴다. R16 판정은 메인(준비 모드를 아는 쪽)이 한다.
  - 오류: 환경 변수나 기록 파일이 없으면 `비용 계산 불가: <이유>` 한 줄을 내고 종료 코드 1로 끝난다.
- **블라인드 범위**(G3·G7, 2026-11-09 사용자 결정): 준비 세션의 비용 보고에 Opus 비중이 나오므로, 강의 피드백 전에 사용자가 준비 모델을 짐작할 수 있다. 블라인드는 "강의 세션이 말하지 않는다"(R14)로만 지킨다.
- **멈춤 메시지 순서**: 강의 세션은 [피드백 질문 → 비용 → 모드 질문 → 커밋 확인]을, 준비 세션은 [비용 → 모드 질문 → 커밋 확인]을 한 메시지로 보낸다. 답을 파일에 적은 뒤 커밋한다. R2나 준비 세션 규칙 3번으로 일찍 멈춘 세션에는 이 멈춤이 없다.
- **기존 설계 2026-11-03 G1~G8과의 관계**: G1(검토까지 끝냄)·G2(퀴즈 초안 별도 파일)·G3(근거 목록)·G5(준비 안 된 회차면 강의 세션이 멈춤)·G6(강의 중 국소 수정)·G8(모든 트랙 같은 방식)의 동작은 바꾸지 않는다. G4(트랙 확정과 커밋 확인 말고는 묻지 않음)에는 R17의 예외 하나를 더한다. G7(사용자 확인 뒤 자기 파일만 커밋)은 커밋 대상에 `feedback.md`·`prep-mode.txt`를 더할 뿐이다.

Test seams: `session-cost.py`를 결과를 아는 테스트 SONNET 세션 기록(`E:\Study\model-test-2026-11-07\sonnet`에서 돈 세션)에 돌린다. 합계 $12.44 ±$0.01, Opus 비중 30.5% ±0.1%p가 나와야 한다(`docs/research/lesson-model-test-2026-11-07/result.md`). 범위 자르기와 R10 오류 줄은 작은 가짜 기록으로 본다. 규칙(R1~R6, R11~R18)은 다음 실제 준비·강의 세션의 기록과 `feedback.md`·`prep-mode.txt` 결과로 확인한다.

## Alternatives
- 아무것도 안 함: 준비 세션의 Opus 비중이 계속 94.6% 수준으로 남아 Opus 사용 한도를 쓴다.
- 준비 모드를 `docs/` 공유 파일 하나로 둠: 준비·강의 세션은 공유 파일을 고치지 못하므로 R11의 답을 적을 수 없다.
- 스킬 frontmatter `model`로 모델 고정: 그 턴에만 적용돼 세션 전체를 바꾸지 못한다.
- 준비 모델을 `status.md`에만 적음: 피드백을 받기 전에 준비 폴더가 지워져 값을 잃는다.

