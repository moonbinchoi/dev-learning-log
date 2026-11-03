# im-not-ai 도입 기록

[im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 일부만 가져와 쓴다. MIT 라이선스이고 전문은 `upstream/LICENSE`에 있다. 가져온 커밋은 `versions.toml`의 `im-not-ai` 값이다.

## 쓰는 것

| 파일 | 쓰는 곳 |
|---|---|
| `skills/humanize-korean/references/quick-rules.md` | `.claude/rules/korean-humanize.md`를 만드는 원본. 복사해 두지 않고 `sync.py`가 갱신할 때 클론에서 읽는다. |
| `upstream/scripts/prepare_monolith_input.py`, `console.py` | 패턴 개수 계산 |
| `upstream/skills/humanize-korean/references/metrics.py`, `metrics_v2.py`, `baseline.json`, `baseline_v2.json` | 위 계산이 읽는 지표와 기준값 |
| `upstream/LICENSE` | 라이선스 |

`upstream/` 안의 파일은 고치지 않는다. 고칠 일이 생기면 `sync.py`를 고친다.

## 쓰지 않는 것

- 재작성 파이프라인과 에이전트 9개: 코드와 HTML을 보호하지 않는다.
- 플러그인 설치: `plugin.json` 버전이 2.3.2로 고정돼 업데이트가 오지 않고, 구성 요소를 고를 수 없다. 스킬의 `paths`는 파일을 읽어도 스킬 본문을 싣지 않았다(2026-11-02 시험).
- 규칙 C-2, C-5, C-9, C-10, J-1: 레슨에 필요한 목록, 번호, 표를 없앤다.
- `quick-rules.md`의 자체검증과 등급 절: 재작성 파이프라인의 스크립트에 기대는 내용이다.
- `risk_band`, `route_hint`: 길이에 좌우되고 AI 문체 표본도 low가 나온다.

## 이 폴더 밖에 있는 것

- `.claude/rules/korean-humanize.md`: `sync.py`가 만드는 글쓰기 규칙. `lecture/**` 파일을 읽을 때 로드되며, 자동 로드 때문에 이 자리에 있어야 한다. 손으로 고치지 않는다.
- `docs/learning/lesson-review.md` 항목 11: 레슨 검토에서 `check-korean.py`를 실행한다.
- `versions.toml`의 `im-not-ai`: 가져온 커밋.
- `lecture/spring-backend/NOTES.md`의 `im-not-ai` 줄: 이 파일을 가리킨다.

## 사용

```
python .tools/im-not-ai/check-korean.py <파일>...
```

패턴 수는 판단 재료이고 합격 기준이 아니다. 걸린 문장을 읽고 고칠 것만 고른다.

## 갱신

1. upstream을 임시 폴더에 받는다. 줄바꿈 변환을 끈다.

   ```
   git clone -c core.autocrlf=false https://github.com/epoko77-ai/im-not-ai <임시 폴더>
   ```

2. 시험한다. 프로젝트에는 아무것도 쓰지 않고 추가·삭제된 규칙과 변경된 줄을 보여 준다.

   ```
   python .tools/im-not-ai/sync.py <임시 폴더>
   ```

3. 보고된 규칙 변경을 읽는다. 규칙은 지침으로 로드되므로 읽기 전에 적용하지 않는다.
4. 적용한다. `upstream/`, 규칙 파일, `versions.toml`이 함께 바뀐다.

   ```
   python .tools/im-not-ai/sync.py <임시 폴더> --apply
   ```

5. 확인하고 임시 폴더를 지운다.

   ```
   python .tools/im-not-ai/test_check_korean.py
   ```

`sync.py`는 upstream 구조가 바뀌었거나 네트워크·프로세스 실행 호출이 생기면 아무것도 적용하지 않고 멈춘다. 그때는 바뀐 내용을 읽고 `sync.py`를 고친다.

## 제거

이 폴더와 `.claude/rules/korean-humanize.md`를 지우고, `lesson-review.md` 항목 11, `versions.toml`의 `im-not-ai` 두 줄, `docs/learning/versions.md`의 im-not-ai 행, `NOTES.md`의 `im-not-ai` 줄을 뺀다. 작업 공간이 git이 아니므로 지우면 되돌릴 수 없다.
