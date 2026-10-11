import json
import os
import random
import re
import smtplib
import sys
import traceback
import urllib.request
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

import covers
import llm

POSTS = Path(__file__).resolve().parent.parent / "src" / "content" / "posts"
HEADS_CHANCE = 0.5          # chance of heads on a flip day
MAX_GAP_DAYS = 7            # safeguard: force heads after this many days without a post
MIN_WORDS = 20              # raise to ~350 once real writing is on
UPLOAD_MIN_OVERALL = 6      # below this the post is rejected
FLOOR_ACCURACY = 5          # below this the post is rejected
LINKEDIN_MIN_OVERALL = 8    # "very good" -> LinkedIn email
LINKEDIN_MIN_ACCURACY = 8


def days_since_last_post():
    dates = [json.loads(p.read_text())["publishedAt"] for p in POSTS.glob("*.json")]
    if not dates:
        return 999
    return (date.today() - date.fromisoformat(max(dates))).days


def flip(force, tails):
    if force:
        return "heads"
    if tails:
        return "tails"
    gap = days_since_last_post()
    if gap == 0:
        return "skip"
    if gap >= MAX_GAP_DAYS:
        return "heads"
    return "heads" if random.random() < HEADS_CHANCE else "tails"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def link_ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status < 400
    except Exception:
        return False


def rule_checks(draft, story):
    problems = []
    words = sum(len(p.split()) for p in draft["content"])
    if words < MIN_WORDS:
        problems.append(f"too short ({words} words)")
    if len(story["sources"]) < 2:
        problems.append("fewer than 2 sources")
    for s in story["sources"]:
        if not link_ok(s["url"]):
            problems.append(f"dead link: {s['url']}")
    if (POSTS / f"{date.today().isoformat()}-{slugify(draft['title'])}.json").exists():
        problems.append("duplicate post")
    return problems


def build_post(draft, story, scores, image, credit):
    slug = slugify(draft["title"])
    words = sum(len(p.split()) for p in draft["content"])
    today = date.today()
    return {
        "slug": slug,
        "title": draft["title"],
        "date": today.strftime("%d %b %Y"),
        "publishedAt": today.isoformat(),
        "tag": draft["tag"],
        "excerpt": draft["excerpt"],
        "readTime": f"{max(1, round(words / 200))} min",
        "image": image,
        "imageCredit": credit,
        "content": draft["content"],
        "sources": story["sources"],
        "score": scores,
        "linkedinUrl": "",
    }


def send_email(subject, body):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    if not sender or not password:
        print(f"\n[email not configured]\nSubject: {subject}\n\n{body}\n")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
    print("Email sent:", subject)


def notify(subject, body, dry):
    if dry:
        print(f"\n[email preview]\nSubject: {subject}\n\n{body}\n")
    else:
        send_email(subject, body)


def run(dry, force, tails):
    result = flip(force, tails)
    if result == "skip":
        print("Already posted today. Skipping.")
        return
    if result == "tails":
        notify("nikki logs: coin was tails",
               "The coin landed tails, so nothing was generated today.", dry)
        return

    story = llm.find_story()
    draft = llm.write_post(story)
    scores = llm.judge_post(draft, story)

    problems = rule_checks(draft, story)
    if scores["accuracy"] < FLOOR_ACCURACY:
        problems.append(f"accuracy too low ({scores['accuracy']})")
    if scores["overall"] < UPLOAD_MIN_OVERALL:
        problems.append(f"overall score too low ({scores['overall']})")
    if problems:
        notify(f"nikki logs: post rejected - {draft['title']}",
               "Rejected because:\n- " + "\n- ".join(problems) + f"\n\nScores: {scores}", dry)
        return

    image, credit = covers.get_cover(slugify(draft["title"]), dry=dry)
    post = build_post(draft, story, scores, image, credit)

    if dry:
        print(json.dumps(post, indent=2))
    else:
        path = POSTS / f"{post['publishedAt']}-{post['slug']}.json"
        path.write_text(json.dumps(post, indent=2) + "\n")
        print("Wrote", path.name)

    site = os.getenv("SITE_URL", "http://localhost:8443").rstrip("/")
    url = f"{site}/post/{post['slug']}"
    sources = "\n".join(f"- {s['title']}: {s['url']}" for s in post["sources"])
    notify(
        f"nikki logs: new post - {post['title']}",
        f"Title: {post['title']}\nLink: {url}\nScores: {scores}\n"
        f"Cover: {credit or image}\n\nSources:\n{sources}\n\n"
        "(The link works once the site has deployed.)",
        dry,
    )

    if scores["overall"] >= LINKEDIN_MIN_OVERALL and scores["accuracy"] >= LINKEDIN_MIN_ACCURACY:
        text = llm.write_linkedin(post, url)
        notify(f"nikki logs: LinkedIn text - {post['title']}",
               f"{text}\n\nBlog link: {url}", dry)
    else:
        print("Not very good: no LinkedIn email.")


def main():
    dry = "--dry" in sys.argv
    force = "--force" in sys.argv
    tails = "--tails" in sys.argv
    try:
        if "--crash" in sys.argv:
            raise RuntimeError("test crash")
        run(dry, force, tails)
    except Exception:
        err = traceback.format_exc()
        print(err)
        try:
            notify("nikki logs: agent crashed", err[-1500:], dry)
        except Exception as mail_err:
            print("Could not send crash email:", mail_err)
        sys.exit(1)


if __name__ == "__main__":
    main()
    