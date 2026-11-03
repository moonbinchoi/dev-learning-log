# 사용자 정의 bridge의 차이를 "포트가 열림"으로 오해했다: 차이는 이름 DNS

3회차(2026-10-14). A(publish·EXPOSE·`-P`) → B(기본 bridge, 이름 실패·IP 성공) → C(`labnet`에 `network connect`, 이름 성공)를 예측 후 실행했다.

- A-1: `-p` 없는 nginx의 `PORTS`가 비어 있고 `localhost:80`이 열린다고 예측했다. 결과는 `80/tcp`, 안 열림.
- A-2: "EXPOSE는 문서"라고 말하면서 "옵션이 없으면 EXPOSE 포트를 연다"고 했다. A-1 결과로 반박했다.
- A-3: `docker port`가 한 줄이라 예측했다. IPv4(`0.0.0.0`)·IPv6(`[::]`) 두 줄.
- A-4: `-P`의 호스트 포트를 80으로 예측했다. 결과는 32768. `ExposedPorts`에서 컨테이너 포트를 읽는다는 예측은 맞았다.
- B-6: 이름 접속 실패는 맞혔으나 근거를 "기본 bridge끼리 연결 안 됨"이라 했다. B-7(IP로 성공)로 교정.
- C-8: 네트워크마다 IP를 따로 받는 것은 맞혔고, "같은 대역"은 틀렸다(172.17 vs 172.18).
- C-9 근거 되묻기와 면접 Q2에서 "사용자 정의 bridge 안에서만 모든 포트가 열린다"를 두 번 말했다. B-7이 반증이다. 되묻기에서는 힌트 뒤 "이름으로 IP를 알 수 없다"에 도달했다.

실측: `-P`의 `docker port` 출력은 IPv4 한 줄뿐이었다(`-p 8081:80`은 두 줄). 원인은 문서에서 찾지 못했다. 기본 bridge 옵션에 `enable_icc: true`, `host_binding_ipv4: 0.0.0.0`.

면접: Q1(EXPOSE vs publish)은 핵심만 맞음, 근거·명령·`-P` 예외 빠짐. Q2(왜 사용자 정의 bridge)는 DNS 맞음, 포트 오해, 격리·IP 동적 배정·구체적 JDBC URL 빠짐. Q3(2회차 Q3 세 번째)은 소스 위치(WSL 리눅스 파일 시스템)와 named volume이 안 맞는 이유는 맞음, inotify는 세 번째로 빠짐.

## Implications
- 4회차 회상 퀴즈: 두 bridge의 차이 세 가지(포트는 차이가 아님을 B-7로), Windows bind mount가 느린 이유 두 가지(VM 경계 + inotify).
- 4회차 앱의 DB 주소는 `jdbc:postgresql://pg:5432/docker_lab`. 앱 컨테이너를 `--network labnet`으로 띄운다. postgres는 `--network labnet -v pgdata:/var/lib/postgresql`로 다시 띄운다.
- 면접 답에 근거를 붙이기 시작했지만 명령·값 같은 구체성이 빠진다. 계속 요구한다.
