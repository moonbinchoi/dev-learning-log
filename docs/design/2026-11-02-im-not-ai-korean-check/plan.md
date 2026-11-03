# Korean prose rules and check with im-not-ai Implementation Plan
Status: implemented

이 문서는 이미 끝난 작업을 기록한 회고이며 실행할 일은 남아 있지 않다. 각 작업은 2026-11-02 디스크에 있는 파일과, 그 동작을 어떻게 확인했는지를 적는다.

**Goal:** 강의 자료와 채팅에 한국어 문체 규칙을 쓰는 시점에 적용하고, 레슨 검토에서 같은 글에 같은 값이 나오는 문체 수치를 본다.

**Architecture:** im-not-ai에서 7개 파일만 `.tools/im-not-ai/upstream/`에 복사한다. `sync.py`가 `quick-rules.md`로 규칙 파일을 만들고, `check-korean.py`가 복사한 `prepare_monolith_input.py`로 패턴을 센다. 플러그인, 에이전트, 스킬, 훅은 없다.

**Tech Stack:** Python 3 표준 라이브러리, `.claude/rules/` 경로 지정 규칙 파일.

**Spec:** `docs/design/2026-11-02-im-not-ai-korean-check/spec.md`

## Global Constraints
- 기준 커밋은 `b37e020`이다. 출처는 https://github.com/epoko77-ai/im-not-ai 이다.
- 규칙 파일 머리말의 `paths`는 `lecture/**`다.
- 제외 규칙은 C-2, C-5, C-9, C-10, J-1이다.
- 작업 공간은 git 저장소가 아니다. `.tools/`는 git에 넣지 않는다.
- 패턴 수는 합격 기준이 아니다. `risk_band`, `route_hint`는 쓰지 않는다.

## Review Focus
다섯 항목 모두 시험을 추가하지 않았고 열린 상태다.
1. 실제 강의 세션에서 규칙 로드: 비강의 세션에서 `NOTES.md`를 읽을 때만 로드를 봤다. 강의 세션은 한 번도 돌지 않았다.
2. `lecture/**` 파일을 읽기 전에 쓴 채팅: 규칙이 적용되지 않는다. 세션 시작 때 `NOTES.md`를 읽는 순서에 기댄다.
3. 원본 저장소가 `quick-rules.md` 구조를 바꾸는 경우: 최근 29개 커밋 재현은 통과했고 오래된 23개는 적용 없이 실패했다. 현재 위치의 `sync.py`는 `b37e020`으로만 시험했다.
4. 패턴이 0건인 AI 문체나 표본에 없는 문체: 내장 표본 한 개로만 `sync.py`가 시험한다. 기록에 남은 표본 값 차이(28.65 대 28.72)의 원인도 추적하지 않았다.
5. `check-korean.py`를 여러 파일에 돌릴 때 중간 파일에서 실패하는 경우: 앞 파일의 결과 줄은 이미 출력된다.

---

### Task 1: 도구 폴더와 가져온 파일
Covers: R17 (command run in this session), R18 (command run in this session)

**Files:**
- `.tools/im-not-ai/README.md`
- `.tools/im-not-ai/upstream/` (7개 파일: `LICENSE`, `scripts/prepare_monolith_input.py`, `scripts/console.py`, `skills/humanize-korean/references/metrics.py`, `metrics_v2.py`, `baseline.json`, `baseline_v2.json`)

**Interfaces:**
- Produces: `upstream/scripts/prepare_monolith_input.py`. Task 2가 실행하고 `_ROUTE_TELL_KEYS_V16`, `_ROUTE_TELL_KEYS_V2`, `_V26_ROUTE_PATTERNS`를 읽는다.

- [x] **Step 1:** `ls .tools/im-not-ai`가 `README.md`, `check-korean.py`, `sync.py`, `test_check_korean.py`, `upstream`을 보여 준다(`__pycache__`는 시험 잔여물이다). R17의 폴더 밖 참조 네 곳은 Task 5에 있다.
- [x] **Step 2:** `upstream/` 아래 7개 파일이 있다. `quick-rules.md`는 복사하지 않았다.
- [x] **Step 3:** `.tools/im-not-ai/README.md`의 제목 `쓰는 것`, `쓰지 않는 것`, `이 폴더 밖에 있는 것`, `사용`, `갱신`, `제거`와 첫 문단(출처, MIT 라이선스)이 R18의 항목을 담는다. `grep -n '^#'`로 확인했다.

### Task 2: 문체 검사 `check-korean.py`
Covers: R4 (command run in this session), R5 (command run in this session), R6 (automated test `test_check_korean.py`, HTML 단언), R7 (automated test `test_check_korean.py`, Markdown 단언), R8 (rule only, no automated check), R9 (command run in this session)

**Files:**
- `.tools/im-not-ai/check-korean.py`: `prose(path)`, `scan(text, vendor=VENDOR)`, `main(paths)`
- `.tools/im-not-ai/test_check_korean.py`

**Interfaces:**
- Produces: `prose(path) -> str`, `scan(text, vendor) -> {"chars", "tells", "counts", "hits"}`. Task 3과 Task 4의 시험이 `scan`을 쓴다.

- [x] **Step 1 (R6):** `check.prose`가 `.html`에서 `head`, `pre`, `svg`를 빼고 `<code>`를 `코드`로 바꿔 `문장 코드 끝`을 낸다고 `test_check_korean.py`가 단언한다. `style`, `script`, `nav` 제거는 같은 정규식이 처리하지만 단언하지 않는다.
- [x] **Step 2 (R7):** `.md`에서 제목, 목록 표시, 코드 펜스, 인라인 코드를 처리해 `제목\n\n코드 항목`을 낸다고 단언한다. 이미지, `**`, 인용 표시는 단언하지 않는다.
- [x] **Step 3 (R4, R9):** 이 세션에서 `python .tools/im-not-ai/check-korean.py lecture/spring-backend/lessons/0001-item-form-validation.html`을 실행했다. 출력은 `lecture/spring-backend/lessons/0001-item-form-validation.html | 5174자 | 0건 | 0.00/1k | {}`이며 걸린 문장 줄은 없다. 구현 당시 값 0건과 같다. 줄 형식은 Final verification의 출력에서도 본다. 두 출력 모두 `risk_band`, `route_hint`가 없고 `check-korean.py`에서 두 낱말은 주석에만 있다.
- [x] **Step 4 (R5):** 같은 레슨 파일에 두 번 실행한 출력의 md5가 `786f0e505dbcd8ae248acaa07659ba88`로 같았다.
- [x] **Step 5 (R8):** `scan`이 종료 코드, `00_metrics.error` 파일, `00_metrics.json` 유무를 보고 `RuntimeError`를 낸다. 실패를 일으켜 확인한 적은 없다.

### Task 3: 규칙 파일 생성 `build_rule`
Covers: R2 (rule only, no automated check), R3 (automated test `test_check_korean.py`), R15 (automated test `test_check_korean.py`)

**Files:**
- `.tools/im-not-ai/sync.py`: `HEADER`, `DROP`, `PROTECT`, `build_rule(clone, commit)`, `rule_ids(text)`
- `.claude/rules/korean-humanize.md` (생성물, 손으로 고치지 않는다)

**Interfaces:**
- Produces: `build_rule(clone, commit) -> str`. 보호 문단 3개나 `## A.`, `## 자체검증`이 없으면 `ValueError`를 낸다. Task 4가 쓴다.

- [x] **Step 1 (R3):** 시험이 가짜 클론에서 `build_rule`을 돌려 `- **C-2**`가 규칙 파일에 없고 `## 자체검증` 뒤 내용이 없다고 단언한다. 이 세션에서 `grep -cE '^- \*\*(C-2|C-5|C-9|C-10|J-1)\*\*' .claude/rules/korean-humanize.md`도 0이었다.
- [x] **Step 2 (R15):** `## A.`만 있는 `quick-rules.md`로 `build_rule`을 부르면 `ValueError`가 난다고 단언한다. 이 단언은 `build_rule`까지만 덮고, `main`이 이 오류에서 아무것도 쓰지 않는다는 점은 단언하지 않는다. `main`은 `build_rule`을 쓰기 전에 부르고 `sys.exit`로 끝난다.
- [x] **Step 3 (R2):** `HEADER`의 첫 글머리 줄이 코드 블록, 인라인 코드, HTML 태그와 속성, 식별자, 명령, 경로, URL, 인용한 출력을 바꾸지 말라고 지시한다. 규칙 문구라서 자동 검사는 없다.

### Task 4: 갱신 흐름 `sync.py`
Covers: R11 (recorded trial, dry-run at new location in the 2026-11-02 implementation session), R12 (recorded trial, `--apply` at new location in the same session), R13 (rule only, no automated check), R14 (rule only, no automated check), R16 (rule only, no automated check)

**Files:**
- `.tools/im-not-ai/sync.py`: `main()`, `FILES`, `QUICK_RULES`, `FORBIDDEN`, `SAMPLE`

**Interfaces:**
- Consumes: Task 2의 `scan`, Task 3의 `build_rule`, `rule_ids`.

- [x] **Step 1 (R13, R14):** `main`이 없는 파일 목록과 금지 호출 목록으로 `sys.exit`한다. 쓰기는 이 검사 뒤에 있다. 시험 실행은 기록에서 항목별로 확인하지 못했다.
- [x] **Step 2 (R16):** 임시 폴더로 복사한 파일에 `scan(SAMPLE, vendor=trial)`을 돌리고, 예외나 패턴 0건이면 `sys.exit`한다. 쓰기는 그 뒤에 있다. 기록에서 항목별로 확인하지 못했다.
- [x] **Step 3 (R11):** `--apply` 없이 실행하면 바뀐 파일, 추가·사라진 규칙, 규칙 파일 변경 줄을 출력하고 `시험만 했다`로 끝난다. 이동한 위치에서 시험 실행을 한 기록은 2026-11-02 구현 세션 기록에 있다. 이 문서를 쓸 때는 클론이 없어 실행하지 않았다.
- [x] **Step 4 (R12):** `--apply`가 `upstream/`의 7개 파일, 규칙 파일, `versions.toml`의 `im-not-ai` 줄을 쓴다. 적용 기록은 2026-11-02 구현 세션 기록에 있고, 시험한 커밋은 `b37e020`뿐이다.

### Task 5: 프로젝트 연결
Covers: R1 (recorded trial, 2026-11-02 비강의 세션 관찰), R10 (command run in this session), R19 (command run in this session)

**Files:**
- `.claude/rules/korean-humanize.md` (머리말 `paths: "lecture/**"`)
- `docs/learning/lesson-review.md` 항목 11, `docs/learning/versions.md`, `versions.toml`, `lecture/spring-backend/NOTES.md` 82번째 줄

- [x] **Step 1 (R1):** 2026-11-02 이 프로젝트의 비강의 세션에서 `lecture/spring-backend/NOTES.md`를 읽었을 때 규칙 파일이 지침으로 로드됐다. 이 관찰 외 별도 기록 파일은 없다. 실제 강의 세션은 돌지 않았다.
- [x] **Step 2 (R10):** `docs/learning/lesson-review.md` 28번째 줄 항목 11이 `check-korean.py` 실행, 규칙 파일로 산문 읽기, `패턴 수는 합격 기준이 아니다`를 적는다.
- [x] **Step 3 (R19):** `versions.toml` 16번째 줄이 `im-not-ai = "b37e020"`이고, 규칙 파일 10번째 줄 머리말이 `commit b37e020`을 적는다.
- [x] **Step 4:** `lecture/spring-backend/NOTES.md`와 `docs/learning/versions.md` 14번째 줄이 `README.md`를 가리킨다.

## Final verification
`E:\Study\Inflearn`에서 실행한다.

```bash
python -I .tools/im-not-ai/test_check_korean.py && python .tools/im-not-ai/check-korean.py .scratch/im-not-ai/seeded-ai-style-sample.txt
```

이 세션에서 실제로 나온 출력이다. 종료 코드는 0이다.

```
OK
.scratch/im-not-ai/seeded-ai-style-sample.txt | 383자 | 11건 | 28.72/1k | {"분열문(D-8)": 1, "이유다(D-10)": 1, "시간지평(D-11)": 1, "은유가족(D-14)": 1, "범용동사(F-7)": 2, "결산변이(D-1)": 1, "conclusion_pivot_count": 4}
```

이어서 걸린 문장이 `  <패턴> | <문장>` 형식으로 7줄 나온다(분열문 D-8, 이유다 D-10, 시간지평 D-11, 은유가족 D-14, 범용동사 F-7 두 줄, 결산변이 D-1). 구현 당시 값 `OK`와 `383자 | 11건 | 28.72/1k`와 같다.

## After implementation
git 저장소가 아니라서 이 작업에 해당하는 PR은 없다. 2026-11-02 사용자의 전체 승인 지시에 따라 intent.md, spec.md, plan.md를 모두 `Status: implemented`로 바꿨다.
