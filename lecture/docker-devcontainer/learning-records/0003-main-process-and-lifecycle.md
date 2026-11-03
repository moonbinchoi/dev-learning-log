# 컨테이너 수명은 주 프로세스에 묶인다: exec 셸 종료를 컨테이너 종료로 오해했다

1회차(2026-10-09). nginx로 run → logs → exec → stop → start → rm을 예측 후 실행했다. 실습에서 틀린 예측 두 개가 핵심이었다.

- exec 셸에서 `exit`하면 "nginx가 종료 신호를 받아 Exited"라고 예측했다. 결과는 `Up 12 minutes`. 터미널이 *어느 프로세스*에 붙어 있는지(포그라운드 run = PID 1, logs = 호스트의 docker logs, exec = 추가 프로세스 sh)로 정리한 뒤, 면접 답에서 "sh만 죽고 컨테이너엔 영향 없다"를 스스로 말했다.
- running 컨테이너를 `-f` 없이 `rm`하면 "알아서 지운다"고 예측했다. 실제는 데몬이 거부한다(`container is running: stop the container before removing or force remove`).

맞힌 것: 포그라운드 Ctrl+C → Exited (0), `-d` 출력이 컨테이너 ID, 멈춘 컨테이너에 exec는 오류, start 후 `/tmp/mark.txt` 유지(같은 ID·CREATED로 같은 컨테이너임을 확인).

Windows 구조 질문은 세 번째 시도에서 "클라이언트는 Windows, 데몬은 WSL2, `docker version`의 `OS/Arch`"까지 답했다. 필드 값(windows/linux)은 말하지 않았다.

## Implications
- 2회차 첫 실습: 같은 이미지로 새 컨테이너를 띄워 `mark.txt`가 없음을 확인한다(rm과 함께 쓰기 레이어가 사라진다는 1회차 예측의 실측). 이것이 볼륨이 필요한 이유로 이어진다.
- 2회차 회상 퀴즈: exec `exit` 뒤 컨테이너 상태와 그 이유(주 프로세스), stop/start 사이 유지되는 것(쓰기 레이어·ID·설정)과 새로 시작되는 것(주 프로세스, exec 프로세스는 다시 안 뜸).
- "쓰기 가능한 컨테이너 레이어"를 "컨테이너 안의 저장소"라고 불렀다. 용어집 용어로 답하도록 계속 요구한다.
- 오류 메시지의 `Error response from daemon`을 클라이언트·데몬 구조의 근거로 쓸 수 있다는 것을 보여 줬다. 3회차 `172.17.0.1`(요청 출발 주소)도 1회차 로그에서 미리 봐 두었다.
