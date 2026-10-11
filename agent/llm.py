import os

MOCK = os.getenv("MOCK_LLM", "1") == "1"


def find_story():
    if MOCK:
        return {
            "headline": "Example AI story",
            "sources": [
                {"title": "Example One", "url": "https://example.com"},
                {"title": "Example Two", "url": "https://example.org"},
            ],
        }
    raise NotImplementedError("real news search comes later")


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
    raise NotImplementedError("real writing comes later")


def judge_post(draft, story):
    if MOCK:
        return {
            "overall": float(os.getenv("MOCK_OVERALL", "8.5")),
            "accuracy": float(os.getenv("MOCK_ACCURACY", "9")),
        }
    raise NotImplementedError("real judging comes later")


def write_linkedin(post, url):
    if MOCK:
        return f"Mock LinkedIn post about: {post['title']}\n\nRead more: {url}\n\n#AI"
    raise NotImplementedError("real LinkedIn text comes later")