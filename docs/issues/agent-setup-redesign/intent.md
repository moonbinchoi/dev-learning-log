# Intent: 프로젝트 에이전트 구성 재설계

Author: moonbinchoi
Status: accepted (2026-10-20)

## Problem

- P1. 강의 세션 위임 문서가 이전 세대 전역 오케스트레이션의 에이전트와 파일을 가리킨다. `investigator`, `architect`, `editor`, `ORCHESTRATION.md`는 지금 없다(`docs/learning/operating-rules.md:56-67`, `docs/learning/lesson-review.md:7`). 현재 전역 에이전트는 `explorer`, `analyst`, `researcher`, `worker`, `reviewer`, `general-purpose`다.
- P2. 전역 규칙 "모든 검토는 `reviewer`에게"와 프로젝트 `grader`의 관계가 어디에도 정해져 있지 않다.
- P3. 프로젝트 에이전트가 현재 전역 에이전트의 작성 형식을 따르지 않는다. 정의가 한국어라 토큰이 약 1.57배 들고, 상태 줄이 없고, 강제되지 않는 산문 제한이 있다(`grader`의 "Bash는 git에만"; 로컬 관찰에서 실제로 `ls`, `cat`을 실행했다).
- P4. `operating-rules.md:74`가 전역에서 사라진 `Delegation exception` 관례를 언급한다.
- P5. `.claude/hooks/grader-guard.js`가 저장소 밖의 `projects/` 경로도 막는다. 2026-10-20 `~/.claude/projects/.../memory` 파일 읽기가 거부됐다.

## Proposed outcome

- O1. 강의 세션의 모든 위임이 실재하는 에이전트로 모호함 없이 이어진다. 지금 따르는 규칙 문서(`docs/learning/`, `.claude/`, `CLAUDE.md`)에 없는 에이전트·파일 이름이 0건이다.
- O2. 프로젝트 전용 에이전트는 전역 에이전트에 브리프만 줘서는 할 수 없는 일에만 남고, 남는 에이전트마다 그 이유가 한 줄 있다.
- O3. 프로젝트 문서에는 전역 규칙과 다른 점만 적는다.
- O4. 실습 폴더 보호 hook이 저장소의 `projects/`만 막는다. 자체 검사가 `~/.claude/projects/` 경로를 포함해 통과한다.

## Affected users and systems

- 사용자: 학습자이자 이 저장소의 소유자.
- 강의 세션의 메인 Claude와 그 서브에이전트.
- 파일: `.claude/agents/*.md`, `.claude/hooks/grader-guard*.js`, `.claude/settings.json`, `docs/learning/operating-rules.md`, `docs/learning/lesson-review.md`, `docs/superpowers/specs/`.

## Constraints

- C1. 결과물 품질이 떨어지지 않는다.
- C2. 토큰 비용을 줄이는 방향이다.
- C3. 전역 파일(`~/.claude/`)은 고치지 않는다. 발견한 문제는 보고만 한다.
- C4. 사용자에게는 한국어로 답한다. 에이전트만 읽는 글은 영어로 쓴다(전역 CLAUDE.md).
- C5. `.claude/` 아래는 보호 경로다. 서브에이전트의 쓰기는 거부될 수 있으므로 메인 세션이 쓴다.
- C6. 이전 세대의 기록 문서는 고치지 않는다. 필요 없으면 지운다.

## Open questions

- 없음. 인터뷰에서 모두 결정했다.
