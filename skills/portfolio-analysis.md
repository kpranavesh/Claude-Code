# Portfolio Analysis & Stock Discovery

Use this skill when asked to:
- Analyze the current portfolio
- Find new stock ideas or screen for promising names
- Update holdings (add/remove/change value)
- Explain a position, thesis, or risk
- Run the analyzer script

## Trigger phrases
- "analyze my portfolio"
- "find new stock ideas"
- "what should I add"
- "update my holdings"
- "screen for new names"
- "run the analyzer"

---

## Context

**Portfolio file:** `portfolio/holdings.csv`
**Analyzer script:** `portfolio/analyzer.py`
**Report output:** `portfolio/report.md`

The holdings CSV has these columns:
`ticker, value_usd, horizon, sector, type, key_thesis, key_risk`

**Types:** `Equity`, `ETF`, `Crypto`
**Horizons:** `Short (<3)`, `Medium (3-10)`, `Long (Never)`

---

## Prompt

You are helping analyze and expand an investment portfolio. Follow these steps based on the request:

### If running analysis:
1. Tell the user to run the analyzer:
   ```bash
   # Full analysis (live data):
   python portfolio/analyzer.py

   # With stock screener:
   python portfolio/analyzer.py --screen

   # Full run + save report:
   python portfolio/analyzer.py --screen --report

   # Fast (no live fetch, use CSV values):
   python portfolio/analyzer.py --fast
   ```
2. Interpret the output — highlight sector concentration risk, horizon imbalance, or valuation outliers.

### If finding new stock ideas:
Use the investor's profile below to evaluate candidates:

**Investment style (from portfolio patterns):**
- Megacap quality with moats (GOOGL, MSFT, AMZN, NVDA, TSM)
- High-growth tech/AI with strong fundamentals (PLTR, CLS, AMD, DELL)
- ETF core + individual alpha generators
- Crypto as a separate allocation bucket (~20% of portfolio)
- China as speculative growth plays (BABA, BIDU)
- Some dividend/value (SCHD, BRK.B, PYPL)
- Willing to hold concentrated positions if conviction is high
- Short-horizon plays only when there's a clear catalyst

**Screening criteria for new ideas:**
- Revenue growth > 15% YoY preferred
- Forward P/E < 50 for growth, < 20 for value
- Strong gross margins (> 40% for software, > 25% for hardware)
- Analyst consensus: Buy or Strong Buy
- Clear moat: brand, network effect, switching cost, first-mover, data
- Strong leadership: tenure, skin in the game, track record
- Shareholder-friendly: buybacks preferred over heavy stock comp dilution

**Sectors currently underweighted (potential gaps):**
- Healthcare / Biotech (LLY, NVO, ISRG)
- Cybersecurity (CRWD, PANW, ZS)
- Payments / Fintech infrastructure (V, MA)
- Infrastructure / Robotics

### If updating holdings:
Edit `portfolio/holdings.csv` directly. Keep the same column format.
Add new row, update `value_usd` for existing, or remove a row if position closed.

After any CSV update, remind the user to re-run the analyzer to get refreshed metrics.

### If explaining a position:
Read the row from holdings.csv, then enrich with:
- Current price / 52w range via yfinance
- Recent analyst ratings
- Key upcoming catalysts (earnings, product launches, macro events)
- How it fits in the overall portfolio context

---

## Key portfolio facts to keep in mind:
- Total ~$287K across 31 positions
- ~70% long-term / never-sell core
- ~20% crypto allocation (BTC, ETH, BITB, SOL)
- Heavy IT/tech concentration (~30%)
- Conviction picks: QQQM, VOO as index foundation + individual alpha on top
- Pabrai-style thinking: concentrated, high-conviction, long holding periods
