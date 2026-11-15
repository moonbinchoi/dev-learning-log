# dev-learning-log

백엔드 개발 학습 기록 저장소입니다. AI 튜터(Claude Code)와 1:1 수업 방식으로 공부하면서, 회차마다 만든 레슨, 학습 기록, 수업 운영 규칙을 그대로 남깁니다.

학습은 2026년 10월 초에 시작했습니다. 이 저장소의 커밋 기록이 11월부터인 것은, 공개로 전환하면서 강의 교재 자료를 이력에서 지우느라 기록을 정리했기 때문입니다. 그 전 기록은 학습 기록 파일의 날짜(예: [docker 0006](lecture/docker-devcontainer/learning-records/0006-build-cache-and-context.md)의 2026-10-14)와 [spring-shop의 커밋 기록](https://github.com/moonbinchoi/spring-shop/commits)(2026-10-02부터)에 남아 있습니다.

## 학습 트랙

| 트랙 | 상태 | 내용 | 실습 프로젝트 |
|---|---|---|---|
| [spring-backend](lecture/spring-backend/) | 진행 중 | 스프링 MVC 검증, 세션 로그인, 필터·인터셉터, DB 접근 | [spring-shop](https://github.com/moonbinchoi/spring-shop) (상품 주문 관리 서비스) |
| [docker-devcontainer](lecture/docker-devcontainer/) | 완료 (11회차) | Docker 기초, Compose, Dev Container 개발 환경 | [docker-lab](https://github.com/moonbinchoi/docker-lab), [spring-shop의 docker-devcontainer 브랜치](https://github.com/moonbinchoi/spring-shop/tree/docker-devcontainer) |

전체 목록과 상태는 [lecture/TRACKS.md](lecture/TRACKS.md)에 있습니다. 실습 프로젝트 코드는 이 저장소가 아닌 별도 저장소에서 관리합니다.

## 학습 방식

한 회차는 다음 순서로 진행합니다.

1. **예측**: 명령이나 코드를 실행하기 전에 결과와 그 근거를 먼저 말합니다.
2. **직접 구현과 실행**: 실습 코드는 제가 작성하고, 프로젝트의 Dev Container 안에서 실행해 실제 결과를 확인합니다.
3. **비교와 리뷰**: 예측과 실제 결과가 다르면 그 이유를 짚습니다. 실습 코드는 채점 기준([grading.md](docs/learning/grading.md))을 받은 리뷰 에이전트가 채점합니다.
4. **학습 기록**: 틀린 예측, 오개념, 다음 회차에서 다시 물을 것을 `learning-records/`에 남깁니다.
5. **피드백과 규칙 개선**: 회차가 끝나면 강의 내용과 자료를 평가하고, 고칠 점은 수업 운영 규칙과 검사 스크립트에 반영합니다.

역할은 이렇게 나눕니다.

| 맡는 쪽 | 하는 일 |
|---|---|
| AI | 교재를 바탕으로 레슨·퀴즈 준비, 질문과 설명, 채점, 학습 기록 초안 작성 |
| 나 | 예측과 답변, 실습 코드 작성과 실행, 회차 피드백, 운영 규칙 변경 승인 |

## 먼저 볼 것

| 자료 | 볼 점 |
|---|---|
| [학습 기록 docker 0006](lecture/docker-devcontainer/learning-records/0006-build-cache-and-context.md) | Docker 빌드 캐시 실험에서 예측과 실제 결과(15.2초, 2.3초 등)를 비교하고, 틀린 이유를 다음 회차 퀴즈로 넘긴 기록 |
| [레슨 화면: docker 6회차 Compose](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0006-compose.html) | AI와 함께 만든 레슨이 실제로 어떻게 보이는지 |
| [회차 피드백](lecture/spring-backend/feedback.md) → [커밋 61f8c2f](https://github.com/moonbinchoi/dev-learning-log/commit/61f8c2f) | "흐름도가 크다"는 피드백을 그림 높이 700px 제한 규칙과 자동 검사로 바꾼 예 |
| [설계 문서: 강의 준비 세션 분리](docs/design/2026-11-03-lesson-prep-session/) | 학습 환경을 바꿀 때 의도 → 명세 → 계획 순서로 설계한 문서 |
| [practice-guard 훅](.claude/hooks/practice-guard.js) | 메인 AI 세션이 실습 코드를 직접 읽지 못하게 막고, 채점은 리뷰 에이전트에게만 맡기게 하는 훅 (테스트 포함) |

## 레슨 보기

레슨은 GitHub Pages로 브라우저에서 바로 볼 수 있습니다.

- docker-devcontainer: [1](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0001-installation-and-structure.html) · [2](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0002-container-lifecycle.html) · [3](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0003-volumes-and-bind-mounts.html) · [4](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0004-networking.html) · [5](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0005-building-images.html) · [6](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0006-compose.html) · [7](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0007-dev-container-basics.html) · [8](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0008-shop-worktree-dev-container.html) · [9](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0009-claude-in-dev-container.html) · [10](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0010-host-container-handoff.html) · [11](https://moonbinchoi.github.io/dev-learning-log/lecture/docker-devcontainer/lessons/0011-finale.html)
- spring-backend: [1](https://moonbinchoi.github.io/dev-learning-log/lecture/spring-backend/lessons/0001-item-form-validation.html) · [2](https://moonbinchoi.github.io/dev-learning-log/lecture/spring-backend/lessons/0002-member-session-login.html) · [3](https://moonbinchoi.github.io/dev-learning-log/lecture/spring-backend/lessons/0003-login-check-filter-interceptor.html)

spring-backend 2·3회차는 교재 그림을 공개하지 않아 그림 자리가 비어 있고, 대체 텍스트와 출처만 남아 있습니다.

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

## 공개하지 않는 자료

- 유료 강의 교재(`courses/`)와 레슨에 인용한 교재 그림(`assets/course-figures/`)은 저작권 때문에 git에 올리지 않았고, 공개 전 커밋 이력에서도 지웠습니다. 레슨은 교재를 직접 풀어 쓰고 출처는 "교재 N장 M줄" 형식으로만 밝힙니다.
- 로컬 환경 정보가 담긴 분석 자료(`docs/research/`), 개인 작업 메모, 비밀 값(`.env`, `.claude/settings.local.json`)도 올리지 않습니다.
- 그래서 문서 곳곳의 `courses/`, `docs/research/` 링크는 이 저장소에서 열리지 않습니다.

## 라이선스 표기

`.tools/im-not-ai/upstream/`은 MIT 라이선스, `.tools/d2/`는 MPL-2.0 라이선스의 외부 도구이며 각 폴더에 라이선스 파일이 있습니다.
