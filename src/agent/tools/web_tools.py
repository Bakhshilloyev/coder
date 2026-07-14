"""Web tools: fetch a URL and a lightweight web search.

Uses only the standard library so it works everywhere. ``web_search`` queries
the DuckDuckGo HTML endpoint; if that is unreachable it degrades to a clear
error rather than crashing.
"""

import re
import urllib.parse
import urllib.request
from html import unescape

from . import Tool, ToolResult, register

_USER_AGENT = "Mozilla/5.0 (compatible; UnifiedAIAgent/0.1; +https://github.com)"


def _get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, "replace")


def web_fetch(url: str, limit: int = 8000, timeout: int = 30) -> ToolResult:
    try:
        text = _get(url, timeout=timeout)
    except Exception as exc:
        return ToolResult(False, "", error=f"Fetch failed: {exc}")
    # Strip tags crudely for readability on small screens.
    plain = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    plain = re.sub(r"<style.*?</style>", " ", plain, flags=re.S | re.I)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = unescape(re.sub(r"\s+", " ", plain)).strip()
    return ToolResult(True, plain[: int(limit)], meta={"url": url, "bytes": len(text)})


def web_search(query: str, limit: int = 5) -> ToolResult:
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        html = _get(url)
    except Exception as exc:
        return ToolResult(False, "", error=f"Search failed: {exc}")
    results = []
    for m in re.finditer(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        link = unescape(m.group(1))
        title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        results.append(f"{title}\n{link}")
        if len(results) >= int(limit):
            break
    if not results:
        return ToolResult(True, "(no results)", meta={"query": query})
    return ToolResult(True, "\n\n".join(results), meta={"query": query, "count": len(results)})


register(
    Tool(
        "web_fetch",
        "Fetch and extract text from a URL.",
        web_fetch,
        [{"name": "url", "type": "string"}, {"name": "limit", "type": "int"}],
        category="web",
    )
)
register(
    Tool(
        "web_search",
        "Search the web (DuckDuckGo HTML) and return result links.",
        web_search,
        [{"name": "query", "type": "string"}, {"name": "limit", "type": "int"}],
        category="web",
    )
)
