# Lesson diagrams with D2 Implementation Plan
Status: implemented

> 이 문서는 이미 끝난 작업을 기록한 회고이며, 실행할 것이 남아 있지 않다. 단계는 모두 완료 표시(`- [x]`)이고, 각 요구사항이 어떤 파일과 어떤 확인으로 뒷받침되는지만 적는다.

**Goal:** 레슨에 D2 그림을 명령 하나로 넣고, 라이트·다크 테마와 단계 강조까지 되게 한다.

**Architecture:** 프로젝트 안의 `.tools/d2/d2.exe`가 `.d2` 소스를 SVG와 PNG로 만들고, `docs/learning/render-diagram.py`가 SVG를 색 변수로 바꿔 레슨에 끼운다. 다크 색과 단계 강조는 `style.css`가 맡는다.

**Tech Stack:** D2 v0.9.0(ELK 배치), Python 3 표준 라이브러리, CSS `:has()`.

**Spec:** `docs/design/2026-11-02-d2-lesson-diagrams/spec.md`

## Global Constraints
- 설치는 프로젝트 안뿐이다: 전역 설치, PATH 변경, 제3자 스킬 없음.
- `d2 --version`은 `v` + `versions.toml`의 `d2` 값(`0.9.0`)과 같아야 한다.
- 글꼴은 `C:\Windows\Fonts\malgun.ttf`, `malgunbd.ttf`로 고정한다(Windows 전용, 수용한 제약).
- 그림 폭은 720 이하이고 레슨에는 JS를 넣지 않는다.
- 교재 본문과 그림은 외부 서비스나 artifact로 올리지 않는다.

## Review Focus
아래 다섯 조건은 어떤 작업에도 시험이 없다. 모두 열린 상태이며 시험을 더하지 않았다.
1. 실제 레슨을 VS Code 내장 브라우저에서 열었을 때의 표시(시험은 headless Chrome만).
2. 폭 720 그림의 글자가 500px 화면에서 약 9px로 읽히는지(2회차 첫 그림에서 확인 예정).
3. 맑은 고딕이 없는 PC에서의 배치와 글자 폭(이 PC에서만 시험).
4. 같은 이름의 표시가 한 레슨에 두 번 있을 때(첫 번째만 바뀐다).
5. `d2:` 표시가 든 실제 레슨 전체 흐름(표시가 든 레슨이 아직 없다).

---

### Task 1: 프로젝트 안 D2 설치와 버전 고정
Covers: R8 (버전 확인은 R8의 전제)

**Files:**
- `.tools/d2/d2.exe`, `.tools/d2/LICENSE.txt`
- `versions.toml` (`d2 = "0.9.0"`)
- `docs/learning/versions.md` (갱신 절차), `docs/learning/operating-rules.md` (tool 층, 공유 파일 목록)

**Interfaces:** Produces: 실행 파일 경로 `.tools/d2/d2.exe`, 버전 값 `versions.toml`의 `[versions].d2`.

- [x] `.tools/d2/d2.exe`가 있고 `--version`이 `v0.9.0`을 낸다.
- [x] `versions.toml`에 `d2` 값과 `versions.md`의 갱신 절차가 있다.
- 검증 종류: 명령 실행(이전 세션에서 `--version` 확인, 이번 세션은 Final verification이 버전 검사를 통과해야만 렌더되므로 간접 확인).

### Task 2: 공통 테마
Covers: R12, R14

**Files:** `lecture/spring-backend/assets/diagrams/lesson-theme.d2`

**Interfaces:** Produces: 클래스 `input step fail data done stop ask group flow save off`와 단계 표시 `S1`~`S7`. 그림은 첫 줄에 `...@lesson-theme`을 둔다.

- [x] 파일에 역할 색 7종(`input step fail data done stop ask`), `group`, 선 3종(`flow save off`)이 있고 ELK를 쓴다.
- 검증 종류: R12는 규칙만(파일 내용을 읽어 확인, 색 구분을 재는 자동 검사 없음). R14는 규칙만(`lesson-review.md` 10번 항목이 폭 720 이하를 검토하고, 시험 그림 `flow.d2`는 폭 703으로 Final verification 출력에 나타남. 폭을 막는 코드는 없다).

### Task 3: 렌더러와 레슨 삽입
Covers: R8, R9, R10, R11

**Files:**
- `docs/learning/render-diagram.py`
- Test: `docs/learning/test_render_diagram.py`

**Interfaces:**
- Consumes: Task 1의 `D2` 경로와 버전 값, Task 2의 테마(소스 폴더에서 상대 이름으로 import).
- Produces: `adapt(svg)`, `embed(page, name, svg)`, `main(source, lesson=None)`. Task 4의 CSS가 `adapt`가 만든 `var(--c-<hex>, #<hex>)`에 의존한다.

- [x] `main`이 `.svg`와 `.png`를 `.d2` 옆에 만들고 `<x>.svg <N>KB, 폭 <W>, <x>.png`를 출력한다(R8, R9).
- [x] `embed`가 두 표시 사이만 바꾸고 다시 실행해도 SVG가 하나다(R10). 표시가 없으면 `sys.exit(메시지)`로 종료 코드 1이다(R11). 버전 불일치와 `d2` 실패도 같은 방식이다.
- 검증 종류:
  - R8, R9: 명령 실행. Final verification을 이번 세션에서 실행해 출력 `flow.svg 10KB, 폭 703, flow.png`를 얻었다.
  - R10: 자동 시험 `test_render_diagram.py`의 `embed` 교체·재실행 단언.
  - R11: 자동 시험의 `SystemExit` 단언. 종료 코드 1과 "레슨 파일이 안 바뀐다"는 코드 구조(예외가 쓰기 전에 난다)로 보증하며 스크립트 단위 시험은 없다.

### Task 4: 레슨 페이지 스타일
Covers: R7, R15

**Files:** `lecture/spring-backend/assets/style.css` (76~124행: D2 글꼴, 다크 변수, 범례, 단계 보기, `prefers-reduced-motion`)

**Interfaces:** Consumes: Task 3의 `--c-<hex>` 변수와 Task 2의 `S1`~`S7` 클래스. Produces: `.stepper`, `.step-tabs`, `tr[data-step]`, `.legend` 마크업 규칙(`lecture/spring-backend/NOTES.md`에 기록).

- [x] 다크 값이 `style.css` 한 곳에 있고 `--c-1f1f1f` 등 테마 색 전부를 덮는다.
- [x] `.stepper:has(input[value="N"]:checked)`가 `.S<N>` 상자와 `tr[data-step="N"]`을 함께 강조한다(N 1~7).
- 검증 종류: 둘 다 기록된 시험. R7은 일회용 `.scratch/lesson-diagrams/trial/click-test.py`와 `e2e-build.py`로 7단계를 DOM 클릭해 7/7 강조를 확인했다. R15는 같은 시험 레슨을 `check-layout.py` 다크 500px로 돌린 결과다. 둘 다 저장소 시험이 아니며 이번 세션에 다시 돌리지 않았다.

### Task 5: 레슨 작성 규칙과 검토
Covers: R1, R2, R3, R4, R5, R6, R13

**Files:** `docs/learning/lesson-review.md` (10번 항목), `lecture/spring-backend/NOTES.md` (규칙, 명령, 단계 보기 마크업, 결정 기록)

**Interfaces:** Consumes: Task 3의 명령과 Task 4의 마크업.

- [x] 10번 항목이 출처, 바로 보임, `.d2` 소스, 폭 720 이하, `.stepper` 단계 강조를 검토 기준으로 둔다(R2, R3, R4, R14의 검토 쪽).
- [x] `NOTES.md`에 교재 그림 우선, 에디터 탭으로 열기, 요청 흐름 5~7단계 규칙이 있다(R1, R5, R6).
- 검증 종류: R1~R6은 규칙만이며 자동 검사가 없다. 지켰는지는 레슨을 만들 때 Claude가 지키고 `lesson-review.md`로 사람이 본다. R13은 기록된 시험으로, 시험 레슨에서 `check-layout.py`가 통과했고 기존 1회차 레슨은 위반 14건 그대로였다. 이번 세션에 다시 돌리지 않았고, 실제 레슨에 그림이 든 적도 없다.

## Final verification
`E:\Study\Inflearn`에서 실행한다. `flow.svg`와 `flow.png`를 시험 폴더에 다시 만드는 것이 정상이다.

```
python docs/learning/test_render_diagram.py && python docs/learning/render-diagram.py .scratch/lesson-diagrams/trial/e2e/assets/diagrams/flow.d2
```

기대 출력(2026-11-02 실제 실행, 종료 코드 0):

```
OK
flow.svg 10KB, 폭 703, flow.png
```

## After implementation
저장소 루트가 git 저장소가 아니므로 적용할 PR이 없다. 2026-11-02 사용자의 전체 승인 지시에 따라 `intent.md`, `spec.md`, `plan.md`를 모두 `Status: implemented`로 바꿨다.
