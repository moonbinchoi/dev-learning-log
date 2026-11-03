# 예측 재료가 주어지면 결과를 맞히고, 무인 실행의 판정 기준을 실측으로 잡았다. 최소 권한의 "왜"는 아직 막연하다

9회차(2026-10-21). 호스트 PowerShell에서 `docker exec -u vscode -w … -e ENABLE_CLAUDEAI_MCP_SERVERS=false <컨테이너> claude -p … --output-format json | ConvertFrom-Json`으로 컨테이너 Claude에게 이슈 파일(`.scratch/dev-container-readme/issue.md`)을 맡겼다. 권한 없이 1회 → `--resume` + `--allowedTools`로 README 커밋(`6cda8ca`) → 호스트 리뷰 → `--resume`으로 리뷰 반영(`710a74a`) 순서로 진행했다. 커넥터는 사용자가 실행 단위로 끄는 방법(①)을 골랐다.

- 회상: Q1은 두 파일로 나뉜다는 점은 맞았지만 `.claude.json`을 "홈 폴더 밖"으로, `CLAUDE_CONFIG_DIR`를 "그 범위를 보게 하는 것"으로 말했다(실제: 홈 안·`~/.claude/` 밖, 쓰는 위치를 옮김). Q2는 bind mount와 커넥터를 짚었고, common dir의 `master`, 네트워크, 공유되는 git 자격 증명(push)은 빠졌다.
- A-2: 옵션 없는 `docker exec`를 `vscode`·`/vscode`로 예측했다(실제 `root`·`/`). `remoteUser`와 `Config.User`를 구별하지 못했다. 토론에서는 root로 띄웠을 때의 작업 폴더·소유자 문제를 스스로 말했다.
- B: 근거 없는 포트 이유를 지어내지 않을 것을 맞혔다.
- D: `--resume`이면 할 일을 안다, `session_id`가 같다, 거부가 없다 세 가지를 모두 맞혔다.
- E: 작성자(복사된 `.gitconfig`)는 맞혔다. `?? .scratch/`는 몰랐다. README 리뷰는 "고칠 것 없음"이었다. 호스트만 아는 사실(포트 이유, worktree 설정)과 8회차 실측(`${devcontainerId}` 불변)에서 나오는 빈칸을 보지 못했다. 후속 커밋을 amend로 예측했다(실제 새 커밋).

실측으로 확인한 것:
- `docker exec` 기본 사용자는 컨테이너의 `Config.User`(`root`), 작업 폴더는 `/`, `HOME=/root`다. `-u vscode`만 줘도 `HOME=/home/vscode`가 된다. `containerEnv`의 `CLAUDE_CONFIG_DIR`는 사용자와 무관하게 보인다.
- Claude Code 2.1.304 `--help`: `--permission-prompts <host|none>`(기본 host)가 있다. `--permission-mode` choices는 `acceptEdits, auto, bypassPermissions, manual, dontAsk, plan`이다(`default` 없음). `--fork-session`은 "resume할 때 새 ID를 만든다"다.
- 권한 옵션 없는 `-p`: 거부 5건(Bash `ls … && cat …` 2, Write 2, Bash `git add && git commit` 1). Read 도구로는 읽었다. `is_error`는 `False`, `num_turns` 9. 저장소 변화 없음.
- `--resume`은 같은 `session_id`를 이어 쓴다. 이어 간 실행은 `num_turns` 4로 이슈 파일을 다시 읽지 않았다.
- `--allowedTools "Write,Edit,Bash(git add *),Bash(git commit *)"`로 `git add … && git commit …` 복합 명령이 거부 없이 돌았다.
- 커밋 작성자는 호스트 사용자(복사된 `.gitconfig`), 날짜는 `+0000`, 본문에 `Co-Authored-By: Claude Sonnet 5.5`가 붙는다.
- `-p`의 `result`가 질문("report.md를 고칠까요?")으로 끝나도 답할 사람 없이 종료된다.
- Rebuild로 컨테이너가 `clever_northcutt`로 바뀌어도 볼륨은 같은 이름으로 다시 붙었다.

면접:
- Q1은 `permission_denials`와 Manual 시작·자동 거부를 말했다. 거부가 실행 실패가 아니라는 점(`is_error` False의 이유)과 `git`으로 실제 결과를 확인한다는 점은 빠졌다.
- Q2는 "예상치 못한 권한 사용을 막는다"로 막연했다. 격리 밖으로 닿는 대상(bind mount의 common dir, 공유 자격 증명의 push, 네트워크, 커넥터)과 피해 범위 제한, 허용 목록이 못 막는 것(amend 같은 방식)을 리뷰로 보완한다는 점이 빠졌다.
- Q3은 root와 그 이유(VS Code를 거치지 않음)를 맞혔다. 결과(`HOME=/root`, 작성자 없음, root 소유 파일)는 말하지 않았다.

## Implications
- 마무리 회차 회상 퀴즈: (1) `is_error` False인데 일을 못 한 상황에서 무엇을 보고 판정하나. (2) `docker exec`의 사용자를 정하는 것은 `remoteUser`인가 `Config.User`인가, `-u`를 빼면 무엇이 깨지나.
- 리뷰를 "틀린 곳 찾기"로만 본다. 마무리 회차에서는 리뷰 관점(근거 없는 문장, 호스트만 아는 맥락, 앞 실측과의 대조)을 목록으로 먼저 주고 리뷰시킨다.
- 최소 권한의 이유는 "격리 경계 밖으로 닿는 것 목록"과 묶어 다시 묻는다(Q2와 회상 Q2가 같은 빈칸).
