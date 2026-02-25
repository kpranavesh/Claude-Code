# Memory — Krishna · Claude Code Workspace

## Identity
- Name: Krishna | South Indian | Travels for work
- Day job: Product Manager, Analytics team (data science, insights, product strategy)
- Time is the primary constraint — limited evenings/weekends, needs high-leverage work
- Wife works in ML. Dog: Beans, 2-year-old Border Collie.

## How to Talk to Krishna
- **Direct opinion always.** "I'd do X" not "you could consider X."
- **Pushback:** say it plainly — "That's a bad idea because X." No softening, say it once, then help execute.
- Balanced responses: brief framing → implementation. No walls of text, no bullet-point-everything.
- No emojis. Cite file:line for code. Trust that he follows technical reasoning fast.
- Full style guide → `memory/guidelines.md`

## Goals (next 12 months)
1. Launch a side income stream — real MRR, not a hobby
2. Build a personal brand — starting with Substack newsletter
3. Grow the investment portfolio intelligently

## Tech Stack
- Python · LangChain · Anthropic SDK (langchain-anthropic) · pandas · yfinance
- Ships fast with Claude Code + Gemini (design/project mgmt)
- Budget: $50–200/mo for side projects. Prove concept before paying.

## Portfolio
- ~$246K · 31 positions · Pabrai-style concentrated conviction
- Holdings: `portfolio/holdings.csv` | Analyzer: `portfolio/analyzer.py`
- Top 5 picks (Feb 2026): META, NVDA (add), LLY, AVGO, MA (new buys)

## Business / Side Hustle Context
- Full profile: `business-ideas/profile.md`
- #1 priority: Substack newsletter (AI + investing + PM lens) — **started Feb 2026**
- #2: micro-SaaS or tool buildable solo with Claude Code
- Constraint: remote-first, async, no hiring, <12mo to first dollar
- Scout tool: `business-ideas/reddit_scout.py`
- NOTE: Baby food tracker was a copied idea for inspiration — NOT something Krishna built

## WARNAlert — Top Idea (Score: 8.5/10)
- **What:** WARN Act filing monitor → recruiter alerts (paid) + employee alerts (free)
- **Insight:** 60-day advance notice window is the moat. WARN data is public, scattered, ignored.
- **Model:** Employee alert (free) = supply engine. Recruiter alerts ($125/mo) = revenue engine.
- **Flywheel:** WARN filing → employee gets alert → opts into talent pool → recruiter pays to access
- **Closest competitor:** WARNwise ($99/mo, recruiter-only, capped at 10 states). No one has both sides.
- **Data source:** WARN Firehose API ($49/mo, all 50 states, normalized) — don't build a scraper
- **Legal:** M1/M2 clean. M3 (LinkedIn individual matching via Proxycurl) needs FCRA review first.
- **Path to $5K MRR:** 40 customers × $125/mo. Break-even at 1 customer (~$90/mo infra).
- **Status:** Pre-validation. Next action: 20 cold LinkedIn messages to SMB recruiters. Build nothing until 5 say yes.
- **Business plan:** `business-ideas/business-plan/warn-alert-business-plan.md`

## Key Files
| File | Purpose |
|------|----------|
| `CLAUDE.md` | Project conventions + workspace overview |
| `memory/guidelines.md` | Detailed response preferences |
| `memory/changelog.md` | Append-only log of all meaningful updates |
| `memory/snapshots/` | Monthly full snapshots of MEMORY.md |
| `business-ideas/profile.md` | Full personal + business profile |
| `portfolio/holdings.csv` | All investment positions |
| `portfolio/analyzer.py` | Live analysis + stock screener |
| `skills/*.md` | Skill templates (build-agent, review-agent, api-debug, portfolio, business-scout) |

## MCP Setup (as of Feb 2026)
- GitHub MCP: **installed and connected** via `~/.claude.json` (stdio, not HTTP plugin)
- Command: `/opt/homebrew/bin/npx -y @modelcontextprotocol/server-github`
- Also configured: Daloopa MCP, Notion MCP (both need auth)
- Config file: `~/.claude.json` — NOT `~/.claude/settings.json` (that file doesn't exist)
- `~/.claude/plugins/` is the marketplace cache, NOT where active MCP configs live
- If `/mcp` doesn't show a server mid-session: restart Claude Code — MCPs load at startup only
- Verify anytime with: `claude mcp list`

## Token Strategy
- Research/scouting subagents → always use `model: "haiku"` in Task calls (~5x cheaper, no quality loss for web research)
- Quick 1-2 lookups → WebSearch directly in main context, skip the subagent
- Code, planning, architecture → Sonnet (default)
- Heavy reasoning only → Opus

## Memory Hygiene
- Hard limit: 200 lines (truncated after). Currently: ~83 lines. Budget: ~117 lines remaining.
- Update MEMORY.md when: goals change, major project ships, preferences shift
- Log every change in `memory/changelog.md` with date + what/why
- Snapshot monthly into `memory/snapshots/YYYY-MM-DD.md`
