# Mission: Docker와 Dev Container로 개발 환경 만들기

## Why
백엔드 취업에 필요한 Docker 기본기를 원리부터 갖춘다. 프로젝트 환경(JDK·DB)을 코드로 고정해 어느 PC에서나 같은 환경을 띄우고, 그 설정을 shop repo에 넣어 포트폴리오에서 보여준다.

## Success looks like
- `projects/docker-lab`에서 app + Postgres를 Compose로 띄우고, 쓴 명령마다 무슨 일이 일어나는지 설명할 수 있다.
- 자주 쓰는 Dockerfile 명령으로 이미지를 직접 만들고, 레이어와 캐시가 빌드에 미치는 영향을 설명할 수 있다.
- shop을 dev container로 열어 `./gradlew build`와 실행이 되고, 그 `.devcontainer/` 설정이 shop repo에 커밋돼 있다.
- 호스트 Claude가 이슈 파일로 컨테이너 Claude에게 작업을 맡기고 `git diff`로 리뷰하는 흐름을 한 번 끝까지 돌렸다.
- 회차마다 나온 면접 질문(예: 컨테이너 vs VM, 이미지 레이어, bind mount vs volume)에 "왜?"까지 답할 수 있다.

## Constraints
- Docker는 처음이다.
- 교재 없음. Docker docs, VS Code Dev Containers docs, containers.dev, code.claude.com 공식 문서가 1차 자료다.
- 실습 명령은 사용자가 직접 친다.
- Windows 11, Docker Desktop(WSL2 백엔드), VSCode.
- 1세션 = 1회차, 회차당 1시간 내외.
- 컨테이너에는 프로젝트 폴더만 마운트한다. `courses/`(유료 자료)를 컨테이너에 노출하지 않는다.

## Out of scope
- Kubernetes.
- Dockerfile 심화(멀티스테이지 최적화 등). 레이어 개념과 자주 쓰는 명령만 다룬다.
