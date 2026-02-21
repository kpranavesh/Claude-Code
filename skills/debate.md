# Debate — Intellectual Sparring Partner

Use this skill when you want the sharpest opposing view before committing to an idea, plan, or decision.

## Trigger phrases
- "debate this"
- "argue against"
- "stress-test this idea"
- "what would a skeptic say"
- "push back on"
- "steelman the opposition"

---

## What this does

Runs your claim through three elite skeptic personas using **Groq + Llama 3.3 70B** — intentionally not Claude, so you get an uncorrelated perspective from a different model.

| Persona | Focus |
|---------|-------|
| **The Distinguished Engineer** | Technical feasibility, scaling, hidden complexity, "this is a solved problem" |
| **The Veteran Investor** | Moat, real TAM, unit economics, CAC/LTV, "why will YOU win" |
| **The Pragmatic Operator** | Execution risk, distraction, timeline realism, what kills you at month 3 |

Each persona gives 3–5 sharp points and ends with the single hardest question you need to answer before proceeding.

---

## How to run

```bash
# All 3 personas (default):
python debate/sparring_partner.py --claim "your idea or decision here"

# Single persona:
python debate/sparring_partner.py --claim "..." --persona engineer
python debate/sparring_partner.py --claim "..." --persona investor
python debate/sparring_partner.py --claim "..." --persona operator
```

---

## Setup (one-time)

Add to `.env`:
```
GROQ_API_KEY=your_key_here
```

Free key at: https://console.groq.com — generous free tier, no credit card needed.

Install the Groq LangChain package:
```bash
pip install langchain-groq
```

---

## When to use this

- Before starting a new project or business idea
- Before making a significant portfolio move
- Before pitching something internally — hear the pushback first
- Anytime you feel too confident about a decision

## When NOT to use this

- For factual research — this is a debate agent, not a research agent
- After you've already committed — use it before, not to second-guess done deals
