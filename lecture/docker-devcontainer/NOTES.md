# NOTES

## 강의 방식
- 개념은 `RESOURCES.md`의 공식 문서에서 가져온다. 교재가 없다.
- `docs/research/devcontainer-claude.md`의 "미확인" 항목은 실측 전에는 사실로 가르치지 않는다.
- 회차는 아래 순서로 진행한다.
  1. 지난 회차 내용으로 회상 퀴즈 1~2개를 낸다. 첫 회차는 생략한다. 회차 사이가 며칠 이상 벌어졌으면 퀴즈 전에 앞 회차 요약(이번 회차가 기대는 회차는 자세히)을 채팅으로 준다(8회차 사용자 요청).
  2. `lessons/`에 HTML 레슨을 만든다. 개념, 실습 명령, 공식 문서 링크를 담는다.
  3. 개념을 채팅에서 짧게 설명한다.
  4. 실습 명령마다 사용자에게 결과를 먼저 예측하게 한다. 명령의 뜻이 아니라 결과를 묻는다.
  5. 사용자가 명령을 직접 친다.
  6. 출력을 함께 읽고, 예측과 다른 부분을 설명한다.
  7. 면접 질문 2~3개를 묻고 답을 평가한다.
- 레슨에 "오늘 쓰는 명령" 표를 넣는다. 실습의 명령·옵션을 한 줄씩 설명한다.
- 채팅만 보고 수업을 따라갈 수 있게 쓴다. 레슨 HTML은 참고 자료다. "5절 표", "B-3", "A-1 조건표대로"처럼 레슨 위치를 가리키지 않고, 그 표·규칙·값을 채팅에 직접 적는다(8회차 사용자 요청).
- 채팅에서 처음 나오는 명령·옵션은 예측을 묻기 전에 한 줄로 설명한다. 사용자가 뜻을 모르면 예측할 수 없다.
- Dockerfile, `compose.yaml`, `devcontainer.json`은 사용자가 쓰고 Claude가 리뷰한다.
- 면접 답은 개념·원인·원리로 평가한다. 설정 줄의 정확한 문법까지 외우게 하지 않는다(7회차 사용자 의견).
- teach의 브라우저 퀴즈는 만들지 않는다. 예측 후 실행 실습이 대신한다.
- 위 단계가 하나 끝날 때마다 "현재 위치"를 갱신한다. 세션은 예고 없이 끊길 수 있다.

## 명령 실행
- Claude는 상태를 바꾸지 않는 읽기 명령만 직접 실행한다(예: `docker ps|images|inspect|logs|top`, `docker volume|network ls|inspect`, `docker compose ps|config`, `docker buildx history ls|logs`, `docker buildx imagetools inspect`, `docker exec … cat|ls|getent`, `git status|log|diff`). 읽기 명령은 다른 명령과 묶지 않는다. `docker events`에는 `--until`을 붙인다.
- 상태를 바꾸는 명령(`run`, `build`, `rm`, `compose up/down`, `git commit` 등)은 사용자에게 치게 한다.

## 사용자 환경 다루기
- 실습 출력은 `@terminal:lab`으로 받는다([VS Code 문서](https://code.claude.com/docs/en/vs-code#include-terminal-output-in-prompts)).
- 실습 터미널의 이름을 `lab`으로 바꾸게 한다. `@terminal`만 치면 목록이 뜨지 않고 출력도 실리지 않는다.
- 실습 명령마다 먼저 `Clear-Host`를 치게 한다. `@terminal`은 스크롤 기록 전체를 싣는다.
- `@terminal:lab` 첨부가 비어 오면(4회차 내내 그랬다) 다시 시키지 않고 읽기 명령으로 결과를 읽는다. 빌드 출력은 `docker buildx history ls` → `docker buildx history logs <ID>`.
- 통합 브라우저는 같은 주소의 옛 페이지를 캐시로 보여 줄 수 있다. 결과 확인 전 Ctrl+Shift+R을 안내한다.
- `!` Bash 단축키는 안내하지 않는다. 확장에 없다.
- 레슨은 `code <레슨 경로>`로 VS Code 에디터에 연다.
- 레슨을 연 뒤 툴바의 지구본 버튼(Open in Integrated Browser)을 누르라고 안내한다.
- 외부 브라우저(`start`)로 열지 않는다.
- 실습 URL(`http://localhost:…`)은 명령 팔레트 "Browser: Open Integrated Browser"나 터미널 링크 Ctrl+클릭으로 열게 한다([VS Code 문서](https://code.visualstudio.com/docs/debugtest/integrated-browser)).

## 회차 마무리
면접 질문이 끝나면 요청이 없어도 아래를 차례로 한다.
1. "현재 위치"를 "N회차 완료, 다음은 N+1회차"로 바꾼다.
2. 다음 회차로 넘길 내용(못 푼 질문, 리뷰에서 남은 숙제)을 "현재 위치"에 적는다.
3. 학습 기록 조건을 채운 내용을 `learning-records/`에 남긴다.
4. `docker ps -a`, `docker volume ls`, `docker network ls`로 남은 것을 보여 준다.
5. 커리큘럼에 "유지"로 적힌 것과 지울 것을 구분한다. 지우는 명령은 사용자에게 치게 한다.
6. operating-rules.md 강의 세션 규칙 7에 따라 트랙 마크다운을 정리한다.
7. 커밋 전 `git status`와 `git diff`를 함께 확인한다. 커밋은 사용자가 한다.
8. 다음 회차는 새 세션에서 시작하라고 안내하고 세션을 끝낸다.

## 개발 환경
- Windows 11, VS Code.
- Docker Desktop 4.94.0, Engine 29.8.2(WSL2 백엔드, context `desktop-linux`). 2026-10-09 `docker version`으로 확인.
- Compose v5.5.1(2026-10-07 확인).
- VS Code 확장: Container Tools, Dev Containers(`ms-vscode-remote.remote-containers`) v0.469.0.
- 호스트 JDK: Oracle JDK 25.0.4.1.
- 호스트 devcontainer CLI 0.89.0(`npm install -g @devcontainers/cli`, 마무리 회차에 설치, 남김).
- 7회차~ 실습 worktree의 브랜치: `docker-devcontainer`.
- worktree는 `--relative-paths`로 만들었다. 컨테이너 git은 사용자 설정 `dev.containers.experimentalMountGitWorktreeCommonDir`가 켜져 있어야 동작한다(common dir `shop/.git`을 `/workspaces/shop/.git`에 붙인다).
- shop `master` 병합은 spring-backend 강의 세션이 돌고 있지 않을 때 사용자 확인을 받고 한다.
- 창 구성(2026-10-16 확정): 강의는 호스트 VS Code 창(루트)의 Claude 패널, 실습 코딩·빌드·실행은 Dev Containers로 접속한 컨테이너 창. worktree는 bind mount라 호스트 Claude도 같은 파일을 읽고 고친다. `./gradlew`와 앱 실행은 컨테이너에서만 한다(`.gradle/`·`build/`를 두 환경이 같이 쓰고, 호스트 실행은 포트 8080이 되어 spring-backend와 겹친다).

## 커리큘럼
"자료"는 `RESOURCES.md`의 1차 자료다. 면접 질문 후보는 "핵심"의 굵은 글씨다.

| 회차 | 자료 | 기능 또는 주제 | 핵심 | 생략·축소 |
|---|---|---|---|---|
| 0 | What is a container/image, WSL 2 backend | 설치와 구조. Docker Desktop 시작, Dev Containers 확장 설치, `docker run hello-world`, `projects/docker-lab` 만들고 `git init` | **이미지 vs 컨테이너**, **컨테이너 vs VM**, Docker Desktop = WSL2 VM 안의 엔진 + 호스트의 CLI. hello-world 출력으로 pull → create → start 흐름 읽기 | Linux에 Docker Engine 직접 설치 |
| 1 | CLI reference | 컨테이너 다루기. nginx로 `run -d --name`, `ps -a`, `exec -it`, `logs -f`, `stop`, `rm` | 컨테이너 수명주기(created/running/exited), 포그라운드 vs `-d`, **`exec`와 `run`의 차이** | `attach`, `commit` |
| 2 | Volumes, Bind mounts | 데이터. postgres 컨테이너(`POSTGRES_DB=docker_lab`)에 named volume을 붙여, 컨테이너를 지워도 데이터가 남는지 확인. bind mount와 비교 | 컨테이너 쓰기 레이어는 `rm`과 함께 사라짐, **named volume vs bind mount**, Windows 드라이브 bind mount가 느린 이유. 유지: postgres 볼륨 | tmpfs mount |
| 3 | Networking, Bridge driver | 네트워크. `-p 8081:80` publish, 사용자 정의 bridge 네트워크에서 다른 컨테이너가 이름으로 postgres에 접속 | **publish vs `EXPOSE`**, 기본 bridge에는 이름 DNS가 없고 사용자 정의 네트워크에는 있음. 유지: 네트워크, postgres 볼륨 | host·overlay·macvlan 드라이버 |
| 4 | Dockerfile reference, Image layers, Build cache, Build context | 이미지 만들기. docker-lab 앱 생성(엔드포인트 1개가 DB 조회), 호스트에서 `bootJar` → jar를 COPY하는 Dockerfile, `docker build`, 2~3회차의 postgres·네트워크에 붙여 `docker run` | `FROM`·`WORKDIR`·`COPY`·`RUN`·`ENV`·`EXPOSE`·`CMD`/`ENTRYPOINT`, **레이어와 캐시: 명령 순서가 빌드 속도를 바꾸는 이유**, `.dockerignore`, 환경 변수로 DB 주소 주입 | 멀티스테이지, 이미지 최적화(MISSION Out of scope) |
| 5 | Compose file reference, Project name | Compose. 4회차의 `docker run` 명령들을 `compose.yaml`(app은 `build: .`, db는 postgres + volume)로 옮기고 `compose up/ps/logs/down` | 명령형 vs 선언형, 서비스 이름 DNS, `depends_on`과 healthcheck, **compose 프로젝트 이름과 리소스 이름 접두사**, `down`과 `down -v`의 차이. 2~3회차에서 수동으로 만든 볼륨·네트워크는 여기서 정리 | profiles, 여러 compose 파일 병합 |
| 6 | Developing inside a Container, devcontainer.json reference, Improve performance | Dev Container 기초. docker-lab에 `.devcontainer/devcontainer.json`(image 기반)을 쓰고 Reopen in Container, 컨테이너 안에서 `./gradlew bootRun`. 이어서 `dockerComposeFile`로 app + db 구성 | VSCode UI는 호스트, 확장은 컨테이너 안 VS Code Server에서 돈다. **Docker로 운영 환경을 띄우는 것과 dev container의 차이**, `forwardPorts`, Gradle 캐시를 named volume에 두는 이유 | feature 직접 작성, `build.dockerfile` |
| 7 | devcontainer-claude.md, git worktree | shop 적용. worktree 만들기, `.devcontainer/devcontainer.json` 작성(조사 문서 초안에서 출발), `./gradlew build`, 미확인 1~4 실측, 사용자가 커밋. 병합은 "개발 환경"의 조건대로 | **git 브랜치와 worktree**(처음), 실측 결과로 초안 고치기. worktree에서 쓸 호스트 포트(8081) 처리 방식을 미확인 3 결과로 정한다 | — |
| 8 | Development containers (code.claude.com) | 컨테이너 안 Claude. Claude Code feature 추가, 인증·설정 named volume, `CLAUDE_CONFIG_DIR`, 권한 모드. 별도 세션 결과물을 실제로 써 보고 검증 | `containerEnv` vs `remoteEnv`, 컨테이너 안 Claude가 보는 것과 못 보는 것(루트 CLAUDE.md, `courses/`), **격리와 무인 실행의 위험** | — |
| 9 | Headless, devcontainer-claude.md | 호스트↔컨테이너 인수인계. 이슈 파일 → `docker exec … claude -p --output-format json` → 컨테이너 Claude가 브랜치에 커밋 → 호스트에서 `git diff` 리뷰 → `--resume`. 미확인 5~7 실측 | `session_id`와 `--resume`, `permission_denials` 읽기, 리뷰 흐름 | Remote Control, agent teams, MCP·Channel 연결(조사 결과 맞지 않거나 미확인) |
| 마무리 | devcontainer-claude.md | 9회차에 넘긴 미확인 6(`devcontainer exec` CLI)·7(볼륨 위 파일 하나 bind mount) 실측, shop README(9회차 `710a74a`) 다듬기 | 면접 질문 총정리 | — |

## 예정된 공유 파일 변경
강의 세션이 아닌 세션에서 한다. 해당 회차를 마치면 사용자에게 알린다.

## 공유 파일 변경 요청

## 현재 위치
- **마무리 회차 완료(2026-10-21). 커리큘럼 끝.** 다시 열면 `learning-records/0012`의 Implications부터.
- 남긴 것(shop): worktree `shop-docker-devcontainer`(브랜치 `docker-devcontainer`), 컨테이너 `clever_northcutt`, 볼륨 `claude-code-config-1fvkqsrl…`(로그인)·`shop-gradle-home`·`vscode`, 사용자 설정 `dev.containers.experimentalMountGitWorktreeCommonDir`=true. shop `master`는 마무리 회차 끝에 `9159ae6`으로 fast-forward 병합했다.
- 무인 실행 명령 틀: `devcontainer exec --workspace-folder <worktree 호스트 경로> --remote-env ENABLE_CLAUDEAI_MCP_SERVERS=false claude -p "…" [--resume <id>] --allowedTools "Write,Edit,Bash(git add *),Bash(git commit *)" --output-format json`. CLI 없이는 `docker exec -u vscode -w /workspaces/shop-docker-devcontainer -e ENABLE_CLAUDEAI_MCP_SERVERS=false <컨테이너> claude -p …`.
- docker-lab은 커밋이 하나도 없다(전부 untracked).
- 미확인: 6회차 Compose 방식에서 창을 닫을 때 유예 없이 `Exited (137)`이 된 이유(7회차 image 방식은 `Exited (0)`). compose 파일이 `.devcontainer/` 안에 있을 때의 프로젝트 이름. 5회차 C-7 재 `up`에서 `db`만 재생성된 원인. 7회차 자동 forward 포트 43025를 연 컨테이너 프로세스. 8회차 lock 파일이 다음 빌드의 feature 버전을 강제하는지. 9회차 `total_cost_usd`(0.109 → 0.152)가 resume 누적값인지 그 실행만의 값인지. 마무리 회차에서 호스트가 고친 직후 bind mount 파일 첫 읽기의 `No data available` 원인.
- 면접 답 잔여: 5회차 Q3 "시작 ≠ 접속 준비". 8회차 Q3 `.claude.json`이 `~/.claude/` 밖에 생기는 것이 `CLAUDE_CONFIG_DIR`가 필요한 이유. 마무리 Q1 격리 밖 목록(bind mount·common dir, git 자격 증명)·피해 범위·허용 목록 구멍은 리뷰로, Q2 컨테이너 ≠ VM·`overrideCommand` 대기 명령, Q3 브랜치 = 커밋 포인터·HEAD가 몰래 옮겨 가는 문제.
