# NOTES

## 강의 방식
- 미니 프로젝트 "상품 주문 관리 서비스"(`shop`) 하나를 끝까지 만든다. 문제→해결 진화형 설명은 면접에서 "왜?"를 묻는 부분에만 쓴다.
- 회차는 다음 순서로 진행한다.
  1. 지난 회차 내용으로 회상 퀴즈 1~2개를 낸다. 문항은 준비 폴더 `quiz-draft.md`의 것을 그대로 또는 고쳐서 쓴다. 첫 회차는 생략한다. 회차 사이가 며칠 이상 벌어졌으면 퀴즈 전에 앞 회차 요약(이번 회차가 기대는 회차는 자세히)을 채팅으로 준다.
  2. 레슨은 `/prepare-lesson spring-backend` 세션이 `lessons/`에 HTML로 만들고 [lesson-review.md](../../docs/learning/lesson-review.md) 검토까지 끝낸다. 강의 세션은 `operating-rules.md` 강의 세션 규칙 2번의 확인을 거친 뒤 레슨을 연다. 레슨의 맨 앞 절은 "동작 원리"(등장 객체의 역할표, 요청 1건의 번호 붙은 흐름)다. 이어서 실습 과제, 교재 해당 장(1차 자료)을 담는다.
  3. 동작 모델: 역할표와 흐름을 그림과 함께 채팅에서 설명한다. 흐름은 5~7단계로 나누고 누가 검사하고 누가 분기하는지 말한다.
  4. 함께 따라가기: 요청 하나를 단계마다 함께 추적한다. 각 단계에서 객체에 어떤 값이 들어 있는지 표로 본다.
  5. 직접 추적: 사용자가 다른 요청으로 같은 표를 채우고, "누가 검사하고 누가 분기하는가" 같은 역할 질문에 자기 말로 답한다. 답하지 못하면 코딩으로 넘어가지 않는다.
  6. 핵심 동작은 실행 전에 결과를 예측하게 한다. 코드의 뜻이 아니라 결과를 묻는다.
  7. 사용자가 `shop`에서 `git switch -c lesson-NN`으로 회차 브랜치를 만들고 직접 코딩한다. teach의 브라우저 퀴즈 대신 이 실습이 skill 연습이다.
  8. reviewer가 [grading.md](../../docs/learning/grading.md)로 채점하고, 그 결과와 `git diff`로 사용자와 리뷰 대화를 한다.
  9. 면접 질문 2~3개를 묻고 답을 평가한다. 문항은 `quiz-draft.md`의 것을 그대로 또는 고쳐서 쓴다. 개념·원인·원리로 평가하고, 코드 줄의 정확한 문법까지 외우게 하지 않는다.
- 강의 중 질문에 답할 때는 준비 폴더 `sources.md`에서 그 주제의 줄을 찾아 그 범위나 URL부터 읽는다. 답에 모자라면 같은 파일 안에서 앞뒤로 넓혀 읽는다. 주제가 목록에 없으면 없다고 말하고, `sources.md`에 적힌 교재 파일과 공식 문서 페이지 안에서 그 주제 부분만 찾아 읽는다.
- 도식과 이미지는 교재 원문이나 인용할 수 있는 공식 자료(Spring 등)의 것을 먼저 쓴다. 없을 때만 직접 그린다. 링크로 보내지 않고 레슨과 강의 중에 사용자가 바로 보게 넣고, 그림 아래에 출처를 적는다.
- 교재 그림은 `courses/*/docs/*_images/`에 있다. 트랙의 `assets/images/`에 복사해 레슨에 넣는다. 흰 배경 그림은 다크 모드에서도 흰 바탕에 둔다. 교재는 유료 자료이므로 그림이 든 레슨을 Artifact로 게시하지 않는다.
- 채팅에는 이미지가 표시되지 않는다(2026-11-02 시험, 사용자 환경). 강의 중에는 `code <이미지 경로>`로 에디터 탭에 열고, 채팅에는 같은 흐름을 코드 블록 도식으로 적는다.
- 직접 그릴 때는 D2를 쓴다. 소스는 `assets/diagrams/<이름>.d2`이고 첫 줄은 `...@lesson-theme`이다. 파스텔 역할 색(`input`·`step`·`fail`·`data`·`done`·`stop`·`ask`), 묶음(`group`), 선(`flow`·`save`·`off`) 클래스를 쓴다. 폭이 720을 넘으면 내용을 줄이거나 그림을 나눈다. 720이면 500px 화면의 글자가 약 9px이다.
  - 만들기: 레슨에 `<!-- d2:<이름> --><!-- /d2 -->`를 두고 `python docs/learning/render-diagram.py lecture/spring-backend/assets/diagrams/<이름>.d2 <레슨>`을 실행한다. 표시 사이에 SVG가 들어가고, 소스 옆에 강의 탭용 PNG가 생긴다(라이트 색).
  - 단계 보기: `<div class="stepper">` 안에 `<fieldset class="step-tabs">`의 `<input type="radio" name="<그림별 이름>" value="N">`, 그림, `<tr data-step="N">` 표를 둔다. 그림 상자에는 `class: [step; S3]`처럼 `S<N>`을 붙인다. 범례는 `<ul class="legend">`에 역할 이름을 클래스로 준다. 레슨에는 JS를 넣지 않는다.
- 레슨에 "오늘 쓰는 API" 표를 넣는다. 과제에 처음 쓰는 애너테이션·클래스·설정을 한 줄씩 설명한다.
- 채팅 설명은 짧게 쓴다(3회차 피드백: 장황해서 읽히지 않았다). 과제 조건은 완성된 문장이 아니라 클래스 → 메서드 → 필요한 조건 순으로, 모든 조건을 빠짐없이 같은 구조로 적는다.
- 위 단계가 하나 끝날 때마다 아래 "현재 위치"를 갱신한다. 세션은 예고 없이 끊길 수 있다.

### 리마인드 회차(1·2회차)
사용자는 MVC2 1~6장을 외부 강의로 이미 수강했다(`0001`).
- 1단계 회상 퀴즈 자리에 진단 질문 3~5개를 낸다. 그 장의 핵심과 Boot 4 차이를 묻는다.
- 개념 설명은 진단에서 틀리거나 막힌 것만 한다. 동작 모델과 따라가기는 진단 결과와 상관없이 한다. 교재의 V1→V4 진화 과정은 재현하지 않는다.
- 레슨은 동작 원리, 핵심 요약 표, Boot 4.1 차이, 과제 조건만 담는다.
- Java 코드는 사용자가 직접 쓴다. 템플릿 HTML과 `bootstrap.min.css`는 `courses/spring-mvc2/code/`의 예제에서 복사해도 된다.

## 명령 실행
- Claude는 상태를 바꾸지 않는 읽기 명령과 아래 예외만 직접 실행한다(예: `git status|log|diff`, `docker ps|logs|inspect`, `docker volume ls`). 읽기 명령은 다른 명령과 묶지 않는다.
- `./gradlew`, 앱 실행, `shop`의 `git commit`·`git switch`·`git merge`처럼 상태를 바꾸는 명령은 사용자에게 치게 한다.
- 루트 저장소 커밋과 회차 태그만 Claude가 사용자 확인 뒤 실행한다. 커밋은 `CLAUDE.md`의 `## Git` 절차를 따른다.

## 사용자 환경 다루기
- 창 구성: 강의는 호스트 VS Code 창(루트 `E:\Study\Inflearn`)의 Claude 패널, 실습 코딩·빌드·실행은 `projects/shop`을 Dev Containers로 연 컨테이너 창. 소스는 bind mount라 호스트 Claude도 같은 파일을 본다. `./gradlew`와 앱 실행은 컨테이너에서만 한다.
- 컨테이너 창의 터미널 출력은 사용자가 채팅에 붙여 넣는다.
- 레슨은 `code <레슨 경로>`로 VS Code 에디터에 열고, 툴바의 지구본 버튼(Open in Integrated Browser)을 누르라고 안내한다. 외부 브라우저(`start`)로 열지 않는다.
- 앱 화면(`http://localhost:8081`)은 명령 팔레트 "Browser: Open Integrated Browser"나 터미널 링크 Ctrl+클릭으로 연다. 통합 브라우저가 옛 페이지를 캐시로 보여 줄 수 있으니 결과 확인 전 Ctrl+Shift+R을 안내한다.

## 회차 마무리
면접 질문이 끝나면 요청이 없어도 아래를 차례로 한다.
1. "현재 위치"를 "N회차 완료, 다음은 N+1회차"로 바꾸고, 다음 회차로 넘길 내용(못 푼 질문, 리뷰에서 남은 숙제)을 적는다.
2. 학습 기록 조건을 채운 내용은 `learning-records/`에 남긴다.
3. `operating-rules.md` 강의 세션 규칙 7에 따라 트랙 마크다운을 정리하고 그 회차의 `prep/NN/`을 지운다.
4. 컨테이너 창에서 앱을 끄게 한다(Ctrl+C). 컨테이너와 볼륨은 남긴다.
5. `git status`와 `git diff`를 함께 확인한다. 커밋 직전에 확인을 받고, 사용자가 `lesson-NN` 브랜치에 커밋한 뒤 `git switch master`와 `git merge --no-ff lesson-NN`을 친다.
6. 루트 저장소를 `CLAUDE.md`의 `## Git` 절차로 커밋하고, 사용자 확인 뒤 `git tag -a spring-backend/lesson-NN -m "<요약>"`을 실행한다.
7. 다음 회차는 새 세션에서 시작하라고 안내하고, 이 세션은 여기서 끝낸다.

## 교재 읽기
- 교재 경로는 `RESOURCES.md`.
- 교재 전제 버전과의 차이는 각 강좌 README의 '전제 버전'·'Spring Boot 4.1.1 + Java 25와의 차이' 절을 본다. README에서 미확인인 것만 회차에서 공식 문서로 확인한다.

## 개발 환경
- 호스트: Windows 11, VS Code, Docker Desktop(WSL2 백엔드), Dev Containers 확장. 버전은 루트 `versions.toml`을 따른다.
- shop: `E:\Study\Inflearn\projects\shop`, git으로 관리. Group `com.study`, Artifact `shop`, Gradle(Groovy DSL).
- dev container(`.devcontainer/devcontainer.json`, docker-devcontainer 트랙에서 만들어 `master`에 병합): 이미지 `mcr.microsoft.com/devcontainers/java:25-trixie`, 앱 포트는 `containerEnv`의 `SERVER_PORT=8081`과 `forwardPorts` 8081, Gradle 캐시는 볼륨 `shop-gradle-home`.
- docker-devcontainer 트랙의 worktree `projects/shop-docker-devcontainer`(브랜치 `docker-devcontainer`)도 같은 설정이다. 그 트랙은 완료됐으니 그 컨테이너를 같이 띄우지 않는다. 포트 8081이 겹친다.

## 커리큘럼
| 회차 | 강좌·장 | 기능 | 핵심 | 생략·축소 |
|---|---|---|---|---|
| 0 | 준비 | 환경 설치, 프로젝트 생성 | Web, Thymeleaf, Validation, Lombok, DevTools | JDBC·H2는 6회차에 추가 |
| 1 | MVC2 1~5장 (리마인드) | 상품 목록·상세·등록·수정 + 검증 | PRG와 `RedirectAttributes`, `th:object`·`th:field`, Bean Validation, 등록/수정 폼 객체 분리, `BindingResult` 위치. Boot 4 차이: `jakarta.*`, HV 9에서 `org.hibernate.validator.constraints`의 `@NotBlank`·`@NotEmpty` 제거 | 타임리프 기본 문법 전체, 체크박스·라디오·셀렉트, 메시지·국제화, 직접 짜는 검증 V1~V4와 `Validator`, groups, `@ScriptAssert` |
| 2 | MVC2 6장 (리마인드) | 회원 가입, 로그인·로그아웃 | **쿠키만 쓸 때의 보안 문제 → 세션**, `HttpSession`과 `getSession(false)`, `@SessionAttribute`, 타임아웃. `JSESSIONID`를 바꾸면 화면이 어떻게 되는지 예측. Boot 4 차이: `jakarta.annotation.PostConstruct` | 쿠키 로그인 구현, `SessionManager` 직접 구현(설명만), TrackingModes는 설정 한 줄 |
| 3 | MVC2 7장 | 로그인 체크 | 필터 vs 인터셉터, `@Login` ArgumentResolver | — |
| 4 | MVC2 8~9장 | 예외 처리 | 오류 페이지 기본 동작, `@RestControllerAdvice` | `HandlerExceptionResolver` 직접 구현 |
| 5 | MVC2 10~11장 | 상품 이미지 | `MultipartFile` | 타입 컨버터는 `@DateTimeFormat`만 |
| 6 | DB1 1장 | JDBC 저장소 | 순수 JDBC의 반복 코드 체감 | — |
| 7 | DB1 2장 | 커넥션 풀 | HikariCP, DataSource 추상화 | — |
| 8 | DB1 3장 | 구매(재고 + 잔액 차감) | 실패 시 불일치 체험, ACID, 격리 수준, 락 | — |
| 9 | DB1 4장 | 트랜잭션 적용 | 트랜잭션 매니저 → `@Transactional`, 프록시 원리 | TransactionTemplate |
| 10 | DB1 5장 | 예외 전략 | 체크 vs 언체크, 원인 예외 보존 | — |
| 11 | DB1 6장 | 리팩터링 | 스프링 예외 추상화, `JdbcTemplate` | — |
| 마무리 | — | — | 면접 질문 총정리, 포트폴리오용 README | — |

## 공유 파일 변경 요청
- `docs/learning/operating-rules.md` 레슨 설계: 과제 조건을 쓰는 형식 규칙이 없다. 클래스 → 메서드 → 조건 순의 간결한 일관 구조로 쓰라는 규칙을 더한다(3회차 피드백).
- `docs/learning/` 흐름도 도구(`render-diagram.py`, `check-layout.py`): 3회차 레슨의 흐름도(`login-check-flow`, `request-pipeline`)가 여전히 너무 크다는 피드백이다. 그림 높이 700px 이하 규칙이 이 그림들에 적용되지 않은 것으로 보이나 원인은 확인하지 않았다.
- 흐름도와 레슨 HTML 레이아웃의 모범 사례를 웹 검색으로 모아 기준을 만든다(별도 세션).

## 현재 위치
- **3회차 완료(2026-11-10), 다음은 4회차(MVC2 8~9장 예외 처리: 오류 페이지 기본 동작, `@RestControllerAdvice`).** 시작 전에 `shop`의 `lesson-03` 브랜치를 커밋하고 `master`에 `--no-ff`로 병합했는지 확인한다.
  - 4회차 회상 퀴즈 후보(말로 받는다): `postHandle`이 호출되지 않는 경우 둘(`preHandle`이 `false`, 컨트롤러 예외)과 `afterCompletion`이 받는 `ex`(3회차 면접 Q3에서 예외 쪽 이유가 빠졌다), `getSession(false)`를 쓰는 이유, 세션이 있는 것과 세션에 `loginMember`가 있는 것의 차이.
  - 4회차 연결: 3회차에서 인터셉터 제외 경로에 `/error`를 넣었다. 스프링 부트의 오류 페이지도 `DispatcherServlet`을 거쳐 인터셉터를 지나기 때문이라고 말로만 설명했다. 8장에서 오류 페이지 동작을 배울 때 실행으로 확인한다.
  - 코딩에서 이름이 비슷한 API(`hasMethodAnnotation`과 `hasParameterAnnotation`)를 틀렸고, 조건식의 `!`와 질문의 전제(로그인 여부)를 놓친 적이 있다. 처음 쓰는 API는 문서를 먼저 확인하게 하고, 흐름을 추적하기 전에 전제를 말하게 한다.
  - 3회차 남은 일: `getSession()`으로 바꿔 `Set-Cookie`를 보는 실험(A-5)은 실행하지 않고 말로만 확인했다. `supportsParameter`가 항상 `true`일 때 실제로 어떤 파라미터를 가로채는지는 확인하지 못했다.
  - 2회차 남은 일: 타임아웃 실험(`server.servlet.session.timeout=1m`)은 실행하지 않고 정답만 받았다. 앱을 다시 띄우면 메모리 저장소는 비고 `TestDataInit`이 채운다.
  - 1회차에서 남은 일: `BindingResult`를 폼 파라미터 앞에 두면 어떻게 되는지(진단 Q3-c) 실행 확인을 못 했다. `ItemRepository`의 순번은 0부터 시작한다(선택 수정, `MemberRepository`도 같다).
  - 열린 질문(확인 안 됨, 과제가 아니라 실험 주제): `record` 폼 객체가 `th:field`·`BindingResult`와 함께 동작하는가, `void`가 아닌 setter(체이닝)를 스프링과 타임리프가 프로퍼티로 인식하는가.
  - 미확인: 수정 저장 뒤 URL이 `/items/0/edit`로 보였던 1건은 재현되지 않았고 원인을 모른다. 오류 문구가 영어인 이유(컨테이너 로케일로 추정)도 확인하지 않았다.
  - `im-not-ai`: 글쓰기 규칙은 `.claude/rules/korean-humanize.md`(`lecture/**`에서 로드), 검사는 `python .tools/im-not-ai/check-korean.py <파일>`이다. 패턴 수는 판단 재료이고 합격 기준이 아니다. 도입 범위와 갱신·제거 절차는 `.tools/im-not-ai/README.md`에 있다.
- 6회차 전에 정할 것: DB를 어느 컨테이너에서 띄울지. 교재는 H2 서버 모드다. 후보는 dev container를 Compose 방식으로 바꿔 db 서비스를 더하는 것(docker-devcontainer 트랙에서 배운 방식).
