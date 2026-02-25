# Memory Changelog

_Append-only log. One entry per meaningful update to MEMORY.md or guidelines.md._
_Format: `## YYYY-MM-DD — [what changed]`_
_Monthly snapshots saved in `snapshots/YYYY-MM-DD.md`_

---

## 2026-02-21 — Initial setup

**What was built:**
- Created full workspace structure: `skills/`, `portfolio/`, `business-ideas/`
- MEMORY.md: identity, goals, tech stack, portfolio summary, file index (46 lines)
- guidelines.md: full response style guide, recommendation format, pushback protocol
- CLAUDE.md: project-level conventions, workspace map, constraints
- `portfolio/holdings.csv`: 31 positions, ~$246K
- `portfolio/analyzer.py`: live yfinance analysis + stock screener
- `business-ideas/profile.md`: full personal + business profile
- `business-ideas/reddit_scout.py`: 4-agent Reddit + Claude idea scout
- 5 skill files: build-agent, review-agent, api-debug, portfolio-analysis, business-scout

**Key facts captured:**
- Role: PM, Analytics team (data science, insights, product strategy)
- New dad (Eryk, 7mo). Travels for work. Time is the constraint.
- Goals: side income stream, Substack newsletter, grow portfolio
- Communication: direct opinion, no softening, pushback plainly
- Budget: $50–200/mo for side projects
- Platform priority: Substack first

**Portfolio context:**
- 5 conviction picks made: META + NVDA (add to existing), LLY + AVBO + MA (new buys)
- Gaps filled: healthcare (LLY), payments infra (MA), custom AI chips (AVGO)

**Snapshot saved:** `snapshots/2026-02-21.md`

---

## 2026-02-25 — WARNAlert idea researched and documented

**What was built:**
- Full competitor analysis: WARNwise, Parachute, WARNTracker, WARN Firehose, Revelio Labs, SeekOut, Layoffs.fyi, and 6 others
- Business plan: `business-ideas/business-plan/warn-alert-business-plan.md`
- 2 new skill files pushed to GitHub: `skills/prd-enhancement.md`, `skills/linkedin-post.md`

**Key facts captured:**
- WARNAlert scored 8.5/10 — highest-scored idea in Krishna's profile to date
- Business model: free employee alert (supply) + $125/mo recruiter alerts (demand) = two-sided marketplace
- No competitor has both sides. WARNwise ($99/mo) is closest but recruiter-only, 10-state cap.
- Data source decided: WARN Firehose API ($49/mo, all 50 states). Don't build a scraper.
- Legal: M1/M2 fully clean. M3 (LinkedIn individual matching via Proxycurl) needs FCRA review before shipping.
- Path to $5K MRR: 40 customers × $125. Infra break-even at 1 customer ($90/mo total).
- Validation gate: 20 cold LinkedIn messages to SMB recruiters. 5 "yes I'd pay" = green light to build.

**Files updated:** MEMORY.md, business-ideas/profile.md
**Pushed to GitHub:** business-ideas/business-plan/warn-alert-business-plan.md

---

_Next snapshot due: 2026-03-21_
_Update this file whenever: goals change · portfolio thesis shifts · new project launched · preferences updated_
