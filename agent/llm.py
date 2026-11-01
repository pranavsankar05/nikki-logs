import json
import os
import re
import urllib.request
from pathlib import Path

MOCK = os.getenv("MOCK_LLM", "1") == "1"
POSTS = Path(__file__).resolve().parent.parent / "src" / "content" / "posts"

FIND_MODEL = "claude-sonnet-5-5"
WRITE_MODEL = "claude-sonnet-5-5"
JUDGE_MODEL = "claude-haiku-5-5"

VOICE = ("Neutral third person, plain and curious. Explain things clearly for a "
         "college student who follows tech. No hype, no clickbait, no first person.")
MAJOR = ("new model or product releases from major labs, major research results, "
         "policy and regulation, large funding rounds or acquisitions")


def _call(model, system, user, max_tokens, tools=None, label=""):
    import anthropic
    kwargs = dict(model=model, max_tokens=max_tokens, system=system,
                  messages=[{"role": "user", "content": user}])
    if tools:
        kwargs["tools"] = tools
    msg = anthropic.Anthropic().messages.create(**kwargs)
    u = msg.usage
    print(f"[tokens] {label}: in={u.input_tokens} out={u.output_tokens}")
    return "".join(b.text for b in msg.content if b.type == "text")


def _json_from(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON in reply: " + text[:200])
    return json.loads(text[start:end + 1])


def _recent_titles(n=15):
    items = []
    for p in POSTS.glob("*.json"):
        try:
            d = json.loads(p.read_text())
            items.append((d["publishedAt"], d["title"]))
        except Exception:
            pass
    return [t for _, t in sorted(items, reverse=True)[:n]]


def _fetch_text(url, limit=6000):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read(600_000).decode("utf-8", "ignore")
    except Exception as e:
        return f"(could not fetch: {e})"
    html = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", html))
    return text[:limit]


def _source_pack(story):
    parts = []
    for i, s in enumerate(story["sources"], 1):
        parts.append(f"SOURCE {i}: {s['title']} ({s['url']})\n{_fetch_text(s['url'])}")
    return "\n\n".join(parts)


def find_story():
    if MOCK:
        return {
            "headline": "Example AI story",
            "sources": [
                {"title": "Example One", "url": "https://example.com"},
                {"title": "Example Two", "url": "https://example.org"},
            ],
        }
    from datetime import date
    system = ("You are the news researcher for a personal AI journal. Find ONE "
              "important AI news story from the last 7 days using web search.")
    user = (f"Today is {date.today().isoformat()}. Major means: {MAJOR}.\n"
            f"Do NOT pick a story already covered by these posts: {_recent_titles()}\n"
            "Prefer one primary source (company blog, paper, official statement) plus "
            "at least one reputable news outlet. Use only real URLs you saw in search "
            "results.\nReply with ONLY JSON: {\"headline\": str, \"summary\": str, "
            "\"sources\": [{\"title\": str, \"url\": str}]} with 2 to 4 sources.")
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 6}]
    story = _json_from(_call(FIND_MODEL, system, user, 2000, tools, "find_story"))
    story["sources"] = [s for s in story.get("sources", []) if s.get("url")]
    return story
def write_post(story):
    if MOCK:
        return {
            "title": "Example AI story",
            "tag": "AI",
            "excerpt": "A mock post to test the pipeline end to end.",
            "content": [
                "This is the first paragraph of a mock post written without any API call.",
                "This is the second paragraph, used only to test the pipeline.",
            ],
        }
    system = ("You write posts for a personal AI journal. Voice: " + VOICE + "\n"
              "Rules: 1,000 to 1,500 words. Use ONLY facts found in the source text "
              "provided; never invent numbers, quotes, dates or names. Paraphrase in "
              "your own words, no direct quotes. Name the sources in the text. Open "
              "with what happened, then why it matters, background, and what to watch "
              "next. Say so when something is uncertain. Plain paragraphs only: no "
              "markdown, no headings, no bullet points.")
    user = (f"Story: {story['headline']}\n{story.get('summary', '')}\n\n"
            f"{_source_pack(story)}\n\nReply with ONLY JSON: {{\"title\": str (under "
            "80 chars), \"tag\": str (1 to 2 words, e.g. Models, Research, Policy, "
            "Business), \"excerpt\": str (1 to 2 sentences, under 200 chars), "
            "\"content\": [str paragraphs]}")
    return _json_from(_call(WRITE_MODEL, system, user, 6000, label="write_post"))


def judge_post(draft, story):
    if MOCK:
        return {
            "overall": float(os.getenv("MOCK_OVERALL", "8.5")),
            "accuracy": float(os.getenv("MOCK_ACCURACY", "9")),
        }
    system = ("You are a strict fact-checking editor. Score the post against the "
              "source text only.")
    user = (f"POST TITLE: {draft['title']}\n\nPOST:\n" + "\n\n".join(draft["content"])
            + f"\n\n{_source_pack(story)}\n\nScore each from 0 to 10. accuracy: every "
            "claim, number, name and date must be supported by the sources; invented "
            "or unsupported facts must score below 5; 10 only if all is verifiable. "
            "newsworthiness: how important the story is. clarity: how well explained. "
            "originality: how fresh the angle and wording is, not copied from the "
            "sources.\nReply with ONLY JSON: {\"accuracy\": n, \"newsworthiness\": n, "
            "\"clarity\": n, \"originality\": n, \"issues\": [str]}")
    r = _json_from(_call(JUDGE_MODEL, system, user, 1200, label="judge_post"))
    print("judge issues:", r.get("issues"))
    overall = (0.40 * r["accuracy"] + 0.25 * r["clarity"]
               + 0.20 * r["newsworthiness"] + 0.15 * r["originality"])
    return {
        "overall": round(overall, 1),
        "accuracy": float(r["accuracy"]),
        "newsworthiness": float(r["newsworthiness"]),
        "clarity": float(r["clarity"]),
        "originality": float(r["originality"]),
    }


def write_linkedin(post, url):
    if MOCK:
        return f"Mock LinkedIn post about: {post['title']}\n\nRead more: {url}\n\n#AI"
    system = ("You write short LinkedIn posts for a college student's AI journal. "
              "Plain text, no markdown, no emojis, no claims that are not in the post.")
    user = (f"Title: {post['title']}\nExcerpt: {post['excerpt']}\n\n"
            + "\n\n".join(post["content"][:3])
            + f"\n\nWrite: one hook line, then 2 or 3 short lines, then 'Read more: "
            f"{url}', then exactly 3 hashtags.")
    return _call(JUDGE_MODEL, system, user, 500, label="write_linkedin").strip()