# 버전 관리

버전의 기준은 루트 `versions.toml`(Gradle version catalog) 하나다. 버전을 바꿀 때는 이 파일부터 고친다.

## 버전을 읽는 곳

| 대상 | 읽는 방식 |
|---|---|
| `courses/*/code/*` | `settings.gradle`의 `dependencyResolutionManagement { versionCatalogs { libs { from(files('../../../../versions.toml')) } } }` |
| `projects/*` | 복사본 `gradle/libs.versions.toml`. 각 프로젝트는 독립 repo이고, 컨테이너에는 프로젝트 폴더만 마운트되기 때문이다. |
| Gradle wrapper | 읽지 못한다. `./gradlew wrapper --gradle-version <gradle 값>`을 두 번 실행한다. 두 번째 실행에서 jar와 스크립트가 바뀐다. |
| Dockerfile, `compose.yaml`, `devcontainer.json`의 이미지 태그 | 읽지 못한다. 태그를 직접 적고, 같은 값을 `versions.toml` `[versions]`에 등록한다. |
| D2 CLI(`.tools/d2/d2.exe`) | 읽지 못한다. [GitHub 릴리스](https://github.com/terrastruct/d2/releases)의 `windows-amd64` 압축 파일을 `SHA256SUMS`로 확인해 넣고, 같은 값을 `versions.toml`의 `d2`에 등록한다. `render-diagram.py`가 실행할 때 둘을 대조한다. 도식 작업이 막힐 때만 올린다. |
| im-not-ai(`.tools/im-not-ai/upstream/`) | 읽지 못한다. [갱신 절차](../../.tools/im-not-ai/README.md)대로 `sync.py --apply`를 실행하면 `versions.toml`의 `im-not-ai`도 함께 바뀐다. |

`build.gradle`의 플러그인은 `alias(libs.plugins.spring.boot)`와 `alias(libs.plugins.spring.dependency.management)`로 쓰고, toolchain은 `JavaLanguageVersion.of(libs.versions.java.get())`로 쓴다. 라이브러리 버전은 Boot BOM에 맡긴다.

## 새 Gradle 프로젝트

`projects/`에 Gradle 프로젝트를 만들면 첫 커밋 전에 한다.

- `versions.toml`을 `gradle/libs.versions.toml`로 복사한다.
- `build.gradle`을 위 방식으로 바꾼다.
- wrapper를 `gradle` 값에 맞춘다.
- `.devcontainer/devcontainer.json`을 [track-design.md](track-design.md) 7단계대로 둔다.
- 완료: dev container 안에서 `./gradlew build`가 통과한다.

## 버전 점검

새 강좌를 도입할 때 [course-intake.md](course-intake.md)의 "분석" 다음에 한다.

1. 공식 문서에서 Spring Boot, dependency-management 플러그인, Gradle의 최신 안정판과 Java 최신 LTS를 확인한다. `versions.toml`에 등록된 이미지 태그도 확인한다.
2. 메이저 버전이 바뀌면 고치기 전에 사용자에게 묻는다. 소스 코드 이전이 따라온다.
3. `versions.toml`을 고친다.
4. 복사본을 갱신한다: `for d in projects/*/; do [ -f "$d/build.gradle" ] && cp versions.toml "$d/gradle/libs.versions.toml"; done`
5. `gradle` 값이 바뀌었으면 모든 프로젝트의 wrapper를 갱신한다.
6. 이미지 태그가 바뀌었으면 `grep -rn '<이전 태그>' projects/`로 찾아 바꾼다.
7. 새 강좌의 `code/*`를 현재 기준으로 옮긴다.
   - 원본을 `courses/<course>/code-<원래 Boot 버전>-backup.tar.gz`로 남긴다.
   - wrapper를 교체하고, `settings.gradle`과 `build.gradle`을 위 방식으로 바꾼다.
   - 강좌 README의 "현재 최신 안정 버전과의 차이"대로 소스를 고친다. 기능이 없어져 대체할 방법이 없으면 고치지 않고 사용자에게 보고한다.
8. 어긋남을 검사한다. 세 명령 모두 출력이 없어야 한다.
   - `for d in projects/*/; do [ -f "$d/build.gradle" ] && { cmp -s versions.toml "$d/gradle/libs.versions.toml" || echo "$d"; }; done`
   - `grep -L "alias(libs.plugins.spring.boot)" projects/*/build.gradle courses/*/code/*/build.gradle`
   - `grep -L "gradle-<gradle 값>-bin" projects/*/gradle/wrapper/gradle-wrapper.properties courses/*/code/*/gradle/wrapper/gradle-wrapper.properties`
9. worker로 `courses/*/code/*`와 `projects/*`의 모든 Gradle 프로젝트에서 `./gradlew build`를 실행한다. `projects/*`는 컨테이너를 띄운 뒤 `devcontainer exec --workspace-folder <프로젝트 경로> ./gradlew build`로 컨테이너 안에서 실행한다. 사용자가 작성 중인 실습 코드의 컴파일 오류는 고치지 않고 보고한다. 고치지 못한 강좌 예제의 실패는 그 강좌 README의 "예제 코드 상태"에 적는다.
10. 프로젝트 repo의 커밋은 사용자에게 확인한 뒤 한다.

- 완료: 8의 출력이 없고, 9의 빌드가 모두 통과했거나 실패 원인이 기록·보고됐다.

저장소를 GitHub에 올리면 Renovate로 바꿀지 다시 검토한다. Renovate는 저장소마다 버전 업데이트 PR을 자동으로 올린다.
