# NOTES

## 강의 방식
- 미니 프로젝트 "상품 주문 관리 서비스"(`shop`) 하나를 끝까지 만든다. 문제→해결 진화형 설명은 면접에서 "왜?"를 묻는 부분에만 쓴다.
- 회차는 다음 순서로 진행한다.
  1. 지난 회차 내용으로 회상 퀴즈 1~2개를 낸다. 첫 회차는 생략한다. 회차 사이가 며칠 이상 벌어졌으면 퀴즈 전에 앞 회차 요약(이번 회차가 기대는 회차는 자세히)을 채팅으로 준다.
  2. `lessons/`에 HTML 레슨을 만든다. 맨 앞 절은 "동작 원리"(등장 객체의 역할표, 요청 1건의 번호 붙은 흐름)다. 이어서 실습 과제, 교재 해당 장(1차 자료)을 담는다. [lesson-review.md](../../docs/learning/lesson-review.md)로 검토한 뒤 연다.
  3. 동작 모델: 역할표와 흐름을 그림과 함께 채팅에서 설명한다. 흐름은 5~7단계로 나누고 누가 검사하고 누가 분기하는지 말한다.
  4. 함께 따라가기: 요청 하나를 단계마다 함께 추적한다. 각 단계에서 객체에 어떤 값이 들어 있는지 표로 본다.
  5. 직접 추적: 사용자가 다른 요청으로 같은 표를 채우고, "누가 검사하고 누가 분기하는가" 같은 역할 질문에 자기 말로 답한다. 답하지 못하면 코딩으로 넘어가지 않는다.
  6. 핵심 동작은 실행 전에 결과를 예측하게 한다. 코드의 뜻이 아니라 결과를 묻는다.
  7. 사용자가 `shop`에 직접 코딩한다. teach의 브라우저 퀴즈 대신 이 실습이 skill 연습이다.
  8. reviewer가 [grading.md](../../docs/learning/grading.md)로 채점하고, 그 결과와 `git diff`로 사용자와 리뷰 대화를 한다.
  9. 면접 질문 2~3개를 묻고 답을 평가한다. 개념·원인·원리로 평가하고, 코드 줄의 정확한 문법까지 외우게 하지 않는다.
- 도식과 이미지는 교재 원문이나 인용할 수 있는 공식 자료(Spring 등)의 것을 먼저 쓴다. 없을 때만 직접 그린다. 링크로 보내지 않고 레슨과 강의 중에 사용자가 바로 보게 넣고, 그림 아래에 출처를 적는다.
- 교재 그림은 `courses/*/docs/*_images/`에 있다. 트랙의 `assets/images/`에 복사해 레슨에 넣는다. 흰 배경 그림은 다크 모드에서도 흰 바탕에 둔다. 교재는 유료 자료이므로 그림이 든 레슨을 Artifact로 게시하지 않는다.
- 채팅에는 이미지가 표시되지 않는다(2026-11-02 시험, 사용자 환경). 강의 중에는 `code <이미지 경로>`로 에디터 탭에 열고, 채팅에는 같은 흐름을 코드 블록 도식으로 적는다.
- 직접 그릴 때는 D2를 쓴다. 소스는 `assets/diagrams/<이름>.d2`이고 첫 줄은 `...@lesson-theme`이다. 파스텔 역할 색(`input`·`step`·`fail`·`data`·`done`·`stop`·`ask`), 묶음(`group`), 선(`flow`·`save`·`off`) 클래스를 쓴다. 폭이 720을 넘으면 내용을 줄이거나 그림을 나눈다. 720이면 500px 화면의 글자가 약 9px이다.
  - 만들기: 레슨에 `<!-- d2:<이름> --><!-- /d2 -->`를 두고 `python docs/learning/render-diagram.py lecture/spring-backend/assets/diagrams/<이름>.d2 <레슨>`을 실행한다. 표시 사이에 SVG가 들어가고, 소스 옆에 강의 탭용 PNG가 생긴다(라이트 색).
  - 단계 보기: `<div class="stepper">` 안에 `<fieldset class="step-tabs">`의 `<input type="radio" name="<그림별 이름>" value="N">`, 그림, `<tr data-step="N">` 표를 둔다. 그림 상자에는 `class: [step; S3]`처럼 `S<N>`을 붙인다. 범례는 `<ul class="legend">`에 역할 이름을 클래스로 준다. 레슨에는 JS를 넣지 않는다.
- 레슨에 "오늘 쓰는 API" 표를 넣는다. 과제에 처음 쓰는 애너테이션·클래스·설정을 한 줄씩 설명한다.
- 위 단계가 하나 끝날 때마다 아래 "현재 위치"를 갱신한다. 세션은 예고 없이 끊길 수 있다.

### 리마인드 회차(1·2회차)
사용자는 MVC2 1~6장을 외부 강의로 이미 수강했다(`0001`).
- 1단계 회상 퀴즈 자리에 진단 질문 3~5개를 낸다. 그 장의 핵심과 Boot 4 차이를 묻는다.
- 개념 설명은 진단에서 틀리거나 막힌 것만 한다. 동작 모델과 따라가기는 진단 결과와 상관없이 한다. 교재의 V1→V4 진화 과정은 재현하지 않는다.
- 레슨은 동작 원리, 핵심 요약 표, Boot 4.1 차이, 과제 조건만 담는다.
- Java 코드는 사용자가 직접 쓴다. 템플릿 HTML과 `bootstrap.min.css`는 `courses/spring-mvc2/code/`의 예제에서 복사해도 된다.

## 명령 실행
- Claude는 상태를 바꾸지 않는 읽기 명령만 직접 실행한다(예: `git status|log|diff`, `docker ps|logs|inspect`, `docker volume ls`). 읽기 명령은 다른 명령과 묶지 않는다.
- `./gradlew`, 앱 실행, `git commit`처럼 상태를 바꾸는 명령은 사용자에게 치게 한다.

## 사용자 환경 다루기
- 창 구성: 강의는 호스트 VS Code 창(루트 `E:\Study\Inflearn`)의 Claude 패널, 실습 코딩·빌드·실행은 `projects/shop`을 Dev Containers로 연 컨테이너 창. 소스는 bind mount라 호스트 Claude도 같은 파일을 본다. `./gradlew`와 앱 실행은 컨테이너에서만 한다.
- 컨테이너 창의 터미널 출력은 사용자가 채팅에 붙여 넣는다.
- 레슨은 `code <레슨 경로>`로 VS Code 에디터에 열고, 툴바의 지구본 버튼(Open in Integrated Browser)을 누르라고 안내한다. 외부 브라우저(`start`)로 열지 않는다.
- 앱 화면(`http://localhost:8081`)은 명령 팔레트 "Browser: Open Integrated Browser"나 터미널 링크 Ctrl+클릭으로 연다. 통합 브라우저가 옛 페이지를 캐시로 보여 줄 수 있으니 결과 확인 전 Ctrl+Shift+R을 안내한다.

## 회차 마무리
면접 질문이 끝나면 요청이 없어도 아래를 차례로 한다.
1. "현재 위치"를 "N회차 완료, 다음은 N+1회차"로 바꾸고, 다음 회차로 넘길 내용(못 푼 질문, 리뷰에서 남은 숙제)을 적는다.
2. 학습 기록 조건을 채운 내용은 `learning-records/`에 남긴다.
3. `operating-rules.md` 강의 세션 규칙 7에 따라 트랙 마크다운을 정리한다.
4. 컨테이너 창에서 앱을 끄게 한다(Ctrl+C). 컨테이너와 볼륨은 남긴다.
5. `git status`와 `git diff`를 함께 확인한 뒤 `shop`을 커밋한다. 사용자가 요청한 방식이지만 커밋 직전에 확인을 받는다.
6. 다음 회차는 새 세션에서 시작하라고 안내하고, 이 세션은 여기서 끝낸다.

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

## 현재 위치
- **1회차 완료(2026-11-02), 다음은 2회차(리마인드, MVC2 6장).** 커밋 전이면 먼저 `shop`을 커밋한다.
  - 1회차 피드백 처리(2026-11-02): 회차 순서에 동작 모델·따라가기·직접 추적을 넣었고, `docs/learning/lesson-review.md`에 항목 9~11을 더했다. 2회차 첫 적용이다.
  - `im-not-ai`: 글쓰기 규칙은 `.claude/rules/korean-humanize.md`(`lecture/**`에서 로드), 검사는 `python .tools/im-not-ai/check-korean.py <파일>`이다. 패턴 수는 판단 재료이고 합격 기준이 아니다. 도입 범위와 갱신·제거 절차는 `.tools/im-not-ai/README.md`에 있다.
  - 도식 도구는 D2로 정했다(2026-11-02). Figma는 도입하지 않았다. 손으로 고칠 캔버스가 필요해지면 `@next-ai-drawio/mcp-server`를 먼저 본다. 근거: `.scratch/lesson-diagrams/`.
  - 2회차 시작 전: 10일 넘게 비면 앞 회차 요약을 먼저 준다. 앱을 다시 띄우면 메모리 저장소는 비어 있다.
  - 2회차 회상 퀴즈(말로 받는다): 검증 실패 때 왜 리다이렉트하지 않는가, `Item`에 `@NotBlank`를 달면 검증되는가, 타입 오류에서 `BindingResult` 유무에 따른 결과와 상태 코드(400과 500의 구분), `addAttribute`의 값이 URL에서 어디로 가는가.
  - 남은 일: `BindingResult`를 폼 파라미터 앞에 두면 어떻게 되는지(진단 Q3-c) 실행 확인을 못 했다. `ItemRepository`의 순번은 0부터 시작한다(선택 수정). `reference/form-validation.html`은 채점 뒤 공개했다.
  - 미확인: 수정 저장 뒤 URL이 `/items/0/edit`로 보였던 1건은 재현되지 않았고 원인을 모른다. 오류 문구가 영어인 이유(컨테이너 로케일로 추정)도 확인하지 않았다.
- 6회차 전에 정할 것: DB를 어느 컨테이너에서 띄울지. 교재는 H2 서버 모드다. 후보는 dev container를 Compose 방식으로 바꿔 db 서비스를 더하는 것(docker-devcontainer 트랙에서 배운 방식).
