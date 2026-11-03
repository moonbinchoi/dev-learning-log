# Spec: Korean prose rules and check with im-not-ai
From: intent.md · Status: implemented

이미 끝난 작업의 회고 문서이며, 2026-11-02 디스크에 있는 상태만 적는다. 실제 강의 세션에서 동작한 적은 없다. 승인은 2026-11-02 사용자의 전체 승인 지시에 따른다.

## Requirements
THE SYSTEM은 R1~R3에서 Claude Code와 규칙 파일, R4~R9에서 `.tools/im-not-ai/check-korean.py`, R10에서 레슨 검토 문서, R11~R16에서 `.tools/im-not-ai/sync.py`, R17~R19에서 프로젝트 파일 구성이다.

- R1 (← G1). WHEN Claude가 `lecture/**` 아래 파일을 읽으면 THE SYSTEM SHALL `.claude/rules/korean-humanize.md`를 지침으로 로드한다.
- R2 (← G1). THE SYSTEM SHALL 규칙 파일에서 코드 블록, 인라인 코드, HTML 태그와 속성, 식별자, 명령, 경로, URL, 인용된 프로그램 출력을 바꾸지 말라고 지시한다.
- R3 (← G1). THE SYSTEM SHALL 규칙 파일에 규칙 C-2, C-5, C-9, C-10, J-1을 넣지 않는다.
- R4 (← G2). WHEN `python .tools/im-not-ai/check-korean.py <파일>...`을 실행하면 THE SYSTEM SHALL 파일마다 `<경로> | <글자 수>자 | <패턴 수>건 | <값>/1k | <패턴별 개수 JSON>` 한 줄을 출력하고, 찾을 수 있는 문장마다 `  <패턴> | <문장>` 한 줄을 출력한다. 값은 패턴 수를 글자 수로 나눠 1000을 곱한 뒤 소수 둘째 자리까지 쓴다.
- R5 (← G2). WHEN 같은 파일에 R4를 다시 실행하면 THE SYSTEM SHALL 같은 출력을 낸다.
- R6 (← G2). WHEN 입력이 `.html`이면 THE SYSTEM SHALL `style`, `script`, `svg`, `pre`, `head`, `nav` 요소를 세지 않고, `<code>`는 낱말 `코드`로 바꿔 태그를 뺀 산문만 센다.
- R7 (← G2). WHEN 입력이 그 밖의 파일이면 THE SYSTEM SHALL 코드 펜스와 이미지를 세지 않고, 인라인 코드는 낱말 `코드`로 바꾸고, 제목, 목록, 인용 표시와 `**`를 뺀 산문만 센다.
- R8 (← G2). IF 지표 계산이 실패하면 THEN THE SYSTEM SHALL 실패한 파일의 결과 줄 없이 종료 코드 1로 끝난다. 앞선 파일의 결과 줄은 이미 출력된 채로 남는다.
- R9 (← G2). THE SYSTEM SHALL 합격, 불합격, `risk_band`, `route_hint`를 출력하지 않는다.
- R10 (← G2). THE SYSTEM SHALL `docs/learning/lesson-review.md` 항목 11에서 reviewer가 R4를 실행하고 규칙 파일로 산문을 읽게 하며, 패턴 수가 합격 기준이 아니라고 적는다.
- R11 (← G3). WHEN `python .tools/im-not-ai/sync.py <클론>`을 `--apply` 없이 실행하면 THE SYSTEM SHALL 바뀐 파일, 추가되거나 사라진 규칙 ID, 규칙 파일 변경 줄을 보고하고 프로젝트에는 아무것도 쓰지 않는다.
- R12 (← G3). WHEN `--apply`를 붙이면 THE SYSTEM SHALL `upstream/`의 7개 파일, 규칙 파일, `versions.toml`의 `im-not-ai` 값을 함께 갱신한다.
- R13 (← G3). IF 클론에 7개 파일이나 `quick-rules.md`가 없으면 THEN THE SYSTEM SHALL 아무것도 쓰지 않고 없는 파일을 알리며 끝난다.
- R14 (← G3). IF 가져올 `.py`에 네트워크, 프로세스 실행, `eval`, `exec` 호출이 있으면 THEN THE SYSTEM SHALL 아무것도 쓰지 않고 해당 호출을 알리며 끝난다.
- R15 (← G3). IF `quick-rules.md`에서 보호 문단 3개(`**Do-NOT`, `**서법 보존`, `**내용 앵커`)나 규칙 본문 경계(`## A.`, `## 자체검증`)를 찾지 못하면 THEN THE SYSTEM SHALL 아무것도 쓰지 않고 오류로 끝난다.
- R16 (← G3). IF 새 파일로 내장 표본을 검사해 패턴이 0건이거나 검사가 실패하면 THEN THE SYSTEM SHALL 아무것도 쓰지 않고 오류로 끝난다.
- R17 (← G4). THE SYSTEM SHALL 도구 파일(`README.md`, `check-korean.py`, `sync.py`, `test_check_korean.py`, `upstream/`)을 `.tools/im-not-ai/` 한 폴더에 모은다. 폴더 밖에는 생성된 규칙 파일과, 검토 항목 11, `versions.toml`, `docs/learning/versions.md`, `lecture/spring-backend/NOTES.md`의 참조만 둔다.
- R18 (← G5). THE SYSTEM SHALL `.tools/im-not-ai/README.md`에 출처와 라이선스, 쓰는 파일, 쓰지 않는 것과 이유, 폴더 밖 파일, 사용, 갱신, 제거 절차를 적는다.
- R19 (← G5). THE SYSTEM SHALL 가져온 기준 커밋을 `versions.toml`의 `im-not-ai`와 규칙 파일 머리말에 기록한다.

## Design
- 출처는 https://github.com/epoko77-ai/im-not-ai 이고 현재 기준 커밋은 `b37e020`이다. 이 프로젝트에만 설치하며, 플러그인, 전역 설치, 에이전트, 스킬, 훅, 항상 싣는 컨텍스트는 없다.
- 가져오는 파일 7개는 `LICENSE`, `scripts/{prepare_monolith_input,console}.py`, `skills/humanize-korean/references/{metrics,metrics_v2}.py`, `baseline.json`, `baseline_v2.json`이다.
- 규칙 파일은 `sync.py`가 클론의 `quick-rules.md`로 만들고 손으로 고치지 않는다. 고정 머리말과 보호 문단 3개, `## A.`부터 `## 자체검증` 앞까지의 본문, 라이선스로 구성하고, 제외 규칙은 줄째 뺀다. `quick-rules.md` 자체는 복사하지 않는다. 머리말의 `paths`는 `lecture/**`다.
- 규칙은 쓰는 시점에 적용하는 지침이며, 완성된 글을 고쳐 쓰는 단계로 쓰지 않는다. 학습자의 이해가 규칙보다 우선한다.
- 로드 시점: 강의 세션은 시작할 때 `NOTES.md`를 읽으므로 그때 규칙이 로드된다. `lecture/**` 파일을 읽기 전에 쓴 채팅에는 적용되지 않는다.
- 검사는 `upstream/scripts/prepare_monolith_input.py`를 `sys.executable -I --genre report`로 임시 폴더에서 한 번 실행해 `00_metrics.json`을 읽는다. 이 도구는 지표 계산이 실패해도 0으로 끝나므로 `00_metrics.error` 파일 유무까지 본다. LLM과 네트워크는 쓰지 않는다.
- 검사는 내용 검토 단계에서 시각 검토 전에 한 번 돈다. 고친 뒤 레이아웃이 바뀔 수 있기 때문이다.
- `sync.py`는 `upstream/`, 규칙 파일, `versions.toml`의 `im-not-ai` 줄만 쓰고 트랙 파일은 쓰지 않는다. 강의 세션이 진행 중이어도 실행할 수 있다.
- 추적은 커밋 해시와 README로 한다. 도구 변경의 이력은 남지 않으며, 폴더는 프로젝트 규칙에 따라 git에 넣지 않는다.
- 제거는 폴더, 규칙 파일, 검토 항목 11, `versions.toml`의 주석과 값 두 줄, `versions.md` 행, `NOTES.md` 줄을 지우는 것이다. 작업 공간이 git이 아니므로 되돌릴 수 없다.
- 구현 당시 측정값(1천 자당): AI 문체 표본 28.72(383자, 11건), 레슨 1과 용어집 0, 교재 4·5·6장 0.31, 0.78, 0.59. 기록에는 표본이 28.65(384자)로 적힌 곳도 있다.
- 알려진 한계: 규칙 로드는 격리된 시험 프로젝트와 이 프로젝트의 비강의 세션에서만 확인했다. 현재 위치의 `sync.py`는 커밋 `b37e020`으로만 시험했다. 과거 52개 커밋 재현은 이전 이름의 스크립트로 했고, 최근 29개는 통과, 오래된 23개는 적용 없이 실패했다.

Test seams: `python -I .tools/im-not-ai/test_check_korean.py`가 산문 추출과 규칙 생성을 덮는다. 나머지는 `check-korean.py <파일>` 출력(R4~R9)과 `sync.py <클론>` 시험 실행 출력(R11, R13~R16)을 본다.

## Alternatives
아래 사유는 2026-11-02 조사와 시험 결과이며 근거는 `.scratch/im-not-ai/`에 있다.

- Do nothing: 문체 규칙이 로드되지 않고 레슨 검토에 결정적 근거가 없다.
- 공식 플러그인(`--scope local`): 버전이 2.3.2로 고정돼 업데이트가 멈추고, 스킬 4개와 에이전트 9개가 통째로 들어온다. 전체 설치(`install.sh`)는 전역(`~/.claude`)이다.
- `.claude/skills/im-not-ai/` 스킬 폴더: 스킬의 `paths`가 스킬 본문을 싣지 않아 자동 로드되지 않는다.
- 비공개 클론에 `study` 브랜치를 두고 플러그인으로 사용: 같은 `paths` 문제로 `.claude/rules` 스텁이 필요했고, 사용자가 이 방식을 버려 저장소를 삭제했다.
- 하드 포크: 잦은 규칙 수정(8월 18일 이후 25회)을 놓친다. 공개 포크는 비공개로 바꿀 수 없다.
- `@` 외부 경로 import: 로드되지 않았다.
- 도구 폴더 안의 git 저장소: `.tools/`를 git에 넣지 않는 프로젝트 규칙에 어긋난다.
- 다른 도구(hanlint, korean-writing, im-ai-copyeditor, avoid-ai-writing): 결정적 검사기로 맞지 않아 im-not-ai를 유지했다.

## Open questions
- `reference/` 페이지 작성에도 문체 검사를 적용할 것인가.
- 어투와 특징을 분석한 문서가 생기면 검사에 어떻게 활용할 것인가. 현재 프로젝트에 그런 문서는 없다.
