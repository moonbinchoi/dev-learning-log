# Lesson Prep Session Implementation Plan
Status: approved

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Execution:** Native(superpowers:executing-plans). 사용자가 2026-11-04에 골랐다.

**Goal:** `/prepare-lesson <track>` 한 번으로 다음 회차의 검토된 레슨, 퀴즈 초안, 근거 목록을 별도 세션에서 만들고, 강의 세션은 그 결과를 확인한 뒤 바로 가르치게 한다.

**Architecture:** 코드를 더하지 않는다. 진입점 스킬 파일 하나와 규칙 문서 수정이 전부이고, 절차는 `docs/learning/operating-rules.md`에 둔다. 규칙이 문서에 들어갔는지는 절 단위 grep으로, 동작은 새 세션을 열어 실제 결과 파일과 `git` 상태로 확인한다.

**Tech Stack:** Claude Code skills(`.claude/skills/*/SKILL.md`), Markdown, Git Bash

**Spec:** `docs/design/2026-11-03-lesson-prep-session/spec.md`

## Global Constraints

- 명령은 저장소 루트(`E:/Study/Inflearn`)의 Git Bash에서 돌린다. `TMP=<session scratchpad>/lesson-prep-check`이고 Task 4 전에 `mkdir -p "$TMP"`로 만든다.
- 규칙 문서 산문은 한국어로, 기존 문서의 문체(짧은 평서문, 번호 목록)로 쓴다. `SKILL.md`와 `CLAUDE.md`는 영어로 쓴다.
- `operating-rules.md` "강의 세션 규칙"의 번호 1~7은 바꾸지 않는다. `CLAUDE.md:15`와 두 트랙 `NOTES.md`가 "규칙 7"을 번호로 가리킨다. 새 강의 세션 규칙은 2번의 하위 항목과 새 8번으로 넣는다.
- `lecture/docker-devcontainer/`, `docs/learning/track-design.md`, `lecture/TRACKS.md`는 고치지 않는다(spec "문서 변경 위치").
- `operating-rules.md`와 spring-backend `NOTES.md`를 고치기 전에 spring-backend 강의 세션이 돌고 있지 않은지 사용자에게 확인한다(`operating-rules.md` "공유 파일 변경").
- 커밋은 `CLAUDE.md` `## Git` 절차대로 한다. 파일 목록과 한국어 메시지를 보여 주고 확인을 받은 뒤 `git add -A -- <paths>`와 `git commit -m "<message>" -- <paths>`를 실행한다. 메시지 끝에는 세션이 안내받은 attribution 줄을 붙인다.
- 회차 태그는 이 구현에서 달지 않는다.

## Review Focus

- 회차 칸이 숫자가 아닌 회차(`마무리`): 준비 세션이 멈추지 않고 NN을 골라 `Open judgments`에 적어야 한다. 실제로 닿는 건 spring-backend 11회차 뒤다. → Task 1 Step 1에서 규칙 문구를 확인한다.
- 중간에 끊긴 준비(`Round`만 있고 `Review: passed`가 없는 폴더)를 다시 돌릴 때: 같은 폴더를 덮어쓰고 `Lesson`에 적힌 레슨 파일을 다시 쓴다. 새 레슨 번호가 생기면 안 된다. → Task 1 Step 1에서 규칙 문구를 확인한다.
- 강의 세션에서 사용자가 NN을 바꿀 때: 폴더 이름, `shop` 회차 브랜치 `lesson-NN`, 회차 태그가 함께 바뀌어야 한다. → Task 2 Step 1에서 규칙 문구를 확인한다.
- 퀴즈 문항 노출: 레슨, `reference/`, 준비 세션의 마지막 보고에 문항과 답이 나오면 안 된다. → Task 4 Step 4
- 다른 트랙 세션과 동시 실행: 준비 세션의 커밋이 다른 세션의 stage를 담으면 안 된다. → Task 4 Step 4의 `git show --name-only`

---

### Task 1: 준비 세션 진입점과 규칙
Covers: R1, R2, R3, R4, R5, R7, R10, R11, R13, R14, R19, R20, R21

**Files:**
- Create: `.claude/skills/prepare-lesson/SKILL.md`
- Modify: `docs/learning/operating-rules.md` ("강의 세션 규칙" 절 뒤, "레슨 설계" 앞에 새 절)
- Modify: `CLAUDE.md` (`## Lessons`)

**Interfaces:**
- Produces: 슬래시 명령 `/prepare-lesson <track>`; `operating-rules.md`의 `## 준비 세션 규칙` 절과 그 안의 "다음 회차 읽기" 규칙(Task 2가 이 이름으로 가리킨다); 준비 폴더 `lecture/<track>/prep/NN/`의 세 파일 형식(Task 2·3·4가 쓴다).

- [ ] **Step 1: 실패하는 검사를 돌린다**

```bash
test -f .claude/skills/prepare-lesson/SKILL.md || echo "MISSING skill"
grep -q "/prepare-lesson" CLAUDE.md || echo "MISSING CLAUDE.md line"
S=$(sed -n '/^## 준비 세션 규칙/,/^## 레슨 설계/p' docs/learning/operating-rules.md)
for k in "/prepare-lesson" "다음 회차 읽기" "0회차 준비" "다음은 X회차" "Round" "Lesson" "Review: passed" "Open judgments" "→ 선택:" "quiz-draft.md" "sources.md" "lesson-review.md" "## Git" "마무리"; do printf '%s' "$S" | grep -qF -- "$k" || echo "MISSING $k"; done
```

Expected: `MISSING` 줄이 16개(스킬, `CLAUDE.md`, 키워드 14개) 나온다.

- [ ] **Step 2: `.claude/skills/prepare-lesson/SKILL.md`를 만든다**

frontmatter는 `name: prepare-lesson`, `description`(다음 회차를 별도 세션에서 준비한다는 한 문장), `disable-model-invocation: true`, `argument-hint: <track>`이다. 본문은 두 줄이다. `docs/learning/operating-rules.md`의 "준비 세션 규칙"을 따르라는 줄과 `Track: $ARGUMENTS` 줄이다. 절차는 본문에 쓰지 않는다.

- [ ] **Step 3: `operating-rules.md`에 `## 준비 세션 규칙` 절을 쓴다**

번호 목록으로 쓰고 아래 내용을 모두 담는다. 괄호 안은 근거 요구사항이고 문서에는 쓰지 않는다.
1. 진입은 `/prepare-lesson <track>`이다. 인자가 없으면 `TRACKS.md`의 "진행 중" 트랙을 보여 주고 묻는다. 그 밖에는 커밋 확인 말고 묻지 않는다(R10).
2. **다음 회차 읽기**: spec Design "다음 회차 읽기"의 세 줄을 그대로 옮긴다(`0회차 준비` → `0`; `N회차 완료`와 `다음은 X회차` → X; 굵게 표시·괄호 안·뒤 설명 무시; 두 예시). 강의 세션도 이 규칙을 쓴다고 적는다.
3. 멈춤 조건: 트랙이 `TRACKS.md`에 없거나 "진행 중"이 아니거나, X를 읽지 못하거나, X가 커리큘럼 표 회차 칸에 없으면 파일을 쓰지 않고 이유를 알리고 멈춘다(R13).
4. 준비 폴더: `lecture/<track>/prep/NN/`. X가 숫자면 NN은 X의 두 자리 표기다. X가 숫자가 아니면(예: `마무리`) 커리큘럼 표와 앞 회차를 보고 NN을 정하고 `Open judgments`에 적는다. 다른 `prep/*/`와 기존 회차 태그의 번호와 겹치지 않게 한다(R21). 회차 X의 준비 폴더는 `status.md`의 `Round`가 X인 폴더다. 그 폴더에 `Review: passed`가 있으면 쓰지 않고 그 `status.md` 경로를 적어 알리고 멈춘다. 없으면 덮어쓰고, `Lesson`이 적혀 있으면 그 레슨 파일을 다시 쓴다(R14).
5. 순서: 멈춤 조건 확인 → `status.md`에 `Round`를 먼저 적는다 → 가르칠 내용을 커리큘럼 표, "현재 위치"에 넘겨 둔 내용, `learning-records/`(다른 트랙 것은 규칙 4대로 읽기만)로 정한다 → 자료 읽기, 레슨 작성, 검토는 "강의 세션의 위임" 표와 [lesson-review.md](lesson-review.md)를 그대로 쓴다 → `status.md`에 결과를 적는다 → 커밋한다(R1).
6. `status.md` 형식: spec Design의 예시 블록을 그대로 넣는다. 검토 지적 수정까지 끝나면 `Lesson`과 `Review: passed`를 적는다(R2). 통과하지 못하면 `Review: passed`를 적지 않고 커밋 확인 때 그렇게 보고한다(R3). 판단이 애매하면 `- <질문> → 선택: <값>` 줄을 `Open judgments`에 적고 이어 간다(R11).
7. `quiz-draft.md`: 회상 퀴즈와 면접 질문 2~3개를 모범 답과 함께 쓴다. 트랙 `NOTES.md`가 회상 퀴즈 자리에 진단 질문을 정한 회차는 진단 질문을, 회상 퀴즈를 생략하는 첫 회차는 면접 질문만 쓴다. 형식은 `## 회상 퀴즈`(또는 `## 진단 질문`), `## 면접 질문` 절 아래 `- Q: <문항>` 줄과 그 밑의 `  - 모범 답: <답>` 줄이다(R4). 레슨, `reference/`, 어느 문서에서도 링크하지 않고, 채팅 보고에 문항과 답을 싣지 않는다(R5).
8. `sources.md`: 레슨의 `<h2>` 절마다 한 줄 이상 `<절 제목> | <교재 경로>:<시작>-<끝>` 또는 `<절 제목> | <공식 문서 URL>`. 레슨에 옮긴 부분의 근거만 적는다(R7).
9. `NOTES.md`와 `TRACKS.md`는 고치지 않는다. 쓰기는 자기 트랙 폴더에서만 한다. 절차는 트랙마다 같고, 트랙마다 다른 값은 그 트랙 `NOTES.md`의 커리큘럼 표와 "현재 위치"에서 읽는다(R20).
10. 끝에 `CLAUDE.md` `## Git` 절차로 그 세션이 만들거나 고친 파일만 커밋한다. 사용자가 거절하면 커밋하지 않고 끝낸다. 회차 태그는 달지 않는다(R19).

- [ ] **Step 4: `CLAUDE.md` `## Lessons`에 한 줄을 더한다**

`Prepare each lesson in its own session with /prepare-lesson <track> before teaching it.`의 뜻을 한 문장으로 쓴다. 기존 "Before teaching ... follow `docs/learning/operating-rules.md`" 문장 뒤에 둔다.

- [ ] **Step 5: 검사를 다시 돌린다**

Step 1의 명령. Expected: 출력 없음.

- [ ] **Step 6: 커밋한다**

경로: `.claude/skills/prepare-lesson/SKILL.md`, `docs/learning/operating-rules.md`, `CLAUDE.md`. 메시지 예: `강의 준비 세션 진입점과 준비 세션 규칙을 더한다`.

### Task 2: 강의 세션의 확인과 국소 수정 규칙
Covers: R12, R15, R16, R17, R18, R22

**Files:**
- Modify: `docs/learning/operating-rules.md` ("강의 세션 규칙" 2번 하위 항목, 7번 정리 대상, 새 8번, "강의 세션의 위임"의 "메인이 직접 하는 위임 예외")

**Interfaces:**
- Consumes: Task 1의 "다음 회차 읽기" 규칙과 `status.md` 형식(`Round`, `Lesson`, `Review: passed`, `Open judgments`).

- [ ] **Step 1: 실패하는 검사를 돌린다**

```bash
L=$(sed -n '/^## 강의 세션 규칙/,/^## 준비 세션 규칙/p' docs/learning/operating-rules.md)
for k in "/prepare-lesson <track>" "→ 결정:" "Review: passed" "회차 브랜치" "한 절" "prep/NN/" "다시 검토하지 않는다"; do printf '%s' "$L" | grep -qF -- "$k" || echo "MISSING $k"; done
printf '%s' "$L" | grep -c '^[0-9]\.' 
sed -n '/^메인이 직접 하는 위임 예외/,/^트랙/p' docs/learning/operating-rules.md | grep -qF "준비 세션" || echo "MISSING 위임 예외"
```

Expected: `MISSING` 7줄, 번호 줄 수 `7`, `MISSING 위임 예외`.

- [ ] **Step 2: 2번 아래에 확인 규칙을 하위 항목으로 쓴다**

순서대로: 준비 세션 규칙의 "다음 회차 읽기"로 X를 읽고 `Round`가 X인 `prep/*/`를 찾는다 → 폴더나 `Review: passed`나 `Lesson`의 파일이 없으면 알리고 `/prepare-lesson <track>`을 먼저 돌리라고 안내하고 멈춘다. 레슨을 만들거나 검토하지 않는다(R15) → `Open judgments`에서 `→ 결정:`이 없는 줄마다 사용자에게 묻고 줄 끝에 `→ 결정: <값>`을 붙인다. 결정에 따른 레슨 수정은 8번의 범위를 따른다(R12) → NN 결정이 바뀌면 폴더 이름, `shop` 회차 브랜치 `lesson-NN`, 회차 태그 `<track>/lesson-NN`에 그 값을 쓴다(R22) → 레슨은 다시 검토하지 않는다(R16).

- [ ] **Step 3: 7번 정리 대상에 준비 폴더를 더한다**

"그 회차의 `prep/NN/` 폴더를 지워 회차 마무리 커밋에 담는다"를 정리 대상 목록에 한 항목으로 더한다.

- [ ] **Step 4: 새 8번을 쓴다**

강의 중 레슨의 오류나 빠진 내용이 드러나면, 고칠 범위가 한 절 이하면 그 자리에서 고친다(R17). 한 절을 넘으면 고치지 않고 채팅으로 문제를 설명한 뒤 `NOTES.md` "현재 위치"에 다음 회차로 넘길 내용으로 적는다(R18).

- [ ] **Step 5: 위임 예외 항목을 고친다**

"조사 직후 같은 맥락에서 하는 회차 레슨 작성. 그 레슨의 검토 지적 수정과 용어집 갱신도 포함한다."를 준비 세션 기준으로 바꾼다: 준비 세션에서 조사 직후 같은 맥락에서 하는 레슨 작성과 검토 지적 수정, 용어집 갱신. 강의 세션의 8번 국소 수정을 같은 항목에 더한다.

- [ ] **Step 6: 검사를 다시 돌린다**

Step 1의 명령. Expected: `MISSING` 없음, 번호 줄 수 `8`.

- [ ] **Step 7: 커밋한다**

경로: `docs/learning/operating-rules.md`. 메시지 예: `강의 세션이 준비 결과를 확인하고 레슨을 국소 수정하게 한다`.

### Task 3: spring-backend 회차 순서
Covers: R6, R8, R9

**Files:**
- Modify: `lecture/spring-backend/NOTES.md:6-7` (1·2단계), `:14` (9단계), `:42-50` ("회차 마무리")

**Interfaces:**
- Consumes: Task 1의 `quiz-draft.md`·`sources.md` 형식, Task 2의 강의 세션 규칙 2번 하위 항목과 7번.

- [ ] **Step 1: 실패하는 검사를 돌린다**

```bash
M=$(sed -n '/^## 강의 방식/,/^### 리마인드/p' lecture/spring-backend/NOTES.md)
for k in "quiz-draft.md" "sources.md" "/prepare-lesson"; do printf '%s' "$M" | grep -qF -- "$k" || echo "MISSING $k"; done
sed -n '/^## 회차 마무리/,/^## 교재/p' lecture/spring-backend/NOTES.md | grep -qF "prep/NN/" || echo "MISSING 마무리"
```

Expected: `MISSING` 4줄.

- [ ] **Step 2: 1·2·9단계를 고친다**

- 1단계: 회상 퀴즈(리마인드 회차는 진단 질문)는 준비 폴더의 `quiz-draft.md` 문항을 그대로 또는 고쳐서 낸다(R6). 첫 회차 생략과 앞 회차 요약 문장은 그대로 둔다.
- 2단계: 레슨은 `/prepare-lesson spring-backend`가 만들고 검토까지 끝낸다. 강의 세션은 `operating-rules.md` 강의 세션 규칙 2번의 확인을 거쳐 연다. 레슨의 절 구성 문장("동작 원리"가 맨 앞 등)은 그대로 둔다. 준비 세션이 이 문장을 읽고 레슨을 만들기 때문이다.
- 강의 중 질문에 답할 때는 `sources.md`에서 주제 줄을 찾아 그 범위나 URL부터 읽고, 모자라면 같은 파일 안에서 넓혀 읽는다. 주제가 목록에 없으면 없다고 말하고 `sources.md`에 적힌 교재 파일과 공식 문서 페이지 안에서만 찾는다(R8, R9). 회차 순서 목록 뒤 "강의 방식" 항목으로 둔다.
- 9단계: 면접 질문도 `quiz-draft.md`의 문항을 그대로 또는 고쳐서 낸다(R6).

- [ ] **Step 3: "회차 마무리" 3단계에 준비 폴더 삭제를 더한다**

"`operating-rules.md` 강의 세션 규칙 7에 따라 트랙 마크다운을 정리하고 그 회차의 `prep/NN/`을 지운다."

- [ ] **Step 4: 검사를 다시 돌린다**

Step 1의 명령. Expected: 출력 없음.

- [ ] **Step 5: 커밋한다**

경로: `lecture/spring-backend/NOTES.md`. 메시지 예: `spring-backend 회차 순서가 준비 폴더를 쓰게 한다`.

### Task 4: 새 세션으로 동작 확인과 2회차 준비
Covers: R1, R2, R3, R4, R5, R7, R13, R14, R15, R19

**Files:**
- Create (준비 세션이 만든다): `lecture/spring-backend/prep/02/status.md`, `quiz-draft.md`, `sources.md`, `lecture/spring-backend/lessons/0002-*.html`
- Modify: `lecture/spring-backend/NOTES.md:87` (2회차 회상 퀴즈 줄 삭제)

**Interfaces:**
- Consumes: Task 1~3의 규칙 전부.

스텝 순서가 곧 시험 조건이다. 1은 준비 전에, 3은 2회차 준비 후에만 성립한다. 각 `claude -p` 실행이 슬래시 명령을 실행하지 못하면, 같은 입력을 새 대화형 세션에 쳐서 같은 기준으로 본다.

- [ ] **Step 1: R15 — 준비 전에 강의 세션을 연다**

```bash
claude -p "/mattpocock-skills:teach spring-backend" > "$TMP/r15.txt"; grep -F "/prepare-lesson spring-backend" "$TMP/r15.txt"; git status --short lecture/
```

Expected: 안내 줄이 한 줄 이상 나오고, `git status` 출력은 없다.

- [ ] **Step 2: R13 — 완료된 트랙을 준비한다**

```bash
claude -p "/prepare-lesson docker-devcontainer" > "$TMP/r13.txt"; cat "$TMP/r13.txt"; git status --short lecture/
```

Expected: 트랙이 "진행 중"이 아니라서 멈춘다는 보고가 나오고, `git status` 출력은 없다.

- [ ] **Step 3: 사용자가 2회차를 준비한다**

사용자에게 새 대화형 세션에서 `/prepare-lesson spring-backend`를 치고, 끝의 커밋 확인을 승인해 달라고 요청한다. 레슨 검토에 서브에이전트가 돌기 때문에 이 단계는 헤드리스로 돌리지 않는다. 끝나면 그 세션의 마지막 보고를 받는다.

- [ ] **Step 4: 준비 결과를 확인한다**

```bash
P=lecture/spring-backend/prep/02
grep -x "Round: 2" $P/status.md && grep -x "Review: passed" $P/status.md
LES=lecture/spring-backend/$(sed -n 's/^Lesson: //p' $P/status.md); test -f "$LES" && echo LESSON_OK
sed -n '/^## 면접 질문/,/^## /p' $P/quiz-draft.md | grep -c '^- Q:'
grep -E -v '^.+ \| (courses/.+\.md:[0-9]+-[0-9]+|https?://\S+)$' $P/sources.md | grep -v '^#' | grep -v '^$'
grep -o '<h2[^>]*>[^<]*' "$LES" | sed 's/<h2[^>]*>//' | while read -r h; do grep -qF -- "$h" $P/sources.md || echo "NO SOURCE: $h"; done
git grep -n "quiz-draft" -- lecture/spring-backend/lessons lecture/spring-backend/reference
git show --name-only --format= HEAD | grep -v '^lecture/spring-backend/'
git tag -l 'spring-backend/*'
```

Expected: `Round: 2`, `Review: passed`, `LESSON_OK`, 면접 질문 수 `2` 또는 `3`. 그 밖의 명령은 출력이 없다. `sources.md`의 형식 위반 줄, 출처 없는 절, 퀴즈 링크, 트랙 밖 커밋 파일, 회차 태그가 모두 없다는 뜻이다. Step 3의 마지막 보고에 `quiz-draft.md`의 `- Q:` 문항이 들어 있지 않은지 눈으로 본다(R5).

- [ ] **Step 5: R14 — 같은 회차를 다시 준비한다**

```bash
claude -p "/prepare-lesson spring-backend" > "$TMP/r14.txt"; cat "$TMP/r14.txt"; git status --short lecture/
```

Expected: 보고에 `prep/02/status.md` 경로가 있고 이미 통과해 멈췄다고 말한다. `git status` 출력은 없다.

- [ ] **Step 6: 2회차 회상 퀴즈 줄을 옮겼는지 보고 지운다**

`NOTES.md:87`의 네 문항(검증 실패 때 리다이렉트하지 않는 이유, `Item`의 `@NotBlank`, 타입 오류와 `BindingResult` 유무, `addAttribute` 값의 위치)이 `prep/02/quiz-draft.md`에 있는지 읽어 확인한다. 빠진 문항이 있으면 사용자에게 알리고 그 문항을 `quiz-draft.md`에 더한다. 그 뒤 `NOTES.md`의 그 줄을 지운다.

```bash
grep -c "2회차 회상 퀴즈" lecture/spring-backend/NOTES.md
```

Expected: `0`

- [ ] **Step 7: 커밋한다**

경로: `lecture/spring-backend/NOTES.md`와 Step 6에서 고쳤다면 `lecture/spring-backend/prep/02/quiz-draft.md`. 메시지 예: `2회차 회상 퀴즈를 준비 폴더로 옮긴다`.

## Final verification

Task 4 Step 3에서 사용자가 `/prepare-lesson spring-backend`를 실행하고 커밋을 승인한 뒤, 같은 상태에서 돌린다.

```bash
P=lecture/spring-backend/prep/02 && grep -x "Review: passed" $P/status.md && test -f "lecture/spring-backend/$(sed -n 's/^Lesson: //p' $P/status.md)" && test -s $P/quiz-draft.md && test -s $P/sources.md && ! git grep -q "quiz-draft" -- lecture/spring-backend/lessons lecture/spring-backend/reference && git log -1 --format=%s -- $P/status.md && claude -p "/prepare-lesson spring-backend" | grep -c "prep/02/status.md" && test -z "$(git status --short lecture/)" && echo PASS
```

Expected:

```
Review: passed
<준비 세션 커밋 메시지 한 줄>
1
PASS
```

`1`은 다시 준비하려 할 때 멈춤 보고에 `prep/02/status.md`가 나온 줄 수다. 보고 문구에 따라 1보다 클 수 있다.

## After implementation

- 이 변경에는 원격과 PR이 없다. mattpocock-skills:pr로 PR 본문을 쓰되 파일로 만들지 않고 사용자에게 보여 준다. Evidence에 Final verification 출력을 넣고 `docs/design/2026-11-03-lesson-prep-session`을 링크한다.
- 사용자가 결과를 받아들이면 `intent.md`, `spec.md`, `plan.md`를 `Status: implemented`로 바꾸고 `CLAUDE.md` `## Git` 절차로 커밋한다.
- 구현이 플랜과 달라지면 같은 커밋에서 `plan.md`를 고친다.
