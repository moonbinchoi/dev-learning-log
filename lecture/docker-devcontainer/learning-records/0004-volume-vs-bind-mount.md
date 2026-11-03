# bind mount를 복사·단방향으로 오해했다: "같은 디렉터리"로 교정

2회차(2026-10-14). A(쓰기 레이어) → B(anonymous volume) → C(named volume) → D(bind mount)를 예측 후 실행했다. 볼륨 쪽 예측은 거의 맞았고, 틀린 예측은 bind mount에 몰렸다.

- D-8: 빈 `site`를 nginx HTML 경로에 bind mount하면 "Welcome이 보인다"고 예측했다. 결과는 403. 원래 파일이 가려진다는 것을 표로 읽고도 예측에 쓰지 못했다.
- D-10: 컨테이너 안에서 만든 `c.txt`가 "이미 bind mount돼 있으니 호스트에 안 보인다"고 예측했다. 결과는 보임. "마운트 시점에 이미지 파일이 가려짐"과 "마운트 뒤 그 경로 = 호스트 폴더"를 구분하지 못했다.
- B-2: anonymous volume 이름을 `postgres`로 예측했다. postgres의 DB 이름 기본값과 Docker 볼륨 이름을 섞었다.
- B-3: "볼륨은 언제든 연결/해제할 수 있다"고 했다. 마운트는 create 때 정해진다고 교정했다.

맞힌 것: named volume은 `rm` 뒤에도 남고 새 컨테이너(ID 다름)에서 `hello`가 조회됨, 없는 볼륨 이름을 주면 `run`이 만든다, `Mountpoint`가 리눅스 경로, 컨테이너를 지워도 bind mount 파일은 남는다.

실측: Windows 경로에서도 `-v`가 없는 호스트 디렉터리를 만든다. `\\wsl$\docker-desktop\var\lib`에는 `misc`만 있고 볼륨 경로가 보이지 않는다. postgres 18.6 이미지의 VOLUME은 `/var/lib/postgresql`, PGDATA는 `/var/lib/postgresql/18/docker`. 볼륨이 있는 상태의 재실행 로그에 `Skipping initialization`.

면접: Q1(데이터 보존)은 좋음. Q2(named vs bind)는 처음에 저장 위치만 답했고, 빈칸 채우기로 복사/가림과 용도를 답했다. Q3(Windows 드라이브 bind mount)는 "VM 경계"와 inotify가 빠졌고, 소스 코드 대안으로 named volume을 댔다(정답: WSL 리눅스 파일 시스템).

## Implications
- 3회차 회상 퀴즈: 빈 bind mount가 403을 낸 이유, Q3 재답(VM 경계 + 소스는 WSL 파일 시스템).
- 3회차 postgres는 `-v pgdata:/var/lib/postgresql`로 다시 띄운다. 이미 초기화돼 있어 `POSTGRES_*`는 무시되고 비밀번호는 `pw` 그대로다.
- 8회차: bind mount가 양방향이라 마운트 범위가 곧 컨테이너가 고칠 수 있는 범위다. D-10을 근거로 쓴다.
- 면접 답이 "어디에"에서 멈춘다. "무엇이 다르게 동작하나 + 오늘 본 근거"까지 요구한다.
