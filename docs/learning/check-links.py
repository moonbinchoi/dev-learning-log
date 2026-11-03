"""레슨 HTML의 외부 링크 상태와 `#` 조각의 id·name을 확인한다.

사용: python check-links.py <lesson.html>
결과: 실패한 링크만 한 줄씩 `원인 | URL`. 실패가 없으면 `OK`.
"""
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def fetch(url):
    # 기본 User-Agent를 막는 사이트가 있다
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return type(e).__name__, ""


def main(lesson):
    sys.stdout.reconfigure(encoding="utf-8")
    page = open(lesson, encoding="utf-8").read()
    links = sorted({html.unescape(u) for u in re.findall(r'href="(https?://[^"]+)"', page)})
    pages = sorted({u.split("#")[0] for u in links})
    with ThreadPoolExecutor(8) as pool:
        got = dict(zip(pages, pool.map(fetch, pages)))
    bad = []
    for url in links:
        base, _, frag = url.partition("#")
        status, body = got[base]
        if status != 200:
            bad.append(f"HTTP {status} | {url}")
        elif frag:
            # docs.docker.com은 id를 따옴표 없이 쓰고(id=healthcheck), containers.dev는 <a name>을 쓴다
            f = re.escape(urllib.parse.unquote(frag))
            if not re.search(rf'(?:id|name)=(?:"{f}"|{f}[\s>])', body):
                bad.append(f"no id | {url}")
    print("\n".join(bad) or "OK")


if __name__ == "__main__":
    main(sys.argv[1])
