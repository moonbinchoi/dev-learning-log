"""check-korean.py와 sync.py의 규칙 생성을 확인한다. 사용: python .tools/im-not-ai/test_check_korean.py"""
import importlib.util
import pathlib
import tempfile

HERE = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check = load("check-korean")
sync = load("sync")

with tempfile.TemporaryDirectory() as tmp:
    page = pathlib.Path(tmp) / "page.html"
    page.write_text(
        "<head><title>제목</title></head><p>문장 <code>getName()</code> 끝</p>"
        "<pre><code>Item item = new Item();</code></pre><svg><text>그림</text></svg>",
        encoding="utf-8")
    assert check.prose(page) == "문장 코드 끝"

    note = pathlib.Path(tmp) / "note.md"
    note.write_text("# 제목\n\n- `code` 항목\n\n```java\nint a;\n```\n", encoding="utf-8")
    assert check.prose(note) == "제목\n\n코드 항목"

    clone = pathlib.Path(tmp) / "clone"
    (clone / "skills/humanize-korean/references").mkdir(parents=True)
    (clone / "LICENSE").write_text("MIT\n", encoding="utf-8")
    quick = clone / sync.QUICK_RULES
    quick.write_text(
        "**Do-NOT 보호**\n\n**서법 보존 유지**\n\n**내용 앵커 유지**\n\n---\n\n"
        "## A. 번역투\n\n- **A-1** 규칙\n- **C-2** 뺄 규칙\n\n## 자체검증 체크리스트\n\n버릴 내용\n",
        encoding="utf-8")
    rule = sync.build_rule(clone, "abc1234")
    assert "commit abc1234" in rule and "- **A-1** 규칙" in rule
    assert "- **C-2**" not in rule and "버릴 내용" not in rule
    assert sync.rule_ids(rule) == {"A-1"}

    quick.write_text("## A. 번역투\n", encoding="utf-8")
    try:
        sync.build_rule(clone, "abc1234")
    except ValueError:
        pass
    else:
        raise AssertionError("구조가 바뀐 규칙 파일을 통과시켰다")

clean = check.scan("컨트롤러는 요청을 받아 상품을 저장한다.")
tells = check.scan(sync.SAMPLE)
assert clean["tells"] == 0, clean
assert tells["tells"] > 0 and tells["hits"], tells
print("OK")
