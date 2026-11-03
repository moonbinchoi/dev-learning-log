# Spec: Lesson diagrams with D2
From: intent.md · Status: implemented

이미 끝난 작업의 회고 문서이며, 디스크에 있는 구현만 적는다. 실제 레슨에는 아직 쓰인 적이 없다. 승인은 2026-11-02 사용자의 전체 승인 지시에 따른다.

## Requirements
THE SYSTEM은 R1~R6에서 레슨을 만드는 Claude, R7과 R12~R15에서 레슨 페이지와 공통 테마, R8~R11에서 `docs/learning/render-diagram.py`다.

- R1 (← G1). WHERE 2회차 이후 레슨이 핵심 개념을 다루면 THE SYSTEM SHALL 그 개념의 동작 원리를 그림과 함께 설명한다.
- R2 (← G2). IF 교재나 공식 자료에 맞는 그림이 있으면 THEN THE SYSTEM SHALL 그 그림을 넣고 그림 아래에 출처를 적는다.
- R3 (← G2). IF 맞는 그림이 없으면 THEN THE SYSTEM SHALL D2로 직접 그린다.
- R4 (← G3). THE SYSTEM SHALL 모든 그림을 링크로 보내지 않고 레슨 페이지에 바로 보이게 넣는다.
- R5 (← G3). WHEN 강의 중 그림을 보여 주면 THE SYSTEM SHALL 이미지 파일을 VS Code 에디터 탭으로 열고, 채팅에는 같은 흐름을 코드 블록 도식으로 적는다.
- R6 (← G4). THE SYSTEM SHALL 요청 흐름 그림을 5~7단계로 그리고 단계 번호, 판단 주체, 분기, 단계별 데이터 위치를 담는다.
- R7 (← G4). WHEN 사용자가 레슨에서 단계 N(1~7)을 고르면 THE SYSTEM SHALL 단계 N의 활성 구성 요소를 강조한다.
- R8 (← G5). WHEN `python docs/learning/render-diagram.py <x.d2>`를 실행하면 THE SYSTEM SHALL `<x.d2>` 옆에 `<x>.svg`와 라이트 색 `<x>.png`를 만든다.
- R9 (← G5). WHEN R8이 끝나면 THE SYSTEM SHALL `<x>.svg <N>KB, 폭 <W>, <x>.png` 한 줄을 출력한다. N은 SVG 글자 수를 1024로 나눈 몫이고 W는 SVG `viewBox`의 폭이다.
- R10 (← G5). WHEN 레슨 파일을 두 번째 인자로 주면 THE SYSTEM SHALL `<!-- d2:<x> -->`와 `<!-- /d2 -->` 사이를 SVG로 바꾼다. 다시 실행해도 SVG는 하나만 남는다.
- R11 (← G5). IF 레슨에 두 표시 중 하나라도 없으면 THEN THE SYSTEM SHALL 레슨을 바꾸지 않고 없는 표시를 알리는 메시지와 함께 0이 아닌 종료 코드로 끝난다.
- R12 (← G6). THE SYSTEM SHALL 공통 테마로 서로 구분되는 파스텔 역할 색 7종, 묶음 상자, 선 3종을 제공한다.
- R13 (← G7). WHEN 그림이 든 레슨을 `docs/learning/lesson-review.md` 절차로 검토하면 THE SYSTEM SHALL 그림을 넣기 전의 같은 레슨보다 `check-layout.py` 위반 수를 늘리지 않는다.
- R14 (← G7). THE SYSTEM SHALL 그림 폭을 720 이하로 유지한다.
- R15 (← G7). WHERE 다크 테마이면 THE SYSTEM SHALL 그림 색을 다크 값으로 표시한다.

## Design
- 설치: `.tools/d2/d2.exe`(D2 v0.9.0)만 프로젝트 안에 둔다. 전역 설치, PATH 변경, 제3자 스킬은 없다. 스크립트는 `d2 --version`이 `v` + `versions.toml`의 `d2` 값과 다르면 메시지와 함께 종료한다.
- 그림 선택: 교재 그림은 `courses/*/docs/*_images/`에서 트랙의 `assets/images/`로 복사해 넣는다. 흰 배경 그림은 다크 모드에서도 흰 바탕에 둔다. 직접 그린 그림은 `style.css`의 단계 강조가 닿도록 인라인 SVG로 넣는다.
- 교재는 유료 자료이므로 본문과 그림을 외부 서비스에 올리거나 artifact로 게시하지 않는다.
- 테마: 원본은 `lecture/spring-backend/assets/diagrams/lesson-theme.d2`이고 그림 첫 줄은 `...@lesson-theme`, 배치 엔진은 ELK다. 상자 색은 `input #f5f5f5`, `step #dae8fc`, `fail #ffe6cc`, `data #fff2cc`, `done #d5e8d4`, `stop #f8cecc`, `ask #e1d5e7`(마름모), 묶음은 `group #f8f8f4`다. 선은 `flow`(실선), `save`(움직이는 점선), `off`(옅은 점선)다.
- 렌더: `d2`를 소스 폴더에서 상대 이름으로 호출한다. 절대 경로면 `@lesson-theme` import를 찾지 못한다. 글꼴은 `C:\Windows\Fonts\malgun.ttf`, `malgunbd.ttf`로 고정해 Windows 전용이며, 이는 수용한 제약이다.
- SVG 변환(`adapt`): 임베드 `@font-face`를 지우고, `fill`과 `stroke`의 6자리 hex를 속성과 CSS 규칙 두 형식 모두 `var(--c-<hex>, #<hex>)`로 바꾼다. 다크 값은 `lecture/spring-backend/assets/style.css` 한 곳에 두며, 색을 더하면 다크 값도 함께 더한다. PNG는 변환하지 않아 라이트 색이다.
- 단계 보기: `<div class="stepper">` 안에 `<fieldset class="step-tabs">`의 `<input type="radio" value="N">`, 그림, `<tr data-step="N">` 표를 둔다. 상자에는 `class: [step; S3]`처럼 `S<N>`을 붙인다. N을 고르면 CSS `:has()`로 `.S<N>` 상자와 표 줄이 함께 강조된다. 레슨에는 JS를 넣지 않는다.
- 범례는 SVG 폭을 늘리지 않도록 HTML `<ul class="legend">`로 둔다.
- 애니메이션은 `save` 선뿐이고 `prefers-reduced-motion: reduce`이면 끈다.
- 오류: 표시 없음, 버전 불일치, `d2` 실패는 모두 메시지와 함께 종료 코드 1로 끝난다. 레슨 파일 자체가 없으면 SVG와 PNG를 만든 뒤 Python 예외로 끝난다.
- 강의 중 표시: Claude 채팅 패널에는 이미지가 나오지 않으므로 `code <이미지 경로>`로 연다.
- 진행 중인 강의 세션이 있으면 트랙 파일을 고치지 않는다.
- 효과 판단: G1의 효과는 2회차 후 사용자 피드백으로 판단하며 측정값은 없다.
- 알려진 한계: 폭 720 그림은 500px 화면에서 글자가 약 9px이고, 2회차 첫 그림에서 확인한다. 이 PC의 맑은 고딕에 의존하며 다른 PC에서는 시험하지 않았다. 표시는 시험에 쓴 headless Chrome 기준이고 VS Code 내장 브라우저에서는 시험하지 않았다. 같은 이름의 표시가 두 번이면 첫 번째만 바뀐다.
- 검토 규칙은 `lesson-review.md` 10번 항목(출처, 페이지 표시, `.d2` 소스, 폭 720 이하, 단계 강조)에, 갱신 절차는 `docs/learning/versions.md`에 있다.

Test seams: `docs/learning/test_render_diagram.py`가 `adapt()`와 `embed()`를 직접 호출한다. 렌더 전체는 샘플 `.d2`로 스크립트를 실행해 출력 줄과 SVG, PNG 파일을 본다. 단계 강조와 다크 표시는 저장소에 자동 시험이 없고, `check-layout.py`와 이미지 검토로 본다.

## Alternatives
아래 사유는 2026-11-02 조사와 시험 결과이며 근거는 `.scratch/lesson-diagrams/`에 있다.

- Do nothing: 레슨마다 그림을 손으로 그려야 하고, 교재 그림이 있는데도 직접 그리는 일이 반복된다.
- Hand-written SVG + CSS: 좌표를 손으로 맞춰야 해서 G5를 못 채운다.
- Figma: 원본이 `.fig` 바이너리라 텍스트로 검토할 수 없고, 쓰기 기능이 유료로 옮겨 가며, 한글을 시험하지 못했다.
- beautiful-mermaid, mermaid-cli: 색 변수 후처리나 Chromium이 필요하고 대비를 `check-layout.py`로 재기 어렵다.
- next-ai-draw-io: 참고 후보다. 브라우저 탭에서 내보내야 하고 자동 배치가 없다. D2 자동 배치가 기대에 못 미치면 먼저 볼 후보이지만 확정된 대체재는 아니다.
