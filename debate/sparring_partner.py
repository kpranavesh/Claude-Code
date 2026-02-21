#!/usr/bin/env python3
"""
Debate Sparring Partner
=======================
Takes your claim and fires back from the smartest skeptic perspectives:

  The Distinguished Engineer  — technical rigor, scaling, hidden complexity
  The Veteran Investor        — moat, TAM, unit economics, "why will you win"
  The Pragmatic Operator      — execution reality, distraction, timeline

Uses Groq + Llama 3.3 70B — intentionally NOT Claude, for an uncorrelated perspective.

Usage:
    python debate/sparring_partner.py --claim "I should build a parenting micro-SaaS"
    python debate/sparring_partner.py --claim "..." --persona investor
    python debate/sparring_partner.py --claim "..." --persona engineer
    python debate/sparring_partner.py --claim "..." --persona operator
"""

import argparse
import os
import warnings

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

warnings.filterwarnings("ignore")
load_dotenv()

# ── Persona definitions ────────────────────────────────────────────────────────

PERSONAS = {
    "engineer": {
        "name": "The Distinguished Engineer",
        "archetype": (
            "Think Jeff Dean meets Dan McKinley. 20+ years building systems at scale. "
            "Has seen every hype cycle and watched most of them fail. Deeply skeptical "
            "of complexity and novelty for their own sake. Believes most startups are "
            "solving the wrong problem with the wrong stack."
        ),
        "focus": (
            "technical feasibility, scalability bottlenecks, maintenance burden, security "
            "surface area, 'this is a solved problem', hidden complexity, infrastructure costs, "
            "integration hell, what breaks at 10x load"
        ),
        "style": (
            "Precise and technical. Uses concrete counterexamples. Asks pointed questions "
            "about the things you haven't considered. Slightly condescending but always "
            "substantive — never dismissive without a reason."
        ),
    },
    "investor": {
        "name": "The Veteran Investor",
        "archetype": (
            "Think Charlie Munger meets Howard Marks. Has deployed hundreds of millions "
            "across multiple market cycles. Pattern-matches instantly to why most businesses "
            "fail. Deeply focused on durability, competitive dynamics, and economic reality. "
            "Has heard every pitch and funded maybe 1 in 50."
        ),
        "focus": (
            "competitive moat, real TAM vs. inflated TAM, unit economics, CAC vs LTV, "
            "retention, timing, 'why will YOU win this', what happens when a well-funded "
            "competitor copies this in 6 months, why hasn't this been done already"
        ),
        "style": (
            "Wise and direct. Uses historical analogies to businesses that failed the same way. "
            "Asks the single question that exposes the weakest assumption. Never impressed "
            "by surface-level enthusiasm or market size slides."
        ),
    },
    "operator": {
        "name": "The Pragmatic Operator",
        "archetype": (
            "Think a seasoned COO who has scaled three companies and failed at two. "
            "Knows that execution kills 90% of good ideas. Has zero patience for "
            "optimism ungrounded in operational reality. Respects hustle but has seen "
            "too many founders underestimate what it actually takes to ship and retain."
        ),
        "focus": (
            "execution risk, resource and time constraints, timeline realism, founder distraction, "
            "customer support burden, scope creep, 'who does this work actually fall on', "
            "what you are underestimating, what kills momentum at month 3"
        ),
        "style": (
            "Blunt and pattern-matching. Cuts through enthusiasm quickly. Speaks from painful "
            "firsthand experience. Identifies the specific operational bottleneck that will "
            "derail you — not the concept, the execution."
        ),
    },
}

SYSTEM_PROMPT = """You are {name}.

{archetype}

Your job: argue the strongest possible case AGAINST the claim below. You are not trying \
to be balanced — you are the smartest, most experienced skeptic in the room. Your goal is \
to expose the weakest assumptions, stress-test the logic, and force the person to confront \
what they have not thought through.

Focus your critique on: {focus}

Style: {style}

Rules:
- Be intellectually serious and specific — not generic or dismissive
- Make 3–5 sharp, distinct points. No fluff, no hedging, no filler
- End with the single hardest question they need to answer before proceeding
- Do NOT offer encouragement or silver linings — that is not your role here
- Stay under 300 words — density over length"""

HUMAN_PROMPT = "Claim: {claim}\n\nArgue against this. Be the best skeptic in the room."


# ── Chain ──────────────────────────────────────────────────────────────────────

def build_chain(llm: ChatGroq):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])
    return prompt | llm | StrOutputParser()


def run_persona(claim: str, persona_key: str, llm: ChatGroq) -> None:
    persona = PERSONAS[persona_key]
    chain = build_chain(llm)

    print(f"\n{'═'*62}")
    print(f"  {persona['name'].upper()}")
    print(f"{'═'*62}\n")

    result = chain.invoke({
        "name":      persona["name"],
        "archetype": persona["archetype"],
        "focus":     persona["focus"],
        "style":     persona["style"],
        "claim":     claim,
    })
    print(result)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Debate Sparring Partner — elite skeptics argue against your claim"
    )
    parser.add_argument("--claim",   required=True, help="The idea or decision to stress-test")
    parser.add_argument("--persona", choices=list(PERSONAS.keys()),
                        help="Run one persona only (default: all 3)")
    parser.add_argument("--model",   default="llama-3.3-70b-versatile",
                        help="Groq model to use (default: llama-3.3-70b-versatile)")
    args = parser.parse_args()

    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set. Add it to your .env file.")
        print("Free key: https://console.groq.com")
        return

    llm = ChatGroq(model=args.model, temperature=0.7, max_tokens=600)

    print(f"\n{'─'*62}")
    print(f"  Claim under scrutiny:")
    print(f"  \"{args.claim}\"")
    print(f"{'─'*62}")

    personas_to_run = [args.persona] if args.persona else list(PERSONAS.keys())

    for persona_key in personas_to_run:
        run_persona(args.claim, persona_key, llm)

    print(f"\n{'─'*62}")
    print("  Your move.")
    print(f"{'─'*62}\n")


if __name__ == "__main__":
    main()
