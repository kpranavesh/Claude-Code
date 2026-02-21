#!/usr/bin/env python3
"""
Business Idea Scout — Multi-Agent System
=========================================
Four agents running in sequence via LangChain + Claude:

  Agent 1 · Reddit Scraper   — fetches top posts from business/startup subreddits
  Agent 2 · Idea Extractor   — extracts concrete, actionable business ideas from raw posts
  Agent 3 · Profile Scorer   — scores each idea against your personal profile
  Agent 4 · Report Writer    — synthesizes into a clean ranked report

Usage:
    python business-ideas/reddit_scout.py
    python business-ideas/reddit_scout.py --subs entrepreneur SideProject passive_income
    python business-ideas/reddit_scout.py --timeframe month --limit 50 --save
    python business-ideas/reddit_scout.py --fast   # skip LLM, just dump raw Reddit posts
"""

import argparse
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

warnings.filterwarnings("ignore")
load_dotenv()

HERE = Path(__file__).parent
PROFILE_FILE = HERE / "profile.md"
REPORTS_DIR = HERE / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

REDDIT_HEADERS = {"User-Agent": "Mozilla/5.0 (BusinessScout/1.0; personal-research)"}

# ── Subreddit universe ────────────────────────────────────────────────────────
DEFAULT_SUBS = [
    "entrepreneur",
    "SideProject",
    "passive_income",
    "SaaS",
    "startups",
    "digitalnomad",
    "freelance",
    "ArtificialIntelligence",
    "ChatGPT",
    "learnprogramming",
    "datascience",
    "marketing",
    "Entrepreneur",
    "microsaas",
    "indiehackers",
]

# ── Agent 1: Reddit Scraper ───────────────────────────────────────────────────

def fetch_subreddit(subreddit: str, limit: int, timeframe: str) -> list[dict]:
    """Pull top posts from a subreddit via public Reddit JSON API (no auth needed)."""
    url = f"https://www.reddit.com/r/{subreddit}/top.json"
    try:
        r = requests.get(
            url,
            headers=REDDIT_HEADERS,
            params={"t": timeframe, "limit": limit},
            timeout=12,
        )
        r.raise_for_status()
        posts = r.json()["data"]["children"]
        results = []
        for p in posts:
            d = p["data"]
            if d.get("stickied"):
                continue
            results.append({
                "title":        d["title"],
                "score":        d["score"],
                "comments":     d["num_comments"],
                "subreddit":    subreddit,
                "url":          f"https://reddit.com{d.get('permalink', '')}",
                "body":         (d.get("selftext") or "")[:600].strip(),
            })
        return results
    except Exception as e:
        print(f"  ⚠  r/{subreddit}: {e}")
        return []


def scrape_reddit(subreddits: list[str], limit: int, timeframe: str) -> list[dict]:
    """Agent 1: Collect posts across all target subreddits."""
    all_posts = []
    for sub in subreddits:
        posts = fetch_subreddit(sub, limit, timeframe)
        all_posts.extend(posts)
        print(f"  r/{sub:<24} → {len(posts)} posts")
    # Sort by engagement (score + comments)
    all_posts.sort(key=lambda p: p["score"] + p["comments"] * 2, reverse=True)
    return all_posts[:200]  # cap to avoid token blowout


# ── Agent 2: Idea Extractor ───────────────────────────────────────────────────

EXTRACTOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a sharp business analyst who extracts concrete, actionable business ideas
from Reddit posts. Focus only on ideas that could realistically generate income — not vague
discussions or questions.

For each distinct idea you identify, output a JSON object with:
  - "idea": short name (5 words max)
  - "description": 1–2 sentences on what it is and how it makes money
  - "category": one of [SaaS, Content, Service, App, API, Marketplace, Newsletter, Course, Other]
  - "signals": why Reddit thinks this is promising (upvotes, comments, demand signals)
  - "source_sub": which subreddit it came from

Output a JSON array of ideas. Extract 15–25 ideas. Skip redundant ones. Be specific, not generic.
"""),
    ("human", """Here are the top Reddit posts from business/startup communities this week:

{posts_text}

Extract the most promising, concrete business ideas from these posts."""),
])


def extract_ideas(posts: list[dict], llm: ChatAnthropic) -> list[dict]:
    """Agent 2: Use Claude to extract business ideas from raw Reddit posts."""
    # Format posts for the prompt
    posts_text = ""
    for i, p in enumerate(posts[:80], 1):  # top 80 to stay within context
        posts_text += f"\n[{i}] r/{p['subreddit']} | ↑{p['score']} | 💬{p['comments']}\n"
        posts_text += f"Title: {p['title']}\n"
        if p["body"]:
            posts_text += f"Body: {p['body']}\n"

    chain = EXTRACTOR_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({"posts_text": posts_text})

    # Parse JSON from response (handle markdown code blocks)
    try:
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        ideas = json.loads(raw.strip())
        return ideas if isinstance(ideas, list) else []
    except json.JSONDecodeError:
        print("  ⚠  Extractor: could not parse JSON — returning raw text")
        return [{"idea": "Parse error", "description": raw[:200], "category": "Other",
                 "signals": "", "source_sub": ""}]


# ── Agent 3: Profile Scorer ───────────────────────────────────────────────────

SCORER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a business advisor helping evaluate startup ideas for a specific person.
Score each idea strictly and honestly. Do not be optimistic for its own sake — an idea that
doesn't fit the person should score low.

Score each idea on these dimensions (1–10 each):
  - remote_score:     can this be done 100% remotely?
  - income_score:     realistic MRR potential within 12 months ($1K+ = 6, $5K+ = 8, $10K+ = 10)
  - buildability:     can they build it solo using Python + Claude Code + LangChain?
  - skill_fit:        how well does it match their skills (data, AI, finance, app dev)?
  - time_efficiency:  low hours-per-dollar ratio? (scales without more hours = higher score)

Compute: overall_score = (remote * 0.30) + (income * 0.25) + (buildability * 0.20) + (skill_fit * 0.15) + (time_efficiency * 0.10)

Also add:
  - "first_step": the single most important first action they should take (1 sentence)
  - "time_to_revenue": realistic estimate (e.g., "2–4 weeks", "3–6 months")
  - "why_fit": 1 sentence on why this matches their profile
  - "why_risk": 1 sentence on the biggest risk or challenge

Output a JSON array — same ideas as input but with all score fields added.
Keep all original fields. Sort by overall_score descending.
"""),
    ("human", """Here is the person's profile:

{profile}

---

Here are the business ideas to score:

{ideas_json}

Score all ideas and return the full enriched JSON array, sorted by overall_score descending."""),
])


def score_ideas(ideas: list[dict], profile: str, llm: ChatAnthropic) -> list[dict]:
    """Agent 3: Score each idea against the user's profile using Claude."""
    chain = SCORER_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({
        "profile": profile,
        "ideas_json": json.dumps(ideas, indent=2),
    })

    try:
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        scored = json.loads(raw.strip())
        return scored if isinstance(scored, list) else ideas
    except json.JSONDecodeError:
        print("  ⚠  Scorer: could not parse JSON — returning unscored ideas")
        return ideas


# ── Agent 4: Report Writer ────────────────────────────────────────────────────

REPORT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are writing a concise, actionable business opportunity report.
Be direct. No fluff. Write for someone who is busy, smart, and wants to act fast.

Structure:
1. TL;DR (3 bullets — top 3 ideas they should seriously consider)
2. Top 10 Ranked Opportunities (table + brief commentary per idea)
3. Hidden Gems (2–3 lower-ranked ideas that might be underrated for this person)
4. Emerging Themes from Reddit this week (patterns, what's buzzing)
5. Recommended Next Steps (specific, ordered by priority)

Tone: sharp, confident, like a smart friend who has done the research for you.
Use markdown. This will be saved as a .md report file.
"""),
    ("human", """Person profile summary:
{profile_summary}

Scored business ideas (sorted by fit):
{scored_json}

Write the full opportunity report."""),
])


def write_report(scored_ideas: list[dict], profile: str, llm: ChatAnthropic) -> str:
    """Agent 4: Synthesize everything into a clean markdown report."""
    # Summarize profile briefly for context
    profile_summary = "\n".join(profile.split("\n")[:30])

    chain = REPORT_PROMPT | llm | StrOutputParser()
    report = chain.invoke({
        "profile_summary": profile_summary,
        "scored_json": json.dumps(scored_ideas[:20], indent=2),  # top 20 scored
    })
    return report


# ── Display helpers ───────────────────────────────────────────────────────────

def print_section(title: str):
    print(f"\n{'═'*62}")
    print(f"  {title}")
    print(f"{'═'*62}")


def print_top_ideas(ideas: list[dict], n: int = 10):
    print(f"\n  {'#':<3} {'Score':>6}  {'Idea':<28}  {'Category':<12}  {'Income':>7}  {'Build':>6}")
    print(f"  {'─'*72}")
    for i, idea in enumerate(ideas[:n], 1):
        score = idea.get("overall_score", 0)
        if isinstance(score, str):
            try:
                score = float(score)
            except Exception:
                score = 0
        name     = str(idea.get("idea", ""))[:26]
        cat      = str(idea.get("category", ""))[:11]
        income   = idea.get("income_score", "?")
        build    = idea.get("buildability", "?")
        print(f"  {i:<3} {score:>6.2f}  {name:<28}  {cat:<12}  {income:>7}  {build:>6}")
        if idea.get("why_fit"):
            print(f"       → {idea['why_fit']}")
        if idea.get("first_step"):
            print(f"       ✦ {idea['first_step']}")
        print()


# ── Main orchestrator ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Business Idea Scout — multi-agent Reddit + Claude")
    parser.add_argument("--subs",      nargs="+", default=DEFAULT_SUBS,
                        help="Subreddits to scrape (default: 15 business subs)")
    parser.add_argument("--timeframe", default="week",
                        choices=["day", "week", "month", "year"],
                        help="Reddit timeframe for top posts (default: week)")
    parser.add_argument("--limit",     type=int, default=25,
                        help="Posts per subreddit (default: 25)")
    parser.add_argument("--save",      action="store_true",
                        help="Save markdown report to reports/ directory")
    parser.add_argument("--fast",      action="store_true",
                        help="Skip LLM agents — just print raw Reddit posts")
    parser.add_argument("--model",     default="claude-sonnet-4-6",
                        help="Claude model to use (default: claude-sonnet-4-6)")
    args = parser.parse_args()

    # Load profile
    if not PROFILE_FILE.exists():
        print(f"ERROR: profile not found at {PROFILE_FILE}")
        sys.exit(1)
    profile = PROFILE_FILE.read_text()

    # ── Agent 1: Scrape Reddit ──────────────────────────────────────────────
    print_section(f"AGENT 1 · REDDIT SCRAPER  (timeframe={args.timeframe})")
    posts = scrape_reddit(args.subs, args.limit, args.timeframe)
    print(f"\n  Total posts collected: {len(posts)}")

    if args.fast:
        for p in posts[:20]:
            print(f"\n  [{p['subreddit']}] ↑{p['score']} — {p['title']}")
        return

    # ── Init LLM ───────────────────────────────────────────────────────────
    llm = ChatAnthropic(model=args.model, temperature=0.2, max_tokens=4096)

    # ── Agent 2: Extract Ideas ─────────────────────────────────────────────
    print_section("AGENT 2 · IDEA EXTRACTOR")
    print("  Extracting business ideas from posts via Claude...", end="", flush=True)
    ideas = extract_ideas(posts, llm)
    print(f" found {len(ideas)} ideas.")

    if not ideas:
        print("  No ideas extracted. Try --fast or check API key.")
        return

    # ── Agent 3: Score Against Profile ────────────────────────────────────
    print_section("AGENT 3 · PROFILE SCORER")
    print("  Scoring ideas against your profile...", end="", flush=True)
    scored_ideas = score_ideas(ideas, profile, llm)
    print(f" done.")

    # Sort by score
    def get_score(x):
        s = x.get("overall_score", 0)
        try:
            return float(s)
        except Exception:
            return 0
    scored_ideas.sort(key=get_score, reverse=True)

    print_top_ideas(scored_ideas)

    # ── Agent 4: Write Report ─────────────────────────────────────────────
    print_section("AGENT 4 · REPORT WRITER")
    print("  Synthesizing final report...", end="", flush=True)
    report_md = write_report(scored_ideas, profile, llm)
    print(" done.")

    # Print report to terminal
    print(f"\n{'─'*62}\n")
    print(report_md)

    # Save report
    if args.save:
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
        report_path = REPORTS_DIR / f"report_{date_str}.md"
        report_path.write_text(report_md)
        print(f"\n  Report saved → {report_path}")

    print()


if __name__ == "__main__":
    main()
