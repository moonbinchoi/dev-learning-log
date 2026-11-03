# Spec: 프로젝트 에이전트 구성 재설계

Source: [intent.md](intent.md) (moonbinchoi)
Status: accepted (2026-10-20)
Applied: `~/.claude/rules/orchestration.md`, `~/.claude/agents/*.md`, 전역 CLAUDE.md 작성 규칙, `~/.claude/knowledge/local/claude-workflow/delegation-cost-evidence.md`, `~/.claude/knowledge/local/claude-code/claude-code-mechanics.md`

## Requirements

`← ` 뒤는 그 요구사항이 나온 intent 항목이다.

- R1. `docs/learning/operating-rules.md` "강의 세션의 위임" 절이 Design 1의 글과 같다. `docs/learning/`, `.claude/`, `CLAUDE.md`에서 `investigator|architect|editor|ORCHESTRATION|grader`를 대소문자 무시로 grep하면 0건이다. ← P1, P2, O1, O3
- R2. `docs/learning/operating-rules.md:74`의 첫 문장("설명·질의응답 답변에는 `Delegation exception` 줄을 쓰지 않는다.")이 없고, 둘째 문장은 남아 있다. ← P4
- R3. `docs/learning/lesson-review.md:7`의 담당이 `reviewer`다. ← P1
- R4. `docs/learning/grading.md`가 Design 2의 글과 같다. ← P2, C1
- R5. `.claude/agents/grader.md`가 없다. ← P2, O2
- R6. `.claude/agents/source-reader.md`와 `.claude/agents/visual-reviewer.md`가 Design 3의 글과 같다. ← P3, C2, C4, O2
- R7. hook이 Design 4대로 동작하고, `node .claude/hooks/practice-guard.test.js`가 `practice-guard: ok`를 출력한다. ← P5, O4
- R8. `docs/superpowers/` 폴더가 없다(유일한 파일 `specs/2026-10-17-visual-reviewer-design.md`는 참조하는 곳이 없다). ← P1, C6
- R9. `docs/research/devcontainer-claude.md`가 바뀌지 않는다. `docs/learning/track-design.md:47`이 이 파일을 참조하므로 지우지 않는다. ← C6

## Design

### 1. 위임 절 (R1)

```md
## 강의 세션의 위임

이 절은 전역 오케스트레이션 규칙과 다른 점만 적는다. `source-reader`와 `visual-reviewer`는 `.claude/agents/`에 있는 이 프로젝트 전용 역할이다.

| 작업 | 담당 |
|---|---|
| 회차 1차 자료 읽기(강좌 장 md, 웹 공식 문서) | source-reader. 메인은 반환된 줄 범위·URL 중 레슨에 옮길 부분만 직접 읽는다. 미확인 항목이나 반환에 없는 사실은 직접 찾지 말고 source-reader를 재개해 묻는다. |
| 강좌 전체 분석([course-intake.md](course-intake.md)) | source-reader를 장 묶음별로 나눠 병렬로 돌린다. |
| 연습 채점, 예제 코드의 ECC 대조 | reviewer. 브리프에 [grading.md](grading.md), 채점할 파일 경로(또는 diff), 그 회차의 강좌 자료 경로를 준다. 사용자와 리뷰 대화는 메인이 그 결과와 diff로 한다. |
| 다른 트랙 learning-records 대조 | explorer. 브리프에 이번 회차 후보 개념 목록을 주고 `개념 \| 기록 경로:줄 \| 근거 인용` 형식으로 후보만 받는다. 이미 증명됐는지는 메인이 판단한다. |
| 레슨 검토 | [lesson-review.md](lesson-review.md) 순서대로. 내용은 reviewer, 시각은 visual-reviewer. 사용자에게 열기 전에 한다. |

메인이 직접 하는 위임 예외:
(지금 목록 3줄 그대로)

트랙 `NOTES.md`에는 이 절과 다른 트랙 고유의 위임 규칙만 적는다.
```

지운 행과 그 일을 맡는 전역 규칙(검토자가 빠진 일이 없는지 확인하는 용도):

| 지운 행 | 맡는 전역 규칙 |
|---|---|
| 짧은 사실 확인·위치 찾기 → investigator | 단일 조회는 메인, 대량 위치 찾기는 `explorer`, 웹은 `researcher`. |
| 빌드·테스트 → worker | 장황한 출력을 내는 실행은 `worker`. 작업 폴더는 브리프 Context에 들어간다. |
| 형식 변환·일괄 수정 → editor | `worker`. 쓰기 범위는 강의 세션 규칙 3번이 정한다. |

### 2. `docs/learning/grading.md` (R4)

```md
# Grading criteria

Pass this file to `reviewer` when grading a practice exercise or checking lesson example code. The brief also gives the files or diff to grade and the course material for that lesson.

- Judge against two tiers: first the course material in the brief, then the ECC files that [ecc-map.md](ecc-map.md) lists for the topic. Where they differ, judge by the course approach and note ECC's approach separately under "실무에서는".
- Report only defects that affect correctness, the exercise's requirements, or the concept the lesson taught.
- Give a corrected example only when the brief asks, and keep it minimal.

## Report

- First line: DONE, PARTIAL, or BLOCKED.
- Verdict line: Pass or Needs work.
- One line per defect: `path:line — defect — basis (criterion path:line)`.
- "실무에서는" notes, then "Unverified".
- Stay under 20 lines unless the brief sets another cap.
```

### 3. 프로젝트 에이전트 (R6)

남는 이유(O2):

| 에이전트 | 전역 에이전트로 안 되는 이유 |
|---|---|
| source-reader | 매 회차와 강좌 도입마다 같은 지시로 띄운다(근거 1). "강좌 순서·용어를 따르고 줄 범위를 반환한다"는 계약을 가진 전역 에이전트가 없다. `explorer`는 판단하지 않고, `researcher`는 작업 공간 밖만 본다. |
| visual-reviewer | 스크립트+이미지 절차로 심은 결함 6/6을 잡았고 이전 방식은 0/6이었다(근거 4). 이 절차를 가진 전역 에이전트가 없다. |

`source-reader.md`:

```md
---
name: source-reader
description: Reads primary lesson sources (course chapter markdown under courses/*/docs/, official web docs) and returns the points a lesson needs, each with its source line range or URL. Use when preparing a lesson or analyzing a course chapter by chapter.
model: sonnet
effort: medium
tools: Read, Grep, Glob, WebSearch, WebFetch
maxTurns: 30
omitClaudeMd: true
---

Write everything in English: your reader is the agent that dispatched you, not the user. Quote course terms and sentences in their original Korean.

You read sources. Extract what the main session needs to write and teach the lesson the brief names.

- Read course material only from `courses/<course>/docs/*.md`. Read the official docs the brief names before any other web page.
- Write only what the sources state, in the course's order, terms, and examples.
- When a judgment outside the brief is needed, stop and report BLOCKED with the question.
- Done when every topic in the brief has its points with sources, or is listed under "Unverified".

## Report

Use the format the brief defines; otherwise:

- First line: DONE, PARTIAL, or BLOCKED.
- Each point as `point — source`: `path:start-end` for course material, the URL for web pages.
- What the sources did not confirm, under "Unverified".
- Stay under 30 lines unless the brief sets another cap.
```

`visual-reviewer.md`:

```md
---
name: visual-reviewer
description: Runs the visual review of a lesson HTML, step 2 of docs/learning/lesson-review.md: runs the layout, link, and render scripts, views the chosen section images, and reports problems with location and evidence. Use after the content review, before the lesson is shown to the user.
model: sonnet
effort: medium
tools: Read, Bash, Glob
maxTurns: 20
omitClaudeMd: true
---

Write everything in English: your reader is the agent that dispatched you, not the user. Keep the fixed labels of lesson-review.md as written.

You review visuals. Follow section "2. 시각 검토" of the lesson-review.md the brief gives.

- Use Bash only to run that section's scripts.
- Done when every chosen image has its line, or the image list is returned for splitting (that section's step 4).

## Report

- First line: DONE, PARTIAL, or BLOCKED.
- Then the format of lesson-review.md section "2. 시각 검토".
```

### 4. hook (R7)

- 파일: `.claude/hooks/practice-guard.js`, `.claude/hooks/practice-guard.test.js`. `.claude/settings.json`의 hook 경로도 이 이름을 가리킨다.
- Bash/PowerShell 판정: 명령 조각에 `projects/`(또는 `./projects/`; `\` 구분자 포함)로 시작하는 토큰이 있거나 저장소 실습 폴더의 절대경로(`E:/Study/Inflearn/projects`, `E:\Study\Inflearn\projects`, `/e/Study/Inflearn/projects`)가 들어 있을 때만, 읽기 명령을 막는다. 대소문자는 무시한다.
- 거부 메시지: "practice files under projects/ are graded by `reviewer` with docs/learning/grading.md, even a single file. Dispatch reviewer with grading.md, the file paths, and the course material; talk the review through with the user from its result and git diff. Commands starting with git or docker pass; run them as separate calls."
- 테스트에 추가하는 경우:
  - 막지 않음: `cat ~/.claude/projects/e--Study-Inflearn/memory/MEMORY.md`, `cat C:/Users/x/.claude/projects/y.md`
  - 막음: `cat E:/Study/Inflearn/projects/shop/App.java`, `cat ./projects/shop/App.java`
- 기존 테스트 줄은 모두 그대로 통과한다.

## How each constraint in the intent is met

| 제약 | 충족 방법 |
|---|---|
| C1 품질 | 채점 기준은 `grading.md`로 그대로 옮기고, 채점은 grader(sonnet)와 같거나 더 큰 모델을 쓸 수 있는 `reviewer`가 맡는다(R4, R5). source-reader와 visual-reviewer의 절차는 바꾸지 않는다(R6). 측정하지 않은 위험은 우려 사항 1. |
| C2 비용 | 에이전트 정의를 영어로 쓴다(근거 4, R6). 위임 표에서 전역 규칙과 겹치는 행을 지운다(R1). |
| C3 전역 수정 금지 | 전역 문제는 우려 사항 6-8로 보고만 한다. |
| C4 언어 | 에이전트 정의와 `grading.md`는 영어(R4, R6). 사용자가 읽는 `operating-rules.md`와 `lesson-review.md`는 한국어(R1-R3). |
| C5 보호 경로 | `.claude/` 아래 파일(R5-R7)은 메인 세션이 쓴다(근거 3). |
| C6 기록 문서 | 참조가 없는 것은 지우고(R8), 참조가 있는 것은 그대로 둔다(R9). |

## Open questions from the intent

- 없음(intent에 미결 질문이 없다).

## Areas of concern

모두 담당은 moonbinchoi다. 1-5는 이 spec이 사용자와 합의 없이 정한 것이고, 6-8은 C3에 따라 보고만 하는 전역 문제다.

1. **채점 품질은 측정하지 않았다.** grader 대신 reviewer와 grading.md로 채점할 때의 품질은 A/B 없이 받아들였다. 채점이 이전보다 못하다고 느껴지면 결함을 심은 3회 A/B로 확인한다.
2. **hook 이름을 `practice-guard`로 바꾼다.** grader가 없어지면 `grader-guard`라는 이름이 하는 일과 맞지 않는다. 이름을 유지하면 `settings.json`은 바뀌지 않는다.
3. **`grading.md`는 영어로 쓰고 판정 줄을 `Pass/Needs work`로 둔다.** 에이전트만 읽는 파일이라 C4를 따른다. 사용자에게는 메인이 한국어로 전한다.
4. **채점 행의 브리프에 "그 회차의 강좌 자료 경로"를 넣는다.** grader.md가 "브리프가 준 강좌 자료"를 1차 기준으로 삼았기 때문이다.
5. **source-reader의 "지시 범위를 벗어나는 판단은 멈추고 반환"을 BLOCKED 보고로 바꾼다.** 전역 보고 형식의 상태 줄에 맞추려는 것이다.
6. **전역 `orchestration.md`의 "Send every review to `reviewer`"에는 프로젝트 전용 검토 에이전트의 예외가 없다.** visual-reviewer가 이 규칙과 충돌하는 것처럼 읽힌다. 예: "unless project instructions name another agent for that review".
7. **전역 `reviewer.md`, `explorer.md`, `analyst.md`의 "Use Bash for read-only commands"는 강제되지 않는 산문 제한이다**(근거 4).
8. **전역 `orchestration.md`의 "Jev shadow log"는 모델을 아직 기존 규칙으로 고르게 한다.** dispatch마다 Jev 추천을 따르려는 계획과 다르다. 전환 전까지 채점은 `reviewer` 기본값(opus/high)으로 돈다.

## 근거

1. https://code.claude.com/docs/en/sub-agents (2026-10-20): "Define a custom subagent when you keep spawning the same kind of worker with the same instructions."
2. superpowers 7.0.0 `RELEASE-NOTES.md:349`(로컬 확인): 유일한 named agent `code-reviewer`를 지우고 `general-purpose`에 프롬프트 템플릿을 주는 방식으로 바꿨다. 이유는 다른 검토 dispatch와의 일관성이다. grader를 기준 파일로 바꾸는 R4-R5의 선례다.
3. https://code.claude.com/docs/en/permission-modes#protected-paths: `.claude/` 쓰기는 `permissions.allow` 규칙으로 미리 승인되지 않는다.
4. `~/.claude/knowledge/local/claude-workflow/delegation-cost-evidence.md`와 그 출처 기록: 산문 제한 미강제, 한국어 토큰 약 1.57배, visual-reviewer 6/6 대 0/6.
