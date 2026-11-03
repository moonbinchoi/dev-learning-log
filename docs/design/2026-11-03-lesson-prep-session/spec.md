# Spec: 강의 준비를 별도 세션으로 분리
From: intent.md · Status: approved

## Requirements
- R1 (← G1). WHEN 사용자가 `/prepare-lesson <track>`을 실행하고 세션이 검토 통과로 끝나면 THE SYSTEM SHALL 다음 회차 X(Design "다음 회차 읽기")의 1차 자료를 읽어 만든 레슨 HTML(도식 포함)이 `lesson-review.md`의 내용·시각 검토를 통과하고 지적 수정까지 끝난 상태로 있게 한다.
- R2 (← G1). WHEN 검토 지적 수정이 끝나면 THE SYSTEM SHALL `prep/NN/status.md`에 `Review: passed`와 레슨 경로를 적는다.
- R3 (← G1). IF 검토가 통과하지 못하면 THEN THE SYSTEM SHALL `Review: passed`를 적지 않고, 커밋 확인 때 통과하지 못했다고 보고한다. 세션이 중간에 끊기면 `Review: passed`가 없는 채로 남고, 다음 준비 세션이 R14로 덮어쓴다.
- R4 (← G2). THE SYSTEM SHALL 준비 세션이 `prep/NN/quiz-draft.md`에 회상 퀴즈와 면접 질문 2~3개를 모범 답과 함께 남기게 한다. 트랙 `NOTES.md`가 회상 퀴즈 자리에 진단 질문을 정한 회차(spring-backend의 리마인드 회차, 3~5개)는 진단 질문을 남기고, 회상 퀴즈를 생략하는 첫 회차는 면접 질문만 남긴다. 개수는 `NOTES.md` 회차 순서의 기존 수치다.
- R5 (← G2). THE SYSTEM SHALL 퀴즈 초안을 레슨 HTML과 `reference/`에 넣거나 어느 문서에서도 링크하지 않고, 준비 세션의 채팅 보고에도 문항과 답을 싣지 않는다.
- R6 (← G2). WHEN 강의 세션이 회상 퀴즈나 면접 질문 단계에 이르면 THE SYSTEM SHALL `quiz-draft.md`의 문항을 그대로 또는 고쳐서 낸다.
- R7 (← G3). THE SYSTEM SHALL 준비 세션이 `prep/NN/sources.md`에 레슨의 절마다 한 줄 이상 `절 제목 | 교재 경로:시작-끝줄 또는 공식 문서 URL`을 남기게 한다.
- R8 (← G3). WHEN 강의 중 사용자가 질문하면 THE SYSTEM SHALL `sources.md`에서 그 주제의 줄을 찾아 그 줄 범위나 URL부터 읽고 답한다. 범위가 답에 모자라면 같은 파일 안에서 앞뒤로 넓혀 읽는다.
- R9 (← G3). IF 질문의 주제가 `sources.md`에 없으면 THEN THE SYSTEM SHALL 목록에 없다고 말하고, `sources.md`에 적힌 교재 파일과 공식 문서 페이지 안에서 그 주제 부분만 찾아 읽어 답한다.
- R10 (← G4). THE SYSTEM SHALL 준비 세션이 트랙 확정(인자가 없을 때)과 커밋 확인 외에는 사용자에게 묻지 않고 끝까지 돌게 한다.
- R11 (← G4). WHEN 준비 중 판단이 애매한 점이 생기면 THE SYSTEM SHALL 질문과 임시로 고른 선택을 `status.md`의 `Open judgments`에 적고 준비를 이어 간다.
- R12 (← G4). WHEN 강의 세션이 시작되면 THE SYSTEM SHALL `Open judgments`에서 결정이 없는 항목마다 사용자에게 질문해 결정을 받고, 그 줄 끝에 `→ 결정: <값>`을 붙인다. 결정에 따른 레슨 수정은 R17·R18의 범위 규칙을 따른다.
- R13 (← G4; 제약 1). IF 트랙이 `TRACKS.md`에 없거나 상태가 "진행 중"이 아니거나, `NOTES.md` "현재 위치" 첫 항목에서 다음 회차 X를 읽지 못하거나, X가 커리큘럼 표의 회차 칸에 없으면 THEN THE SYSTEM SHALL 준비 세션이 파일을 쓰지 않고 그 사실을 알리고 멈추게 한다. X를 읽는 규칙은 Design "다음 회차 읽기"에 있다.
- R14 (← G4; 제약 1). IF 회차 X의 준비 폴더가 이미 있고 그 `status.md`에 `Review: passed`가 있으면 THEN THE SYSTEM SHALL 준비 세션이 덮어쓰지 않고 그 사실을 알리고 멈춘다. `Review: passed`가 없는 준비 폴더는 덮어쓴다.
- R15 (← G5). IF 강의 세션이 열 회차 X의 준비 폴더가 없거나, 그 `status.md`에 `Review: passed`가 없거나, 거기 적힌 레슨 파일이 없으면 THEN THE SYSTEM SHALL 그 사실을 알리고 `/prepare-lesson <track>`을 먼저 돌리라고 안내한 뒤 멈춘다. 레슨을 만들거나 검토하지 않는다.
- R16 (← G1). WHEN 강의 세션이 회차 X를 열고 `Review: passed`가 있으면 THE SYSTEM SHALL 그 레슨을 다시 검토하지 않는다.
- R17 (← G6). WHEN 강의 중 레슨의 오류나 빠진 내용이 드러나고 고칠 범위가 한 절 이하이면 THE SYSTEM SHALL 강의 세션이 그 자리에서 고친다.
- R18 (← G6). IF 고칠 범위가 한 절을 넘으면 THEN THE SYSTEM SHALL 레슨을 고치지 않고 사용자에게 문제를 채팅으로 설명한 뒤, `NOTES.md` "현재 위치"에 다음 회차로 넘길 내용으로 적는다.
- R19 (← G7). WHEN 준비 세션이 끝나면 THE SYSTEM SHALL `CLAUDE.md` `## Git` 절차로 커밋할 파일 목록과 메시지를 보여 주고 확인을 받은 뒤, 그 세션이 만들거나 고친 파일만 커밋한다. 사용자가 거절하면 커밋하지 않고 끝낸다. 회차 태그는 달지 않는다.
- R20 (← G8; 제약 2). THE SYSTEM SHALL 준비 세션 절차를 트랙에 따라 다르게 하지 않고, 트랙마다 다른 값은 그 트랙 `NOTES.md`의 커리큘럼 표와 "현재 위치"에서만 읽는다. 쓰기는 자기 트랙 폴더에서만 한다.
- R21 (← G8, G4). IF 회차 X가 숫자가 아니면(예: `마무리`) THEN THE SYSTEM SHALL 준비 세션이 커리큘럼 표와 앞 회차들을 보고 준비 폴더 번호 NN을 정하고, 그 선택을 `Open judgments`에 적는다. NN은 다른 `prep/*/` 폴더와 기존 회차 태그의 번호와 겹치지 않는다.
- R22 (← G8, G4). WHEN 강의 세션에서 사용자가 R12로 NN을 다른 값으로 정하면 THE SYSTEM SHALL 준비 폴더 이름을 그 값으로 바꾸고, 회차 브랜치 `lesson-NN`과 회차 태그 `<track>/lesson-NN`에 그 값을 쓴다.

## Design

**진입점.** `.claude/skills/prepare-lesson/SKILL.md` 하나. `disable-model-invocation: true`, 인자는 트랙 이름이다. 본문은 "`docs/learning/operating-rules.md`의 준비 세션 규칙을 따른다"만 적는다. 절차는 `operating-rules.md`에 둔다. 인자가 없으면 `TRACKS.md`의 "진행 중" 트랙을 보여주고 묻는다.

**다음 회차 읽기.** 준비 세션과 강의 세션은 `NOTES.md` "현재 위치"의 첫 항목에서 다음 회차 X를 같은 규칙으로 읽는다. 굵게 표시, 괄호 안 내용, 뒤에 붙은 설명은 무시한다.
- `0회차 준비`가 있으면 X는 `0`이다.
- `N회차 완료`와 `다음은 X회차`가 함께 있으면 X다. 예: `**1회차 완료(2026-11-02), 다음은 2회차(리마인드, MVC2 6장).**` → `2`, `11회차 완료, 다음은 마무리 회차` → `마무리`.
- 커리큘럼 표의 회차 칸은 형식 규칙이 없다(`track-design.md` 4단계는 열만 정한다). 그래서 X는 숫자일 수도 이름일 수도 있다.

**준비 폴더.** `lecture/<track>/prep/NN/`. X가 숫자면 `NN`은 X를 두 자리로 쓴 값이고, 숫자가 아니면 R21로 정한다. `NN`은 회차 태그의 번호와 같다. 회차 X의 준비 폴더는 `status.md`의 `Round`가 X인 `prep/*/`이다. 준비·강의 세션은 폴더 이름이 아니라 이 값으로 찾는다. 레슨은 지금처럼 `lessons/<다음 번호 4자리>-<이름>.html`에 두고 도식·이미지·용어집도 지금 위치에 둔다. 준비 폴더의 파일은 셋이다.
- `status.md`: `Round`(커리큘럼 표 회차 칸의 값 그대로), `Lesson`(트랙 폴더 기준 경로), `Review: passed`, `Open judgments`(`- <질문> → 선택: <값>` 줄). 예:
  ```markdown
  Round: 마무리
  Lesson: lessons/0013-finale.html
  Review: passed

  ## Open judgments
  - 준비 폴더 번호 → 선택: 12
  ```
- `quiz-draft.md`: 문항과 모범 답. 레슨과 문서 어디서도 링크하지 않는다.
- `sources.md`: R7 형식. 레슨에 옮긴 부분의 근거만 적는다.

**준비 세션 순서.** 트랙 확정 → R13·R14 확인 → `status.md`에 `Round` 기록(끊겨도 R14가 그 폴더를 찾도록) → 자료 읽기, 레슨 작성, 검토(`operating-rules.md` "강의 세션의 위임" 표와 `lesson-review.md`를 그대로 쓴다) → `status.md`에 `Lesson`과 결과 기록 → 커밋. 덮어쓰는 준비 폴더의 `status.md`에 `Lesson`이 있으면 새 번호를 따지 않고 그 레슨 파일을 덮어쓴다. 가르칠 내용은 지금까지 강의 세션이 정하던 대로 `NOTES.md` 커리큘럼 표, "현재 위치"에 넘겨 둔 내용, `learning-records/`(규칙 4번에 따라 다른 트랙 것은 읽기만)로 정한다. `NOTES.md`와 `TRACKS.md`는 고치지 않는다. 회차 상태는 강의 세션이 바꾼다.

**강의 세션 변경.** `operating-rules.md` "강의 세션 규칙" 2번("NOTES.md의 '현재 위치'부터 잇는다") 뒤에 확인 규칙을 둔다: R15 → R12(R22 포함) → 레슨 열기. 회차 마무리 정리(같은 절 7번)는 `prep/NN/`을 지워 같은 커밋에 담는다. 끝난 일을 위한 파일이고 이력에는 남는다. 이 삭제는 intent에 없는 정리 결정이다.

**문서 변경 위치.**
- `docs/learning/operating-rules.md`: "준비 세션 규칙" 절(R1~R5, R7, R10, R11, R13, R14, R19~R21, "다음 회차 읽기"), 강의 세션 규칙의 확인 규칙(R12, R15, R16, R22)과 레슨 수정 규칙(R17, R18), "강의 세션의 위임" 절의 "메인이 직접 하는 위임 예외" 중 회차 레슨 작성·지적 수정 항목을 준비 세션 기준으로 고침(G1의 결과).
- `lecture/spring-backend/NOTES.md`: "강의 방식" 회차 순서의 1·2·9단계를 `prep/`을 쓰도록 고치고(R6, R8, R9), "회차 마무리"에 `prep/NN/` 삭제를 더한다. "현재 위치"의 2회차 회상 퀴즈 줄은 2회차를 준비할 때 `quiz-draft.md`로 옮기므로, 구현 때 한 번 손으로 지운다.
- 루트 `CLAUDE.md`의 `## Lessons`: 강의 준비는 `/prepare-lesson`이라고 한 줄 더한다.
- `docker-devcontainer`는 완료된 트랙이라 `NOTES.md`를 고치지 않고, R13으로 준비가 막힌다. 새 트랙은 `track-design.md`가 spring-backend `NOTES.md`를 출발점으로 쓰므로 따로 고치지 않는다.

**겹침.** 같은 트랙의 준비와 강의 세션이 겹치지 않게 하는 일은 사용자의 운영에 맡긴다. R13이 앞 회차 마무리를 확인하고 R14가 통과한 준비를 덮어쓰지 않을 뿐, 열려 있는 강의 세션은 감지하지 않는다. 다른 트랙의 강의·준비 세션과는 함께 돌 수 있다: 쓰기는 R20대로 자기 트랙 폴더에서만 하고, 커밋은 `CLAUDE.md` `## Git` 절차대로 자기 파일 경로만 지정한다.

Test seams:
- 준비 결과(R1~R4, R7, R19)는 `prep/NN/` 세 파일, `lessons/`, `git log`로 직접 본다. R13~R15는 해당 상태를 만들어 두고 세션을 열어 메시지와 쓰기 없음을 본다.
- R5, R6, R8~R12, R16~R18, R20~R22는 규칙 문구와 세션 기록을 읽어 확인한다.

## Alternatives
- Do nothing: 강의를 열 때마다 준비가 끝날 때까지 기다리고 준비 맥락이 강의 중 응답을 늦춘다.
- 강의 세션 안에서 준비를 백그라운드 서브에이전트로 돌리기: 준비 결과가 강의 세션 맥락에 다시 쌓이고 커밋 확인(G7)이 강의 흐름을 끊는다.
- hook이나 일정으로 준비 세션 자동 시작: 앞 회차 마무리 시점을 자동으로 알 수 없고 커밋 확인을 받을 수 없다.
- 퀴즈 초안을 `.scratch/`에 두기: git에서 제외되어 G7의 커밋 대상이 되지 못한다.
- 퀴즈 초안을 `.gitignore` 대상 위치에 두기: 커밋되지 않아 G7과 어긋나고 한 컴퓨터에만 남는다. 학습자가 `prep/`을 직접 열면 볼 수 있지만, 링크하지 않는 것으로 충분하다고 사용자가 정했다(2026-11-04).
