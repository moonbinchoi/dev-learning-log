# 앞 단계의 결과를 예측 재료로 쓰기 시작했고, 격리 밖의 계정 연결을 스스로 짚었다. 환경 변수가 필요한 진짜 이유는 놓쳤다

8회차(2026-10-20). shop dev container에 Claude Code feature, `claude-code-config-${devcontainerId}` 볼륨, `CLAUDE_CONFIG_DIR`(containerEnv), 측정용 `remoteEnv`를 더했다. Rebuild → 로그인 → 보이는 것 확인 → 권한 모드 → 재 Rebuild 후 로그인 유지 → `21b4dda` 커밋(lock 파일 포함) 순서로 진행했다. 회차 간격이 길어 회상 퀴즈 전에 0~7회차 요약을 받았다.

- 회상: Q1 worktree 흐름은 맞았지만 `.git` 파일의 상대 경로가 `/workspaces/shop/.git`으로 풀린다는 점은 빠졌다. Q2는 "LF가 달랐다"로 막연했다가, 재답에서 "어느 PC의 git이든 `.gitattributes`를 보고 같은 규칙을 맞춘다"로 핵심을 말했다.
- 7회차 `chown`의 이유(새 볼륨은 root 소유)를 스스로 다시 말하고 `.claude`에도 필요하다고 판단했다. 실측 `vscode root`(그룹 root)로 확인됐다. `devcontainer.json`은 조건 5개를 모두 채워 한 번에 통과했다.
- `chown -R ~`를 제안했다. 볼륨 내부까지 매번 순회하는 비용, 문제는 마운트 지점뿐이라는 점, Dockerfile에서 미리 만드는 방법으로 답했다.
- B-2: 볼륨 개수와 gradle 재사용은 맞혔다. 재사용 근거는 "named volume이라서"였다(실제: 같은 이름). `${devcontainerId}`를 컨테이너 ID로 예측했는데, 재 Rebuild에서 컨테이너가 바뀌어도 볼륨 이름이 그대로인 것으로 반증됐다.
- B-3: node는 20.x로 예측했다(실제 v24.22.0, Node feature 기본 `lts`). `docker exec printenv`의 결과("한 줄, LAB_WHERE 빠짐")는 맞혔다.
- C-5: 루트·전역 `CLAUDE.md`가 없고 `courses`가 안 보인다는 예측을 모두 맞혔다. `/mcp`의 커넥터 3개는 "호스트 MCP"로 예측했다(실제: claude.ai 계정 커넥터).
- E-7: 근거(쓰기 레이어 초기화, 같은 볼륨, `CLAUDE_CONFIG_DIR`)를 세 요소로 나눠 정확히 말했다.
- F-8: `devcontainer-lock.json`이 생길 것은 예측하지 못했다.

실측으로 확인한 것(문서에 없거나 미확인이었던 것):
- `java:25-trixie`에는 Node가 없다. Claude Code feature의 자동 설치는 NodeSource 18 저장소를 더한 뒤 `apt-get install nodejs`를 실행한다. 그런데 Debian `nodejs 20.19.2+dfsg`가 설치되고 npm이 없어 `Failed to install Node.js and npm`으로 끝났다. `ghcr.io/devcontainers/features/node:1`을 더하자 Node 24.22.0이 설치되고 빌드가 성공했다.
- `remoteEnv` 값은 `docker exec`로 띄운 프로세스에 보이지 않는다. `containerEnv` 값은 보인다.
- 새 named volume의 마운트 지점은 root:root로 만들어진다. `chown vscode` 뒤에 `vscode root`가 된다.
- `${devcontainerId}`는 소문자·숫자 52자이고, Rebuild 뒤에도 같다.
- `CLAUDE_CONFIG_DIR`를 지정하면 `.claude.json`과 `.credentials.json`이 모두 볼륨 안에 생긴다. Rebuild 뒤에도 로그인을 묻지 않았다.
- 컨테이너 Claude의 `/context`에는 Memory files 항목이 없었다. 모델은 Sonnet 5.5였다. claude.ai 커넥터(Claude Docs·Gmail·Notion, 도구 103개)가 로그인과 함께 들어왔다.
- Claude Code 2.1.304는 auto 모드로 시작했다. Shift+Tab 순환은 manual → accept edits → plan → auto였다.
- 터미널의 `claude`가 컨테이너 창 에디터의 선택 줄을 받았다.
- feature를 쓰면 `.devcontainer/devcontainer-lock.json`이 생긴다(claude-code 1.0.5, node 1.7.1의 digest).
- `No space left on device`(docker-desktop WSL에 VS Code Server를 설치하다 실패)는 정상적으로 열 때도 나온다. 빌드와는 무관했다.

면접:
- Q1은 커넥터를 근거와 함께 짚었다. 그러나 bind mount된 worktree와 `shop/.git`(master 포함)을 바꿀 수 있다는 점, 볼륨 안의 인증 정보, 네트워크는 빠졌다.
- Q2는 정의, 실측, 결론을 모두 말했다.
- Q3는 "볼륨만 붙이면 Claude가 default 경로를 찾는다"고 답했다. 실제로는 기본 경로가 볼륨 경로와 같고, 문제는 `~/.claude.json`이 폴더 밖에 생긴다는 점이다.

## Implications
- 9회차 회상 퀴즈:
  (1) 볼륨만 붙이면 로그인이 풀리는 이유(`.claude.json`의 위치)와 `CLAUDE_CONFIG_DIR`가 바꾸는 것.
  (2) 확인 없이 도는 컨테이너 Claude가 바꿀 수 있는 호스트 쪽 대상(bind mount 둘, 특히 common dir)과 계정 커넥터.
- 예측 앞에 재료를 한 줄로 다시 적어 주자, 앞 단계의 결과를 예측에 쓰기 시작했다(chown, E-7). 이 방식을 계속한다.
- 9회차 `docker exec`는 기본 사용자가 컨테이너 사용자일 수 있다(6회차 이미지에서는 `root`). 그러면 HOME과 bypass 거부가 달라진다. `-u vscode`가 필요한지 예측시킨다(미실측).
- 9회차 무인 실행 전에 shop에 `disableClaudeAiConnectors`를 켤지 사용자와 정한다.
