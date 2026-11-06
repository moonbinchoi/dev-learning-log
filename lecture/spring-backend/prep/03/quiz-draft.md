# 3회차 퀴즈 초안

## 회상 퀴즈
- Q: 로그인한 브라우저에서 로그아웃(`session.invalidate()`)을 하면, 지워지는 것은 서버의 세션인가 브라우저의 `JSESSIONID` 쿠키인가? 로그아웃 뒤 같은 쿠키로 `GET /`을 보내면 어느 화면이 뜨는가?
  - 모범 답: 서버 세션 저장소의 세션만 지워진다. 브라우저 쿠키는 그대로 남는다. 그 쿠키로 `GET /`을 보내면 서버가 그 ID로 세션을 찾지 못해 `@SessionAttribute`가 `null`이 되고 `home`(로그인 전 홈)이 뜬다.
- Q: 검증 오류가 있을 때 컨트롤러는 왜 리다이렉트하지 않고 폼 뷰를 바로 그리는가? 그리고 검사하는 쪽과 분기하는 쪽은 각각 누구인가?
  - 모범 답: 리다이렉트는 브라우저가 보내는 새 요청이라 모델에 담긴 입력값과 `BindingResult`의 오류가 사라진다. 같은 요청 안에서 뷰를 그려야 입력값과 오류 메시지를 다시 보여 줄 수 있다. 검사는 `@Validated`가 붙은 파라미터에 대해 Bean Validation이 하고 결과를 `BindingResult`에 담는다. 분기는 컨트롤러 코드가 `hasErrors()`로 한다.

## 면접 질문
- Q: 서블릿 필터와 스프링 인터셉터는 무엇이 다른가? 로그인 체크에는 무엇을 쓰겠는가?
  - 모범 답: 필터는 서블릿 표준 기술로 `DispatcherServlet` 앞에서 동작하고 `request`·`response`만 받는다. 인터셉터는 스프링 MVC 기술로 `DispatcherServlet`과 컨트롤러 사이에서 동작하고, 호출될 핸들러와 `ModelAndView`까지 받는다. 인터셉터는 `preHandle`·`postHandle`·`afterCompletion`으로 시점이 나뉘고, `addPathPatterns`·`excludePathPatterns`로 적용·제외 경로를 정밀하게 지정할 수 있다. 필터만 `chain.doFilter`에 다른 `request`·`response` 객체를 넘겨 바꿀 수 있다. 스프링 MVC를 쓰고 필터가 꼭 필요한 이유가 없으면 로그인 체크는 인터셉터가 편하다. 제외 경로를 코드 대신 설정으로 두고 `preHandle`만 구현하면 된다.
- Q: 로그인 체크에서 `request.getSession()` 대신 `getSession(false)`를 쓰는 이유는 무엇인가?
  - 모범 답: 로그인 체크는 세션을 찾기만 하는 곳이다. `getSession()`은 세션이 없으면 새로 만들기 때문에, 로그인하지 않은 방문자가 보호된 주소를 열 때마다 쓸모없는 세션이 서버 메모리에 생기고 응답에 `Set-Cookie`가 붙는다. `getSession(false)`는 없으면 `null`을 돌려주므로 세션을 만들지 않는다. 세션을 만드는 곳은 로그인 성공 처리 한 곳뿐이다.
- Q: 인터셉터에서 요청 종료 로그를 `postHandle`이 아니라 `afterCompletion`에 두는 이유는 무엇인가?
  - 모범 답: 컨트롤러에서 예외가 나면 `postHandle`은 호출되지 않는다. `afterCompletion`은 뷰 렌더링 뒤에 예외 여부와 상관없이 불리고 예외를 `ex` 파라미터로 받는다. 단, 그 인터셉터의 `preHandle`이 `true`를 돌려준 경우에만 불린다.
