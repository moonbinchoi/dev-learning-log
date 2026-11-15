# dev-learning-log

백엔드 개발 학습 기록 저장소입니다. AI 튜터(Claude Code)와 1:1 수업 방식으로 공부하면서, 회차마다 만든 레슨, 학습 기록, 수업 운영 규칙을 그대로 남깁니다.

## 학습 트랙

| 트랙 | 상태 | 내용 | 실습 프로젝트 |
|---|---|---|---|
| [spring-backend](lecture/spring-backend/) | 진행 중 | 스프링 MVC 검증, 세션 로그인, 필터·인터셉터, DB 접근 | shop (상품 주문 관리 서비스) |
| [docker-devcontainer](lecture/docker-devcontainer/) | 완료 (11회차) | Docker 기초, Compose, Dev Container 개발 환경 | docker-lab, shop-docker-devcontainer |

전체 목록과 상태는 [lecture/TRACKS.md](lecture/TRACKS.md)에 있습니다. 실습 프로젝트 코드는 이 저장소가 아닌 별도 저장소에서 관리합니다.

## 폴더 안내

| 경로 | 내용 |
|---|---|
| `lecture/<track>/MISSION.md` | 트랙의 목표와 완료 기준 |
| `lecture/<track>/lessons/` | 회차별 레슨 (HTML) |
| `lecture/<track>/learning-records/` | 회차별 학습 기록: 틀린 문제, 오개념, 다음에 확인할 것 |
| `lecture/<track>/reference/` | 복습용 요약 자료 |
| `docs/learning/` | 수업 운영 규칙, 채점 기준, 레슨 검사 스크립트와 테스트 |
| `docs/design/` | 학습 환경을 바꿀 때 쓴 설계 문서 (의도, 명세, 계획) |
| `docs/issues/` | 작업 이슈 기록 |
| `knowledge/` | 참고 노트 |
| `.claude/`, `CLAUDE.md` | AI 튜터의 에이전트, 훅, 규칙 설정 |
| `.tools/` | 보조 도구 (한국어 문체 검사, 다이어그램 렌더링) |

레슨은 HTML 파일이라 GitHub에서는 소스로 보입니다. 내려받아 브라우저로 열면 화면으로 볼 수 있습니다.

## 공개하지 않는 자료와 관리 방법

이 저장소는 공개 저장소이므로, 아래 자료는 로컬에만 두고 git에 올리지 않습니다. 모두 `.gitignore`에 등록되어 있고, 공개 이전의 커밋 이력에서도 제거했습니다.

| 자료 | 로컬 위치 | 공개하지 않는 이유 |
|---|---|---|
| 유료 강의 교재(PDF, 변환한 마크다운, 예제 코드) | `courses/` | 강의 저작물 |
| 레슨에 인용한 교재 그림 | `lecture/<track>/assets/course-figures/` | 강의 저작물 |
| 학습 운영 분석 자료(세션 기록, 비용 분석) | `docs/research/` | 로컬 환경 정보와 원시 기록 포함 |
| 개인 작업 메모, 로컬 환경에 묶인 문서 | `docs/NEXT-SESSIONS.md` 등 | 로컬 경로, 비공개 저장소 정보 포함 |
| 비밀 값 | `.env`, `.claude/settings.local.json` | API 키, 계정 정보 |

관리 규칙:

- **교재 원문은 `courses/` 밖으로 옮기지 않습니다.** 레슨은 교재 내용을 직접 풀어 쓰고, 출처는 "교재 N장 M줄" 형식으로만 밝힙니다.
- **교재 그림을 레슨에 그대로 넣어야 하면 `assets/course-figures/`에만 둡니다.** 그래서 일부 레슨(spring-backend 2·3회차)은 공개 저장소에서 그림 자리가 비어 있고, 대체 텍스트와 출처 문구만 남아 있습니다. 직접 그린 그림은 `assets/diagrams/`와 `assets/images/`에 두며 공개됩니다.
- **비밀 값은 파일에 적지 않습니다.** 필요하면 `.env`나 `settings.local.json`에 두고, 이 두 파일은 git에 올리지 않습니다.
- **새 폴더를 만들 때는 공개 여부를 먼저 정합니다.** 비공개라면 커밋하기 전에 `.gitignore`에 추가합니다.

이 때문에 문서 곳곳의 `courses/`, `docs/research/` 링크는 공개 저장소에서는 열리지 않습니다.

## 라이선스 표기

`.tools/im-not-ai/upstream/`은 MIT 라이선스, `.tools/d2/`는 MPL-2.0 라이선스의 외부 도구이며 각 폴더에 라이선스 파일이 있습니다.
