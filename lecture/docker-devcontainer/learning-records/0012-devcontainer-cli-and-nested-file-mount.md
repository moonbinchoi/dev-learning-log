# 실측으로 미확인 6·7을 닫았다. 예측은 앞 회차 결과를 새 도구에 그대로 옮기는 경향이 남았고, 브랜치를 커밋 포인터로 말하지 못했다

마무리 회차(2026-10-21). 호스트에 devcontainer CLI 0.89.0을 설치해(`npm install -g @devcontainers/cli`, C/C++ 빌드 없이 3초) shop 컨테이너에 `devcontainer exec`을 쳤다. docker-lab에서 볼륨 `lab-vol`을 `/data`에, 호스트 파일 `mount-test\note.md`를 `/data/note.md`에 붙인 alpine:3.22 컨테이너로 겹친 마운트를 쟀다. shop README는 사용자가 네 관점으로 리뷰해 고칠 곳을 정하고, 사용자 요청으로 Claude가 썼다.

- 회상: Q1(`is_error` False인데 일 못 함)은 `permission_denials`와 `git`, 거부 ≠ 실패를 맞혔다. Q2는 `root`·`Config.User`는 맞혔지만 깨지는 것(`HOME=/root`, 작업 폴더 `/`, `.gitconfig` 못 읽음, root 소유 파일)을 못 댔다.
- A: `devcontainer exec`의 사용자를 9회차 `docker exec` 결과(`root`)로 예측했다. CLI가 `remoteUser`를 적용한다는 재료를 쓰지 않았다. 없는 폴더에서 오류로 끝난다는 예측은 맞았다. 토론에서 CLI 쪽 비용으로 "vscode로 실행"을 들었다(실제로는 장점. 비용은 `-u` 없음, Node 필요, 떠 있는 컨테이너에만 붙음).
- B: `docker run --mount` 두 개가 만들 때 함께 붙는다는 것을 몰라 처음 예측의 전제가 틀렸다(설명 뒤 재예측은 맞음). 컨테이너가 `/data/other.txt`를 쓰면 호스트 폴더에 생긴다고 예측했다(실제는 볼륨. 붙인 것은 파일 하나다). 볼륨에 빈 자리 파일이 남는 것은 예측하지 못했다. 몇 번은 결과를 먼저 보고 예측을 적었다.
- 토론(shop에 CLAUDE.md bind mount): `readonly`와 "프로젝트 CLAUDE.md가 낫다"는 맞혔다. 위험을 LF로 말했다(핵심: 컨테이너 Claude가 호스트 전역 지침을 고쳐 모든 호스트 세션에 퍼진다).
- C: README 빈칸 셋(첫 로그인, CLI 사용법, `.gitattributes` 설명)을 찾았다. `.gitattributes`는 커밋돼 있어 설정할 일이 없다는 점은 놓쳤다. 리뷰 요청한 문장의 근거(실측 vs 원리 추론)를 묻자 답하지 않았다.

실측으로 확인한 것:
- `devcontainer exec --workspace-folder E:\…\shop-docker-devcontainer`는 VS Code가 띄운 `clever_northcutt`을 다시 쓴다(라벨 `e:\…`와 대문자 `E:\` 경로가 맞음). `whoami` vscode, `pwd` `/workspaces/shop-docker-devcontainer`, `HOME=/home/vscode`. 출력에 Docker Desktop의 `docker exec` 안내("What's next: Try Docker Debug …")가 붙는다.
- 라벨이 맞는 컨테이너가 없으면(`projects\shop`) `Error: Dev container not found.`로 끝나고 컨테이너를 만들지 않는다(773 ms).
- `--remote-env K=V`는 그 실행에만 변수를 더한다. `containerEnv`의 `CLAUDE_CONFIG_DIR`도 보인다.
- 볼륨 마운트 안 경로에 파일 bind mount를 겹치면 둘 다 동작한다. 그 경로의 쓰기는 호스트 파일로, 나머지 경로의 쓰기는 볼륨으로 간다. Windows 파일은 `-rwxrwxrwx root`, 볼륨 파일은 `-rw-r--r--`로 보인다.
- 컨테이너를 지우면 볼륨에 0바이트 `note.md`(마운트 지점, 컨테이너 생성 시각)가 남는다.
- 호스트에서 `Set-Content`로 다시 쓰든 `Move-Item -Force`로 바꿔치든, 직후 1~2회 읽기는 `cat: read error: No data available`, 몇 초 뒤엔 새 내용이 보였다. 크기·mtime은 즉시 새 값, inode 번호는 바꿔치기 뒤에도 같았다. 포럼 보고("옛 파일을 계속 본다")는 이 환경에서 재현되지 않았다. 원인은 미확인.
- `Set-Content`는 CRLF를 쓴다(`v1 from host` 14바이트).

면접:
- Q1(최소 권한): 커넥터·네트워크를 댔다. bind mount(common dir의 `master`, 호스트 파일), 공유 git 자격 증명(push), "피해 범위 제한"이라는 이유, 허용 목록이 못 막는 방식(amend)을 리뷰로 보완한다는 점은 빠졌다. 허용 목록 구멍을 "더 좁히기"로 답했다.
- Q2(이미지 실행 vs dev container): 세 축을 잡았다. 컨테이너를 "리눅스 가상 OS", 주 프로세스를 "리눅스"로 말했다(실제: VM 아님·커널 공유, `overrideCommand`의 대기 명령). 소스 반영은 맞았지만 "컨테이너 rebuild"라고 했다(이미지 build).
- Q3(브랜치·worktree): 브랜치를 "worktree를 가리키는 포인터"로, 금지 이유를 push 충돌로 말했다(실제: 커밋 포인터, 다른 worktree의 HEAD가 몰래 옮겨 가 작업 폴더와 어긋나고 그대로 커밋하면 변경을 되돌린다).

## Implications
- 트랙 커리큘럼은 끝났다. 다시 이 트랙을 열면 면접 질문 Q1(격리 밖 목록과 피해 범위), Q3(브랜치 = 커밋 포인터, HEAD)부터 회상시킨다.
- 새 도구의 결과를 예측할 때 앞 도구의 결과를 그대로 옮긴다. 예측 재료에 "무엇이 이전과 다른가"를 한 줄로 짚게 한다.
- 결과를 보고 예측을 적는 일이 있었다. 예측을 먼저 받고 명령을 주는 순서를 지킨다.
