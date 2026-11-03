# 사전 지식: MVC 1편 수준, 개발 2년 공백(타 직종 근무)

사용자는 과거에 김영한 「스프링 MVC 1편」 정도까지 공부했고, 2년 동안 다른 직종에서 일하며 개발을 쉬었다. 서블릿, `DispatcherServlet`, `@Controller`/`@RequestMapping` 같은 MVC 1편 내용은 처음부터 가르치지 말고, 회차에서 필요할 때 짧게 리마인드한다.

## 추가(2026-10-23): MVC2 1~6장은 외부 강의로 수강했다

사용자가 「스프링 MVC 2편」 1~6장(타임리프, 메시지·국제화, 검증, 로그인 쿠키·세션)을 외부 강의로 이미 수강했다고 알렸다. 이 장들은 "리마인드"로 판단하고, 7장부터는 "처음"으로 가르친다.

## Implications
- 1·2회차는 리마인드 회차다. 진단 질문에서 틀리거나 막힌 것만 설명한다.
- 수강은 Boot 2~3 기준 교재였으므로 Boot 4 차이(`jakarta.*`, Hibernate Validator 9의 제약 애너테이션 제거, `jakarta.annotation.PostConstruct`)는 수강 여부와 상관없이 짚는다.
- dev container, 볼륨, 포트 forward, git 브랜치·worktree는 docker-devcontainer 트랙에서 배웠다(`docker-devcontainer/0008`, `docker-devcontainer/0009`). 다시 가르치지 않는다.
