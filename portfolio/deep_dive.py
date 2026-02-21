import yfinance as yf, warnings
warnings.filterwarnings("ignore")

picks = {
    "META": "current", "NVDA": "current", "AMD": "current", "CLS": "current",
    "LLY": "new", "AVGO": "new", "MA": "new", "MU": "new", "ANET": "new", "NU": "new",
}

print(f"\n{'─'*130}")
print(f"{'Status':<9} {'Tick':<6}  {'Price':>9}  {'FwdPE':>7}  {'RevGrw':>8}  {'GM':>7}  {'ROE':>7}  {'Analyst':<13}  {'TargetUpside':>13}  {'vs52wLow':>9}  {'vs52wHigh':>10}")
print(f"{'─'*130}")

for ticker, status in picks.items():
    try:
        t = yf.Ticker(ticker)
        i = t.info
        price  = i.get("currentPrice") or i.get("regularMarketPrice") or 0
        high52 = i.get("fiftyTwoWeekHigh") or 0
        low52  = i.get("fiftyTwoWeekLow") or 0
        fwd_pe = i.get("forwardPE") or 0
        rev_g  = (i.get("revenueGrowth") or 0) * 100
        gm     = (i.get("grossMargins") or 0) * 100
        roe    = (i.get("returnOnEquity") or 0) * 100
        analyst= i.get("recommendationKey") or "N/A"
        target = i.get("targetMeanPrice") or 0
        upside = ((target - price) / price * 100) if price and target else 0
        vs_low = ((price - low52) / low52 * 100) if low52 else 0
        vs_high= ((price - high52) / high52 * 100) if high52 else 0
        print(f"[{status.upper():7}] {ticker:<6}  ${price:>8.2f}  {fwd_pe:>7.1f}  {rev_g:>7.1f}%  {gm:>6.1f}%  {roe:>6.1f}%  {analyst:<13}  {upside:>+12.1f}%  {vs_low:>+8.1f}%  {vs_high:>+9.1f}%")
    except Exception as e:
        print(f"[{status.upper():7}] {ticker:<6}  ERROR: {e}")

print(f"{'─'*130}\n")
