# Docker·Dev Container Resources

교재가 없다. 아래 공식 문서가 1차 자료다. 링크는 2026-10-07에 열리는 것을 확인했다.

## Knowledge

### 이 워크스페이스의 조사 결과
- [docs/research/devcontainer-claude.md](../../docs/research/devcontainer-claude.md)
  shop `devcontainer.json`(커밋 `10fc473`), 정한 설계, 인수인계 방식 비교, 미확인 4·9~11. Use for: 6~9회차의 출발점.

### Docker (docs.docker.com)
- [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/), [What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)
  Use for: 0회차 이미지와 컨테이너의 차이, 컨테이너 vs VM.
- [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/)
  Use for: 0회차 Windows에서 Docker가 도는 구조, 2회차 Windows 드라이브 마운트 성능.
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
  Use for: 1회차 `run`·`ps`·`exec`·`logs`·`stop`·`rm`의 옵션 확인. 모든 회차의 상태 확인 명령.
- [Running containers](https://docs.docker.com/engine/containers/run/), [Logging](https://docs.docker.com/engine/logging/), [Start containers automatically](https://docs.docker.com/engine/containers/start-containers-automatically/)
  Use for: 1회차 포그라운드/백그라운드, `logs`가 STDOUT·STDERR를 읽는 원리(nginx 로그 링크), 재시작 정책.
- [Volumes](https://docs.docker.com/engine/storage/volumes/), [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
  Use for: 2회차 named volume과 bind mount 비교.
- [Networking overview](https://docs.docker.com/engine/network/), [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)
  Use for: 3회차 포트 publish, 사용자 정의 네트워크와 컨테이너 이름 DNS.
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/), [Understanding image layers](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/), [Build cache](https://docs.docker.com/build/cache/), [Build context와 .dockerignore](https://docs.docker.com/build/concepts/context/)
  Use for: 4회차 Dockerfile 명령, 레이어 캐시, 빌드 컨텍스트.
- [Compose file reference](https://docs.docker.com/reference/compose-file/), [Specify a project name](https://docs.docker.com/compose/how-tos/project-name/)
  Use for: 5회차 서비스·볼륨·`depends_on`, compose 프로젝트 이름.
- [postgres 공식 이미지](https://hub.docker.com/_/postgres)
  Use for: 2·5회차 `POSTGRES_DB` 등 환경 변수와 데이터 경로.

### Dev Container
- [VS Code: Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)
  Use for: 6~7회차 Reopen in Container, 확장이 컨테이너 안에서 도는 구조.
- [devcontainer.json reference (containers.dev)](https://containers.dev/implementors/json_reference/)
  Use for: 6~8회차 `forwardPorts`, `mounts`, `containerEnv` vs `remoteEnv`, `postCreateCommand`.
- [VS Code: Improve container performance](https://code.visualstudio.com/remote/advancedcontainers/improve-performance)
  Use for: 6~7회차 Gradle 캐시를 named volume에 두는 이유.
- [VS Code: Use Docker Compose](https://code.visualstudio.com/docs/devcontainers/create-dev-container#_use-docker-compose)
  Use for: 6~7회차 Compose 방식의 서비스·소스 마운트·기다리는 명령.
- [devcontainers/images: java](https://github.com/devcontainers/images/tree/main/src/java)
  Use for: 6~7회차 `mcr.microsoft.com/devcontainers/java:25-trixie` 태그. 사용자(`remoteUser` vscode)와 기본 명령은 문서에 없어 이미지 라벨로 확인했다.
- [git worktree](https://git-scm.com/docs/git-worktree), [Pro Git: Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
  Use for: 7회차 브랜치·HEAD, worktree, `.git` 파일과 common dir, `--relative-paths`.
- [VS Code: Resolving Git line ending issues in containers](https://code.visualstudio.com/docs/devcontainers/tips-and-tricks#_resolving-git-line-ending-issues-in-containers-resulting-in-many-modified-files), [gitattributes](https://git-scm.com/docs/gitattributes)
  Use for: 7회차 컨테이너에서만 파일이 modified로 보이는 문제와 `* text=auto eol=lf`.
- [VS Code: dev container CLI](https://code.visualstudio.com/docs/devcontainers/devcontainer-cli), [devcontainers/cli](https://github.com/devcontainers/cli)(README 명령 목록, `src/spec-node/utils.ts`의 라벨 찾기, `devContainersSpecCLI.ts`의 옵션)
  Use for: 마무리 회차 `devcontainer exec`가 라벨로 VS Code의 컨테이너를 찾고 `remoteUser`·`remoteEnv`를 적용한다는 근거.
- [Docker forum: single-file bind mount](https://forums.docker.com/t/sharing-a-single-file-via-a-volume-mount-does-not-work-as-expected/57088)
  Use for: 바꿔치기한 파일을 컨테이너가 못 본다는 보고(공식 문서 아님). 마무리 회차 이 PC에서는 재현되지 않았다.
- Dev Containers 사용자 설정 `dev.containers.experimentalMountGitWorktreeCommonDir`: 공식 문서 페이지 없음. v0.469.0 확장의 설정 설명과 [이슈 #11478](https://github.com/microsoft/vscode-remote-release/issues/11478)이 근거.
  Use for: 7회차 이후 worktree 컨테이너의 git.

### 컨테이너 안 Claude (code.claude.com)
- [Development containers](https://code.claude.com/docs/en/devcontainer)
  Use for: 8회차 Claude Code feature, 인증 볼륨, `CLAUDE_CONFIG_DIR`, 권한 모드.
- [Permission modes](https://code.claude.com/docs/en/permission-modes), [Memory](https://code.claude.com/docs/en/memory), [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory), [Authentication](https://code.claude.com/docs/en/authentication), [MCP: Use MCP servers from Claude.ai](https://code.claude.com/docs/en/mcp)
  Use for: 8회차 시작 모드·순환, `/context` vs `/memory`, `.claude.json`·`.credentials.json` 위치, 컨테이너 로그인, 계정 커넥터와 `disableClaudeAiConnectors`.
- [Claude Code feature 소스](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code), [Node feature](https://github.com/devcontainers/features/tree/main/src/node), [lockfile 스펙](https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainer-lockfile.md)
  Use for: 8회차 Node 자동 설치 실패 원인, Node `lts` 기본값, `devcontainer-lock.json`.
- [Run Claude Code programmatically (headless)](https://code.claude.com/docs/en/headless), [Sessions](https://code.claude.com/docs/en/sessions), [CLI reference](https://code.claude.com/docs/en/cli-reference), [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
  Use for: 9회차 `claude -p`, `--output-format json`, `-p`의 Manual 시작과 자동 거부, `--allowedTools`, `session_id`와 `--resume`, 세션 저장 위치, 호스트↔컨테이너 세션이 서로 닿지 않는다는 근거.

## Wisdom (Communities)

- 아직 사용자에게 묻지 않았다.
