# 로그인 체크: 흐름과 필터·인터셉터 위치는 이해했고, `getSession(false)`와 "세션이 있으면 로그인"은 설명 뒤에 바로잡혔다

3회차에서 필터와 인터셉터가 끼어드는 위치, 로그인하지 않은 사용자의 요청 흐름, `@Login` 리졸버의 구조를 코드로 만들고 실행해 확인했다. 반면 세션의 존재와 로그인 여부를 같은 것으로 보는 오해가 두 번 나왔고, 이름이 비슷한 API와 조건식의 부정을 놓쳤다. 4회차 예외 처리는 인터셉터의 `postHandle`·`afterCompletion`과 `/error` 경로 위에 쌓이므로 이 둘을 다시 확인하고 시작한다.

## Evidence
- 회상 퀴즈: `invalidate()`가 서버 세션만 지운다는 것과 쿠키로 `GET /`을 보내면 `home`이 뜬다는 것은 맞혔다. 검증 실패 때 리다이렉트하지 않는 이유는 PRG의 `addAttribute`와 섞어 답했고, 리다이렉트하면 모델과 `BindingResult`가 사라진다는 이유와 검사·분기의 주체가 빠졌다.
- 직접 추적: 로그인한 사용자의 `GET /items`를 로그인하지 않은 사용자의 흐름으로 답했다(전제를 놓침). `getSession(false)`가 "새 세션을 돌려준다"고 답했고, 인터셉터가 "세션이 `null`이 아니니 `true`"라고 답했다. 설명한 뒤 "쿠키·세션은 있지만 `loginMember`가 없는 요청"은 `false`로 바르게 답했다.
- 예측: `/login`을 제외 경로에서 빼면 무한 리다이렉트가 된다는 것은 맞혔지만 순환 경로(`/login?redirectURL=/login`)는 틀렸다. 필터에서 `!simpleMatch(...)`의 `!`를 놓쳐 화이트리스트 요청의 흐름을 틀렸고, IDE가 넣은 `throw new UnsupportedOperationException`을 남겼다. 쿠키 없는 `/css/*` 요청, 가짜 `JSESSIONID`, `redirectURL` 로그인의 결과는 모두 맞혔다. 브라우저 로그인 폼이 `redirectURL`을 `POST`에 싣는다는 예측도 맞았다.
- 인터셉터 로그 순서 예측은 틀렸다. `LoginCheckInterceptor`의 줄을 `RESPONSE` 뒤에 두고 `postHandle`이 찍힌다고 했으나, 실제는 `preHandle` 두 개 → `false` → 첫 인터셉터의 `afterCompletion`만이었다. 로그로 바로잡혔다.
- `@Login` 리졸버: `supportsParameter`에서 `hasMethodAnnotation`과 `hasParameterAnnotation`을 혼동해 `false`가 되었다. 오류 없이 `@ModelAttribute`가 빈 `Member`를 만들어 로그인하지 않은 요청도 `loginHome`이 나왔다. 이 결과는 고치기 전에 "`loginHome`이 나오는데 멤버 객체는 비어 있을 것"이라고 정확히 예측했다.
- 면접: 필터는 톰캣, 인터셉터는 스프링 MVC 영역에서 끼어든다는 것과 인터셉터의 세 시점을 설명했으나, 핸들러·`ModelAndView`를 받는 것과 경로 패턴 지정이 빠졌다. `getSession(false)`는 빈 세션이 서버에 쌓인다는 이유로 통과했다. `afterCompletion`의 이유는 `preHandle`이 `false`일 때만 답했고 컨트롤러 예외 쪽이 빠졌다. 쿠키는 세션을 가리키는 값이고 쿠키에 데이터를 직접 담으면 변조 위험이 있다고 답해, 2회차의 "세션이 쿠키를 감싼다"는 뒤집힘이 해소되었다.

## Implications
- 4회차에서 `postHandle`이 불리지 않는 경우(`preHandle`이 `false`, 컨트롤러 예외)와 `afterCompletion`의 `ex`를 다시 묻는다. `/error` 제외 경로의 이유를 오류 페이지 동작으로 확인한다.
- 처음 쓰는 API는 코딩 전에 문서의 한 줄을 읽게 한다. 이름이 비슷한 메서드를 구분하지 못했다.
- 흐름을 추적하는 질문에서는 요청의 전제(로그인 여부, 쿠키 유무)를 먼저 말하게 한다.
- 오류 없이 틀리는 코드(`supportsParameter`가 `false`)는 실행 전 예측으로 다룬다. 이번에 예측으로 맞혔다.
