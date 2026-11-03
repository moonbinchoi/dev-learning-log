# 새 트랙 설계

새 트랙을 만들 때 따른다. 새 강좌를 트랙으로 만들 때와 기존 트랙을 나눌 때 모두 해당한다. 단계마다 결정은 사용자 확인을 받는다.

## 1. 범위

- 트랙 이름과 사용할 강좌·장 범위를 정한다. 이름 규칙은 [operating-rules.md](operating-rules.md)를 따른다. 근거는 `courses/<course>/README.md`의 장 표다.
- 다른 트랙과 겹치는 장을 찾고, 장마다 이 트랙에서 "복습", "심화", "생략" 중 무엇으로 다룰지 정한다.
- `lecture/TRACKS.md`에 "설계 중" 행을 추가한다.
- 교재 없이 공식 문서로 가르치는 트랙은 `TRACKS.md`의 강좌(장) 칸에 `없음(공식 문서)`을 적고, 장 표 대신 주제 목록을 쓴다. 이 경우 5단계의 1차 자료는 공식 문서다.
- 완료: 범위 안의 모든 장(교재 없는 트랙은 주제)에 다룰 방식이 정해졌다.

## 2. 미션

- `lecture/<track>/`을 만들고, teach 스킬의 MISSION 형식으로 사용자를 인터뷰해 `MISSION.md`를 쓴다.
- 완료: Why, Success looks like, Constraints, Out of scope가 모두 사용자의 답으로 채워졌다.

## 3. 사전 지식

- 다른 트랙의 `MISSION.md`와 `learning-records/`에서 이 범위와 겹치는 이해를 찾는다.
- 이 범위의 경험을 사용자에게 묻는다.
- `learning-records/0001-prior-knowledge.md`에 적는다. 다른 트랙의 기록은 `<track>/NNNN`으로 인용한다.
- 완료: 범위의 장마다 "이미 앎", "리마인드", "처음" 중 하나로 판단됐다.

## 4. 커리큘럼

- `NOTES.md`에 회차 표를 쓴다: `회차 | 강좌·장 | 기능 또는 주제 | 핵심 | 생략·축소`.
- 실습 프로젝트가 있으면 그 회차에 프로젝트에서 만드는 것을 "기능"에 적는다.
- 3단계에서 "이미 앎"으로 판단한 장은 생략하거나 줄인다.
- 완료: 범위의 모든 장이 어느 회차에 있거나, 생략 사유와 함께 "생략·축소"에 있다.

## 5. 자료

- `RESOURCES.md`에 강좌 `docs/` 경로와 버전 차이를 확인할 공식 문서를 적는다.
- 완료: 커리큘럼의 모든 회차가 1차 자료를 하나 이상 가진다.

## 6. 강의 방식

- 기존 트랙 `NOTES.md`의 "강의 방식"과 "회차 마무리"를 출발점으로 제시하고, 사용자와 함께 이 트랙에 맞게 고친다.
- 완료: `NOTES.md`에 "강의 방식", "회차 마무리", "개발 환경", "현재 위치"가 있다.

## 7. 실습 환경

- 프로젝트를 셋 중 하나로 정한다.
  - 새 repo: `projects/<project>/`를 만들고 `git init`한다.
  - 기존 repo 공유: `git -C projects/<project> worktree add --relative-paths -b <track> ../<project>-<track>`. 작업 폴더는 `projects/<project>-<track>`이다.
    - 이 worktree를 dev container로 열면 VS Code 사용자 설정 `dev.containers.experimentalMountGitWorktreeCommonDir`를 켠다. 꺼져 있으면 컨테이너 안 git이 `fatal: gitfile does not point to a valid repository`로 실패한다(`docs/research/devcontainer-claude.md` Git 절).
  - 프로젝트 없음.
- 다른 트랙과 겹치지 않는 포트와 DB 이름을 배정한다.
- 프로젝트가 있으면 `.devcontainer/devcontainer.json`을 둔다. 출발점은 `projects/shop/.devcontainer/devcontainer.json`이다. 앱 포트는 `containerEnv`의 `SERVER_PORT`와 `forwardPorts`에 배정한 포트를 적고, Gradle 캐시는 named volume에 둔다. 이미지 태그는 `versions.toml`의 `devcontainer-java`를 따른다.
- 완료: 프로젝트가 있으면 dev container 안에서 `./gradlew build`가 통과한다. `TRACKS.md` 행의 모든 칸이 채워졌고 상태가 "진행 중"이다. `NOTES.md`의 "현재 위치"는 "0회차 준비"다.
