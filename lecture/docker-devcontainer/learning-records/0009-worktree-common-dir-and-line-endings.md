# 마운트 결과는 맞히고, 그 결과를 다음 예측(`.git` 경로, 커밋이 보이는 이유)에 잇지 못했다

7회차(2026-10-16). shop에 `git worktree add --relative-paths -b docker-devcontainer ../shop-docker-devcontainer`로 worktree를 만들고, image 방식 `devcontainer.json`(java:25-trixie, 8081, `shop-gradle-home` 볼륨, 확장 3개)을 써서 컨테이너로 열었다. `.gitattributes`에 `* text=auto eol=lf`를 더해 컨테이너에서 `10fc473`을 커밋했다.

- 회상: Q1 쓰기 레이어 vs 볼륨을 근거까지 맞혔다(6회차 C-11에서 틀린 근거). Q2 볼륨 이름 규칙·재사용을 맞혔고, 되묻자 프로젝트 이름 = `compose.yaml`이 있는 폴더 이름도 답했다. external은 "이름 규칙을 안 따르는 볼륨"으로 알고 있어 "Compose가 만들지도 지우지도 않음"을 보충했다.
- git 처음: A-1 `*`를 새 브랜치에 붙는다고 예측했다(실제 `* master`, `+ docker-devcontainer`). HEAD가 폴더마다 있다는 점을 놓쳤다. A-2 `.git`을 폴더로 예측했다(실제 `gitdir: ../shop/.git/worktrees/shop-docker-devcontainer`). A-3 같은 브랜치 `switch`가 성공한다고 예측했다(실제 `fatal: ... already used by worktree`).
- 작성: `devcontainer.json`을 이름 대조 체크 항목을 받고 한 번에 통과했다(6회차는 5건 수정).
- B-5 마운트(worktree 폴더 하나, `shop-gradle-home` 접두사 없음, `vscode` 볼륨 재사용)는 모두 맞혔다. 그러나 C-8에서는 이 결과를 쓰지 않고 "`/workspaces/shop`이 있다, 브랜치가 보인다"로 예측했다(실제 `fatal: gitfile does not point to a valid repository`).
- B-6 "6회차 캐시를 쓴다"로 예측했다. 볼륨 이름이 다르면 다른 저장소라는 점을 Q2와 연결하지 못했다. C-9b 재빌드 후 "볼륨에 캐시가 남아 다시 받지 않는다"는 근거까지 맞혔다.
- C-10 커밋이 호스트에 보이는 이유를 "프로젝트 폴더 bind mount"라고 했다. 실제 이유는 common dir(`shop/.git`) bind mount다.

실측으로 확인한 것(문서에 없음):
- `--relative-paths` 옵션도 `extensions.relativeWorktrees=true`를 켠다(shop `.git/config`).
- `java:25`와 `java:25-trixie`는 같은 digest였다(`da82e1…`).
- 이미지 라벨의 확장(`dbaeumer.vscode-eslint`)과 json의 확장이 합쳐져 설치된다.
- Gradle 데몬 2개(확장 내장 JRE, 이미지 JDK)가 떠 "incompatible Daemon"이 나온다.
- 미확인 3: Docker가 `0.0.0.0`·`[::]:8081`을 publish한 상태에서 VS Code는 `127.0.0.1:8081`을 잡아 재배정하지 않았다. 브라우저 `localhost:8081` → nginx, `127.0.0.1:8081` → shop.
- 사용자 설정 `dev.containers.experimentalMountGitWorktreeCommonDir`(v0.469.0, 기본 false)를 켜면 `projects\shop\.git → /workspaces/shop/.git`이 붙고 컨테이너 git이 동작한다. 컨테이너 git은 2.56.0이다.
- 호스트 `core.autocrlf=true`는 시스템 설정(`C:/Program Files/Git/etc/gitconfig`)이라 컨테이너로 복사되지 않는다. 그래서 eol 속성이 없는 9개 파일이 컨테이너에서만 modified가 된다. 사용자 `.gitconfig`(작성자)는 복사된다.
- image 방식 컨테이너는 창을 닫으면 `Exited (0)`이 된다(6회차 Compose 방식은 137).
- `dubious ownership` 경고는 나오지 않았다.

면접: Q1 "브랜치 = 여러 버전", "동시성 문제"로 답했다. 포인터라는 정의와, 같은 브랜치를 막는 구체적 이유가 빠졌다. Q2는 처음에 "왜 `.gitattributes`인가"만 답했다. 되묻자 "OS 기본값이 다르다"고 했다(실제: 시스템 설정이 복사되지 않음). 해결도 "LF를 따르게 했다"로 막연했다. Q3는 "VS Code가 더 좁은 `127.0.0.1`을 잡는다"는 핵심만 말했다. 상황(다른 프로그램이 같은 포트를 들음)과 예방(트랙별 고유 포트)이 빠졌다.

## Implications
- 8회차 회상 퀴즈: (1) worktree의 `.git` 파일 내용과, 컨테이너 git에 common dir 마운트가 필요한 이유. (2) 컨테이너에서만 파일이 modified로 보인 원인(시스템 설정은 복사되지 않음)과, 저장소의 줄 끝 규칙이 비교를 바꾸는 방식. 줄의 정확한 내용은 묻지 않는다(사용자 의견: 면접에서 필요한 것은 개념).
- 앞 단계의 실측 결과를 다음 예측의 재료로 쓰지 못한다(B-5 → C-8, Q2 → B-6). 예측 질문에 "앞 단계에서 본 X를 놓고"라고 재료를 명시했을 때도 놓쳤다. 다음에는 예측 전에 그 재료를 한 줄로 다시 말하게 한다.
- 면접 답이 정의 없이 결과만 말한다("효율적", "동시성 문제"). "무엇인가 → 오늘 본 출력 → 그래서"의 순서로 답하게 되묻는다.
- 8회차의 컨테이너 Claude는 이 컨테이너(`modest_ride`, 설정 켬)에서 git을 쓴다. 9회차 `git commit -a` 전에 컨테이너 `git status`가 깨끗한지 먼저 본다.
