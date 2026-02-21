# Claude Code Workspace

A personal productivity and research workspace built around [Claude Code](https://claude.ai/code) — Anthropic's CLI agent for software engineering tasks.

This repo contains the configuration, tools, and agents I use day-to-day as a PM and solo builder. Everything here is designed to be run locally with Claude Code as the orchestrator.

---

## What's in here

### `CLAUDE.md`
The master instruction file auto-loaded by Claude Code on every session. Defines how the AI should respond, workflow conventions, tech stack, code standards, and project context. Think of it as a persistent system prompt scoped to this workspace.

### `skills/`
Reusable skill definitions that Claude Code can invoke on demand. Each file is a focused prompt + checklist for a specific type of task:

| Skill | Purpose |
|-------|---------|
| `build-agent.md` | Scaffold a new LangChain + Claude agent from scratch |
| `review-agent.md` | Audit and improve existing agent/chain code |
| `api-debug.md` | Diagnose Claude API and LangChain failures |
| `portfolio-analysis.md` | Analyze holdings and screen for new stock ideas |
| `business-scout.md` | Score and rank business ideas against a personal profile |

### `portfolio/`
Python tools for personal investment analysis using live market data via `yfinance`.

- **`analyzer.py`** — Portfolio summary, sector/horizon allocation, valuation snapshot, and stock screener against a curated universe. Runs in ~60s with live data.
- **`deep_dive.py`** — Quick metrics table for a focused set of tickers (price, fwd PE, revenue growth, ROE, analyst rating, upside to target).

```bash
python portfolio/analyzer.py              # Summary only
python portfolio/analyzer.py --screen    # + new stock ideas
python portfolio/analyzer.py --fast      # Skip live fetch
```

> `holdings.csv` is gitignored — you supply your own.

### `business-ideas/`
A 4-agent system that scrapes Reddit, extracts business ideas, scores them against your profile, and writes a ranked markdown report — all via LangChain + Claude.

- **`reddit_scout.py`** — Pulls top posts from 15 business/startup subreddits, runs them through Claude for idea extraction and profile-fit scoring, outputs a ranked report.

```bash
python business-ideas/reddit_scout.py                            # Standard run
python business-ideas/reddit_scout.py --timeframe month --save  # Deeper, save report
python business-ideas/reddit_scout.py --fast                    # Raw Reddit posts only
```

> `profile.md` is gitignored — the scorer agent expects a personal profile markdown file at `business-ideas/profile.md`.

### `tasks/`
Lightweight task tracking used by Claude Code during multi-step work.

- **`todo.md`** — Active plan written before any non-trivial task. Checked off as work progresses.
- **`lessons.md`** — Rules accumulated from corrections. Reviewed at the start of sessions to prevent repeat mistakes.

---

## Tech stack

- **Python 3.11+**
- **LangChain** + `langchain-anthropic` (LCEL chains, multi-agent orchestration)
- **Claude models:** `claude-sonnet-4-6` (default) · `claude-haiku-4-5-20251001` (fast subtasks) · `claude-opus-4-6` (heavy reasoning)
- **`yfinance`** for live market data
- **`python-dotenv`** for secrets — `ANTHROPIC_API_KEY` expected in `.env`

---

## Setup

```bash
pip install langchain langchain-anthropic yfinance pandas numpy python-dotenv requests
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

---

## What's gitignored

| Path | Reason |
|------|--------|
| `portfolio/holdings.csv` | Personal financial data |
| `business-ideas/profile.md` | Personal profile used by the scorer agent |
| `business-ideas/reports/` | Generated report output |
| `.claude/` | Local Claude Code settings |
| `memory/` | Symlinked personal context directory |
