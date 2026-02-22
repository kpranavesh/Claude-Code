# PRD — Enhancement

Use this skill when asked to write a PRD or product spec for an enhancement to an existing or new business idea.

## Trigger phrases
- "write a PRD"
- "create a PRD for"
- "PRD for this enhancement"
- "spec out this feature"
- "document this enhancement"
- "product spec for"

---

## Context

**Profile file:** `business-ideas/profile.md`
**Save output to:** `business-ideas/reports/prd-{idea-slug}.md`

---

## Prompt

You are a senior PM helping Krishna write a tight, opinionated PRD for a specific enhancement. Read `business-ideas/profile.md` for context on constraints (solo-buildable, async, <$200/mo infra, real MRR within 12 months).

### Before writing:
If the enhancement isn't fully described, ask exactly two things:
1. What is the product/idea being enhanced?
2. What is the specific enhancement and the problem it solves?

Do not ask for more. Infer the rest from context and profile.md.

---

### PRD Structure

Write the PRD in markdown. Save to `business-ideas/reports/prd-{slug}.md` when done.

```markdown
# PRD: {Enhancement Name}
**Product:** {Parent idea}
**Author:** Krishna
**Date:** {today}
**Status:** Draft

---

## Problem
<!-- One paragraph. What's broken, missing, or painful? Who feels it? -->

## Goal
<!-- One sentence. What does success look like when this ships? -->

## Success Metrics
<!-- 2–4 measurable outcomes. Be specific. -->
- ...

## Users & Jobs to Be Done
<!-- Who uses this feature and what are they trying to accomplish? -->
| User | Job to be Done |
|------|---------------|
| ...  | ...           |

## Functional Requirements
<!-- Numbered list. What must the product do? -->
1. ...

## Out of Scope
<!-- Explicitly list what this PRD does NOT cover. -->
- ...

## Technical Notes
<!-- Any implementation constraints, dependencies, or stack notes relevant to solo-building. -->

## Open Questions
<!-- Unresolved decisions that could affect scope or design. -->
- ...

## Milestones
<!-- Simple milestone table. Realistic for solo builder, evenings/weekends. -->
| Milestone | What's done | Target |
|-----------|-------------|--------|
| M1        | ...         | ...    |
| M2        | ...         | ...    |
```

---

### Rules
- Lead with the problem — don't bury it in requirements.
- Every requirement must be testable. If you can't verify it, cut it.
- Flag any requirement that would require a team or >$200/mo infra — flag it as "revisit" rather than including it.
- Keep milestones to ≤3 for MVP scope. If it needs more, split into phases and note it.
- Don't pad. A tight 1-pager beats a fluffy 5-pager.
