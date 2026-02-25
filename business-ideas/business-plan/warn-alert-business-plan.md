# WARNAlert — Business Plan
**Author:** Krishna
**Date:** 2026-02-24
**Status:** Draft — pre-validation
**Score:** 8.5/10 (vs. Krishna's profile constraints)

---

## The One-Liner

WARNAlert turns public WARN Act filings into real-time recruiting intelligence — alerting recruiters to incoming talent pools 60 days before a layoff happens, and alerting employees before their manager does.

---

## Problem

WARN Act filings are legally mandated, publicly available, and ignored by almost everyone. When a company lays off 100+ people, they must file a public notice 60 days in advance — naming the company, location, affected roles, and headcount.

That 60-day window is gold for recruiters. The talent is pre-identified, the layoff is confirmed, and no one else is calling yet.

The problem: WARN filings are scattered across 50 different state agency websites in inconsistent formats — PDFs, Excel sheets, HTML tables. Nobody has made this actionable for the people who need it most.

**Recruiters** spend thousands per month on sourcing tools that find active job seekers. WARN data surfaces passive candidates before they even know they're job seekers.

**Employees** have no reliable way to know if their employer filed a WARN notice. They find out from a manager, a rumor, or Twitter. The notice was public the whole time.

---

## Solution

A two-sided product built on automated WARN data aggregation:

**For recruiters (paid):** Real-time alerts when companies in their target geography, industry, or watchlist file a WARN notice. Filterable, actionable, integrated into their workflow.

**For employees (free):** Single-input alert — enter your employer name and email. Get notified within 24 hours if a matching WARN notice is filed. One CTA: "Recruiters are actively hiring for your role. Want to be discoverable?"

The employee product is the supply engine. Recruiters are the revenue engine. The flywheel: WARN filing → employee gets alert → employee opts into talent pool → recruiter pays to access pool.

---

## Market

**Primary buyer: SMB recruiting agencies and in-house talent teams.**

The US has ~25,000 recruiting/staffing agencies, the majority with <10 employees. These firms spend $75–300/mo on sourcing tools without hesitation — LinkedIn Recruiter alone runs $170+/mo per seat. They have budget, low procurement friction, and a clear ROI calculus: one successful placement from a WARNAlert lead pays for 12 months of subscription.

**TAM:** ~$2.5B (US recruiting tech market, SMB segment)
**SAM:** SMB agencies + in-house teams actively sourcing in sectors with high WARN activity (tech, manufacturing, retail, healthcare)
**SOM (Year 1):** 200 paying subscribers × $125/mo = **$300K ARR**. Conservative. Validate with 10 before modeling further.

---

## Product Roadmap

### M1 — Recruiter Alerts (2 weekends)
- WARN Firehose API integration (all 50 states, normalized, daily updates)
- User auth + onboarding (state / industry / company watchlist setup)
- Daily email digest + instant alert on new matching filing
- Basic web dashboard (recent filings, filter controls)
- Stripe billing ($75–150/mo)

**Validation gate:** 10 paying customers before M2 starts.

### M2 — Employee Alerts + Opt-in Pool (2 weekends)
- Free employee signup: employer name + email → WARN match → alert
- Opt-in CTA: "Let recruiters find you" toggle
- Recruiter-facing talent pool view: opted-in employees from WARN-matched companies
- Recruiter can see: role, location, WARN filing date. Nothing else without employee consent.

**Validation gate:** 50 opted-in employees, 3 recruiters actively using pool view.

### M3 — Individual Matching (2 weekends + legal review)
- Proxycurl API integration: cross-reference WARN filings against LinkedIn profiles by company + location + role type
- Confidence scoring: "87% match — Software Engineer at Salesforce Austin"
- Recruiter unlock: pay per profile enrichment or bundle into Pro tier
- FCRA compliance review required before shipping this layer

**Legal note:** M3 must be reviewed by an employment attorney before launch. FCRA exposure is real if recruiters use this for hiring decisions. M1 and M2 carry no material legal risk.

---

## Competitive Position

| | WARNAlert | WARNwise (closest) | Parachute | WARNTracker |
|--|-----------|-------------------|-----------|-------------|
| WARN-based | ✓ | ✓ | ✗ | ✓ |
| Recruiter alerts | ✓ | ✓ | ✓ | ✗ |
| Employee alerts | ✓ | ✗ | ✓ | ✗ |
| All 50 states | ✓ | ✗ (10 max) | N/A | ✓ |
| LinkedIn matching | ✓ (M3) | ✗ | ✗ | ✗ |
| Price | $75–150/mo | $59–99/mo | Free–? | $250/mo |

**Moat:** No competitor combines WARN automation + employee acquisition funnel + individual matching at SMB price point. WARNwise is closest but caps at 10 states and has no employee layer. Parachute has the model but relies on crowdsourcing — they get profiles 60 days after the layoff. We get them 60 days before.

---

## Business Model

### Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | Employee alert only — employer WARN monitoring, email notification |
| Starter | $75/mo | 3 states, 10 company watchlist, daily digest, web dashboard |
| Pro | $125/mo | Unlimited states, unlimited watchlist, instant alerts, talent pool access |
| Enterprise | $299/mo | Team seats, ATS webhook, CSV export, priority support |

### Unit Economics (Pro tier)
- Revenue per customer: $125/mo
- WARN Firehose API cost: $49/mo (flat, not per-user)
- Proxycurl (M3): ~$0.10/profile lookup — passed through or bundled
- SendGrid email: ~$0.001/email
- Infrastructure (Render/Railway): ~$20/mo
- **Gross margin: ~95%** at 20+ customers

### Path to $5K MRR
- 40 Pro subscribers × $125 = $5,000/mo
- 40 customers from a pool of 25,000 SMB agencies = 0.16% penetration
- Acquisition: cold outreach to recruiters on LinkedIn + niche communities (RecDev, Reddit r/recruiting)

### Path to $10K MRR
- 50 Pro + 10 Enterprise = $6,250 + $2,990 = **$9,240/mo**
- Or: introduce per-profile unlock pricing in M3 ($5–10/profile enrichment)

---

## Go-to-Market

### Phase 0 — Validate before building (Weeks 1–2)
- Cold message 20 SMB recruiters on LinkedIn with the concept, no product yet
- Ask: "Would you pay $99/mo to get a WARN alert when a target company announces layoffs, 60 days before the news breaks?"
- Target: 5 "yes, I'd pay" responses = green light for M1
- Communities: r/recruiting, RecDev Slack, Recruiters on LinkedIn

### Phase 1 — M1 Launch (Weeks 3–6)
- Launch on Product Hunt (recruiter audience is active there)
- Post in recruiting communities: RecDev, r/recruiting, LinkedIn posts
- Cold outreach to 100 SMB agencies in high-WARN sectors (tech, healthcare, retail)
- Target: 10 paying customers

### Phase 2 — Employee Flywheel (Weeks 7–10)
- Launch free employee tier
- Outreach to HR/career communities (r/layoffs, r/cscareerquestions, LinkedIn)
- Partner with outplacement firms — they pay or co-market to affected employees
- Target: 500 free employee signups, 50 opted into talent pool

### Phase 3 — Content + SEO (Ongoing)
- Weekly WARN digest newsletter (free, public) — builds organic traffic and brand
- "Which companies filed WARN notices this week?" — high search intent, zero competition
- LinkedIn content: Krishna's existing audience + PM/data credibility

---

## Tech Stack

- **Data source:** WARN Firehose API ($49/mo Pro tier)
- **Backend:** Python + FastAPI
- **Database:** PostgreSQL (Supabase free tier to start)
- **Email:** SendGrid
- **Auth:** Supabase Auth
- **Frontend:** Simple — Next.js or even a Streamlit MVP to validate
- **Billing:** Stripe
- **Individual matching:** Proxycurl API ($0.10/profile)
- **Hosting:** Railway or Render (~$20/mo)
- **Build time:** Claude Code — solo, evenings/weekends

Total infra cost at launch: **~$90/mo** (WARN Firehose $49 + Supabase $0 + Railway $20 + SendGrid $20 + misc)
Break-even: **1 paying customer**

---

## Financials

### Year 1 Conservative

| Month | Paying Customers | MRR | Cumulative Cost |
|-------|-----------------|-----|-----------------|
| 1–2 | 0 (build) | $0 | $180 |
| 3 | 5 | $625 | $270 |
| 4 | 12 | $1,500 | $360 |
| 6 | 25 | $3,125 | $540 |
| 9 | 40 | $5,000 | $810 |
| 12 | 60 | $7,500 | $1,080 |

**Year 1 ARR target: $90K**
**Year 1 infra spend: ~$1,080**
**Net margin at $7,500 MRR: ~94%**

---

## Legal Considerations

| Layer | Risk | Mitigation |
|-------|------|------------|
| WARN data aggregation | None — public record | None needed |
| Recruiter alerts by company/geography | None | None needed |
| Employee alerts | Minimal — notifying about public records | Clear disclosure in terms |
| M3 individual matching (LinkedIn cross-ref) | FCRA exposure if used for hiring decisions | Employment attorney review before M3 launch. Frame as "discovery signal," not "consumer report." |
| LinkedIn data via Proxycurl | ToS gray zone | Proxycurl operates under hiQ v. LinkedIn precedent. Monitor, have fallback. |

**Rule:** M1 and M2 ship without legal review. M3 requires a 30-minute employment attorney consult (~$300) before launch.

---

## Risks

**1. WARNwise improves their product.** They have a head start on recruiter alerts. Mitigation: employee layer and individual matching are genuine differentiators they haven't touched. Move fast.

**2. WARN Firehose goes down or changes pricing.** Single point of failure on data. Mitigation: warn-scraper (open source, Big Local News) is a fallback. Build the abstraction layer cleanly so the data source is swappable.

**3. Recruiter TAM is smaller than expected.** WARNwise exists and isn't dominating — possible signal. Mitigation: validate with 5 paying customers before M2. Employee layer expands TAM regardless.

**4. LinkedIn shuts down Proxycurl.** Kills M3. Mitigation: M1 and M2 are standalone businesses. M3 is additive, not core.

**5. FCRA classification.** Unlikely for M1/M2, real for M3. Mitigation: legal review before M3. Design M3 as a "discovery tool," not a hiring report.

---

## 90-Day Plan

| Week | Action | Success Criteria |
|------|--------|------------------|
| 1 | Message 20 recruiters with concept | 5+ "yes I'd pay" responses |
| 2 | If validated: set up WARN Firehose, auth, SendGrid | Working alert pipeline |
| 3–4 | Build M1: recruiter dashboard, filters, Stripe | Deployed, demo-ready |
| 5 | Soft launch to validation cohort | First paying customer |
| 6–7 | Product Hunt launch + recruiting community posts | 10 paying customers |
| 8–9 | Build M2: employee alerts + opt-in pool | 50 employee signups |
| 10 | Launch free employee tier publicly | 200 employee signups |
| 11–12 | Optimize onboarding, reduce churn, prep M3 spec | 25 paying customers, <5% monthly churn |

---

## What Success Looks Like at 12 Months

- 60 paying recruiters at $125/mo avg = **$7,500 MRR**
- 2,000+ employees on free alert tier (supply moat)
- M3 (individual matching) live with legal clearance
- Weekly WARN digest newsletter at 5,000 subscribers (SEO + brand)
- One partnership with an outplacement firm or HR platform

That's a $90K ARR business built solo, in evenings and weekends, on ~$1,080 of infra.

---

*Next step: 20 cold messages to SMB recruiters this week. Build nothing until 5 say yes.*
