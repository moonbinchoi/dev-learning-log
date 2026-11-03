# 사전 지식: Docker 처음, 셸·네트워크 기초는 앎

Docker, Compose, Dev Container는 모두 처음이다(2026-10-07 인터뷰). 반면 bash 기본(파일 다루기, `chmod`, 환경 변수, 파이프)과 네트워크 기초(IP, 포트, DNS 이름 풀이)는 쓸 줄 알아 다시 가르치지 않는다. git은 commit/push까지만 써 봤으므로 브랜치, worktree, `git diff` 리뷰는 필요한 회차에서 처음부터 가르친다.

## Implications
- Spring은 MVC 1편 수준이다(spring-backend/0001). docker-lab 앱은 Spring Boot로 만들되 Spring 설명은 하지 않는다.
- 네트워크 회차는 포트 개념 대신 "컨테이너마다 네트워크가 따로 있다"는 점과 Docker 내장 DNS에 집중한다.
