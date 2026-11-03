# Plan: 프로젝트 에이전트 구성 재설계

Source: [spec.md](spec.md)

메인 세션이 직접 한다. `.claude/` 아래 쓰기가 섞여 있고(C5), 고칠 파일이 10개 미만이다.

1. R7 hook: `grader-guard*.js`를 `practice-guard*.js`로 바꾸고 판정·메시지·테스트를 고친 뒤 `settings.json` 경로를 바꾼다. 확인: `node .claude/hooks/practice-guard.test.js` → `practice-guard: ok`.
2. R1-R4 문서: `operating-rules.md` 위임 절, `lesson-review.md:7`, `grading.md` 생성.
3. R5-R6 에이전트: `grader.md` 삭제, `source-reader.md`·`visual-reviewer.md` 재작성.
4. R8 삭제: `docs/superpowers/`.
5. 확인: R1 grep 0건, R9 파일 변경 없음.
