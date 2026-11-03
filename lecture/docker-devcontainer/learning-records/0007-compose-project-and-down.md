# 프로젝트 이름을 서비스 이름과 헷갈렸고, `compose.yaml`은 사용법을 받은 뒤에야 썼다

5회차(2026-10-15). 4회차 `docker run` 두 줄을 `compose.yaml`(app `build: .`, db `postgres:18` + healthcheck + named volume)로 옮기고, config → up → ps → 브라우저 → 재 up → down → down -v를 예측 후 실행했다.

- 회상: Q1(RUN이 COPY 위, jar만 바뀜)에서 "RUN 캐시, COPY 재실행"은 맞히고 "15초 뒤 COPY"라고 덧붙였다. Q2는 처음에 "기본 bridge라서", 재답에서 `localhost`=자기 자신은 맞혔지만 "`-p`로 8080만 열려 5432가 닫혔다"고 했다. 호스트→컨테이너(`-p`), 자기 루프백, 같은 네트워크 컨테이너의 세 갈래 그림으로 교정하자 "db에 ports 없을 때 app→db:5432 됨(같은 네트워크), 호스트→5432 안 됨(-p)"을 맞혔다.
- 작성: 조건만 준 첫 레슨으로는 `compose.yaml`을 쓰지 못했다(문법·값 없음). 문법·다른 앱 예시·옵션 변환표를 받은 뒤 썼다. 리뷰에서 environment 목록/맵 섞기(`- KEY: value`), 서비스 이름 `pg`와 참조 `db` 불일치, 서비스 볼륨 `pg_data`와 선언 `pgdata` 불일치를 고쳤다. 자동완성이 넣은 healthcheck 값(timeout 30s, retries 5, start_period 30s)을 기본값으로 알고 있었다.
- B-3: `name:`을 `db`, 네트워크를 `db_default`로 예측했다. 실제 `docker-lab`(폴더 이름), `docker-lab_default`. 프로젝트와 서비스를 구분하지 못했다.
- B-4: db가 `Healthy`(5.8초) 된 뒤 app `Started`(5.9초)를 `service_healthy`를 근거로 맞혔다. 이미지 `docker-lab-app`, 컨테이너 `docker-lab-<서비스>-1`을 출력으로 확인했다(문서에서는 못 찾음).
- B-5: `STATUS`에 "n minutes ago"를 예측했다(실제 `Up 2 minutes (healthy)`, "ago"는 CREATED 칸). db가 `docker-lab_pgdata`를 쓴다는 것은 근거까지 맞혔다.
- B-6: 500 오류를 "연결 안 됨"으로 봤다가 로그의 `relation "memo" does not exist`를 읽고 "새 볼륨이라 빈 DB"로 스스로 고쳤다. D-9에서는 힌트 뒤 "연결은 되고 DB는 있지만 테이블이 없다"까지 정밀하게 말했다.
- C-7: 파일을 안 바꾼 재 `up`에서 app은 `Running`(유지). db는 파일 변경 없이 재생성됐다(`docker events`로 확인, 원인 미확인).
- D-8: `down` 뒤 `ps -a`에 지워진 컨테이너가 보인다고 예측했다. `down`은 Removed다. 볼륨 유지·네트워크 삭제·재 up 시 데이터 유지는 맞혔다.

면접: Q1(볼륨 접두사)은 핵심 맞음, `external`을 `extend`로 말함, "항상"은 과함(`name:`이면 접두사 없음), 폴더 이름→프로젝트 이름 근거 빠짐. Q2(down vs down -v)는 대상 맞음, "설정이 바뀌면 down"이라 함(`up`이 비교해 다시 만든다), `down -v`의 용도(DB 초기화)를 몰랐다. Q3(service_healthy)는 동작만 말하고 "시작 ≠ 준비"를 말하지 않았다. 세 답 모두 오늘 본 출력·숫자를 넣지 않았다.

## Implications
- 6회차 회상 퀴즈: `compose.yaml`이 `projects/docker-lab/`에 있을 때 만들어지는 네트워크·볼륨 이름(프로젝트 vs 서비스), `down`과 `down -v` 뒤 각각 남는 것.
- 6회차 `devcontainer.json`은 처음 쓰는 형식이다. 문법·다른 예시·변환표를 레슨에 먼저 넣는다(operating-rules "레슨 설계").
- 면접 답에 출력·숫자를 넣으라는 요구를 질문 문장에 박아도 넣지 않았다. 답을 받은 뒤 "근거가 된 출력 한 줄은?"을 되묻는다.
