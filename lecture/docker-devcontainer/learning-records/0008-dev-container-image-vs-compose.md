# dev container의 동작은 맞히고, 근거로 "쓰기 레이어 vs 볼륨"과 "프로젝트 이름 → 볼륨 재사용"을 구분하지 못했다

6회차(2026-10-15~16). docker-lab에 `devcontainer.json`을 image 방식(`java:25`, `forwardPorts` 8081, `containerEnv` SERVER_PORT)으로 쓰고, 이어서 루트 `compose.yaml`에 `dev` 서비스(sleep infinity, 소스 bind mount, `gradle-cache` 볼륨)를 더해 Compose 방식으로 바꿨다. 실습 창은 `code -n`으로 따로 열었다.

- 회상: Q1 `docker-lab_default`·`docker-lab_pgdata`와 "앞부분은 프로젝트 이름"을 맞혔고, 프로젝트 이름이 폴더 이름에서 온다는 근거는 빠졌다. Q2 `down`/`down -v`와 `down -v`의 용도("새 DB, 테스트 초기화")를 맞혔다(5회차에는 몰랐다).
- 작성: image 방식 `devcontainer.json`은 문법·예시·조건표를 받고 한 번에 통과했다. Compose 방식에서는 environment에 `- KEY: value`(5회차와 같은 실수), 최상위 `gradle-cache:` 누락, `compose.yml`, `/workspace/`, JSON 끝 쉼표를 고쳤다. 오타·누락 3건은 이름 대조를 안 한 것이다.
- B-4: COMMAND를 `bash`로 예측했다(실제 Dev Containers의 `while sleep 1` 반복문, `overrideCommand`). running은 맞혔지만 근거를 "VS Code를 열어서"라 했다. 주 프로세스가 끝나지 않아서 running이고, 그래서 VS Code가 붙을 수 있다는 순서로 교정했다.
- B-5: `whoami`를 `root`로 예측했다(실제 `vscode`, 이미지 라벨 `remoteUser`). JDK는 힌트(마운트는 프로젝트 폴더 하나뿐, `JAVA_HOME`) 뒤 "이미지 안 JDK"로 맞혔다(Microsoft OpenJDK 25.0.4.1).
- B-6: "Started까지 뜨고 브라우저에서 오류"를 맞혔다. HikariPool이 첫 요청 때 연결한다는 것은 로그 시각으로 보였다. `80% EXECUTING > :bootRun`을 멈춘 것으로 오해했다.
- B-7·C-11·C-12: B-7("다시 만들면 사라진다")은 맞혔다. C-11 "다시 받는다"는 결과는 맞았지만 근거를 "쓰기 레이어가 사라져서"라 했다(실제는 C-9에 새로 생긴 빈 볼륨). C-12는 "모르겠다"였다가 질문을 둘(볼륨은 컨테이너 삭제에도 남는다 / gradle-cache는 C-9에 처음 생겼다)로 나누자 "받지 않는다"를 맞혔다.
- C-9: `runServices`를 놓쳐 `app`까지 3개로 예측했다. 볼륨 구분자를 `-`로 썼다. `docker-lab_pgdata`를 "external이 없어서 새로 만든다"고 했다(실제 재사용). external을 "이 프로젝트가 만든 볼륨이 아닌 것"이 아니라 "다시 쓰기 위한 옵션"으로 알고 있었다.
- D-13: `stopCompose`로 둘 다 멈춘다는 것을 근거까지 맞혔다. 처음에는 창을 닫지 않고 Ctrl+C만 했다.

실측으로 확인한 것(문서에 없음): image 방식 기본 작업 경로 `/workspaces/<폴더>`, 루트 `compose.yaml`을 쓰면 Dev Containers의 Compose 프로젝트 이름이 폴더 이름(`docker-lab`), Rebuild는 VS Code가 붙는 서비스(`dev`)만 다시 만들고 `db`는 둔다, 창을 닫으면 둘 다 `Exited (137)`(유예 없이 같은 초에 kill), E: 드라이브 bind mount에서 `./gradlew` 실행 비트 문제 없음, 볼륨 `vscode → /vscode`에 VS Code Server가 든 것으로 보임(프로세스 목록 기준).

면접: Q1(이미지 실행 vs dev container)은 "컨테이너에 접속해 파일을 다룬다"만 말했다. 안에 든 것·주 프로세스·코드 변경 반영의 차이가 빠졌고, "컨테이너 위에서 앱을 동작"이라 해 앱이 주 프로세스라는 점을 놓쳤다. Q2(Gradle 캐시 볼륨)는 "Rebuild는 컨테이너를 지우고 다시 만든다"는 핵심을 맞혔다. 쓰기 레이어와 bind mount 대안이 빠졌다. 되묻자 "볼륨 있을 때 Welcome 없음"은 출력으로 댔고, 볼륨 없을 때의 출력(`No such file or directory`)은 대지 못했다. Q3(forward vs publish)는 `Ports={}`인데 브라우저가 됐다는 실측을 근거로 잘 답했다.

## Implications
- 7회차 회상 퀴즈: (1) Rebuild 뒤 `~/.gradle`이 쓰기 레이어일 때와 볼륨일 때 각각 남는지와 그 근거, (2) 루트 `compose.yaml`의 `pgdata`가 5회차 볼륨을 다시 쓴 이유(프로젝트 이름 → 볼륨 이름, external의 뜻).
- 7회차 shop `devcontainer.json`도 사용자가 쓴다. 쓰기 전에 "서비스·볼륨·경로 이름을 두 파일에서 대조한다"를 체크 항목으로 준다(이번 오타 3건과 5회차 이름 불일치가 같은 종류다).
- 예측 근거가 "결과는 맞고 이유는 다른" 경우가 반복됐다(B-4, C-11). 다음 단계가 그 근거를 시험하도록 예측을 이어 붙이면 스스로 발견했다(C-11 → C-12). 이 방식을 계속 쓴다.
- 면접 답에 출력을 넣으라는 되묻기는 이번에 절반 효과가 있었다. 계속 되묻는다.
