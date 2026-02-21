#!/usr/bin/env python3
"""
Portfolio Analysis & Stock Discovery Tool
==========================================
Loads your holdings from holdings.csv, enriches with live yfinance data,
and screens a curated universe for new names matching your investment style.

Usage:
    python analyzer.py                    # Portfolio summary only
    python analyzer.py --screen           # Summary + new stock ideas
    python analyzer.py --screen --report  # Also saves report.md
    python analyzer.py --fast             # Skip live enrichment (use CSV values)
"""

import argparse
import warnings
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

HERE = Path(__file__).parent
HOLDINGS_FILE = HERE / "holdings.csv"
REPORT_FILE = HERE / "report.md"

# ── Screening universe ────────────────────────────────────────────────────────
# Curated candidates aligned with your investment style:
# AI infra, semiconductors, cloud, fintech, consumer moats, international growth
SCREEN_UNIVERSE = [
    # AI / Cloud / Software
    "ORCL", "SAP", "WDAY", "NOW", "DDOG", "MDB", "NET", "CRWD", "ZS", "PANW",
    "MSTR", "ANET", "SMCI", "APP", "GTLB", "HCP",
    # Semiconductors
    "AVGO", "QCOM", "INTC", "MU", "MRVL", "LRCX", "KLAC", "AMAT", "ASML", "ARM",
    # Fintech / Finance
    "V", "MA", "SQ", "COIN", "NU", "HOOD", "SOFI",
    # Consumer / Retail
    "COST", "NKE", "SBUX", "DUOL",
    # Healthcare / Biotech
    "LLY", "NVO", "ABBV", "ISRG",
    # Energy
    "XOM", "CVX",
    # International
    "SE", "MELI", "GRAB",
    # Industrial / Robotics / Defense
    "DE", "CAT", "RTX", "LMT", "HON", "AXON",
    # EV / Mobility
    "RIVN", "NIO", "LI",
]

CRYPTO_SUFFIX = "USD"

# ── Data loading ──────────────────────────────────────────────────────────────

def load_holdings() -> pd.DataFrame:
    df = pd.read_csv(HOLDINGS_FILE)
    df["value_usd"] = pd.to_numeric(df["value_usd"], errors="coerce").fillna(0)
    return df


def is_crypto(ticker: str) -> bool:
    return CRYPTO_SUFFIX in ticker.upper()


def is_etf(row: pd.Series) -> bool:
    return row.get("type", "").upper() == "ETF"


def safe_get(info: dict, *keys):
    for k in keys:
        v = info.get(k)
        if v is not None:
            return v
    return None


def fetch_info(ticker: str) -> dict:
    """Fetch yfinance info dict with safe fallbacks."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        price = safe_get(info, "currentPrice", "regularMarketPrice", "ask", "bid")
        return {
            "name":           safe_get(info, "shortName", "longName") or ticker,
            "live_price":     price,
            "mkt_cap":        info.get("marketCap"),
            "pe_ttm":         info.get("trailingPE"),
            "fwd_pe":         info.get("forwardPE"),
            "peg":            info.get("pegRatio"),
            "ps":             info.get("priceToSalesTrailing12Months"),
            "pb":             info.get("priceToBook"),
            "rev_growth":     info.get("revenueGrowth"),
            "earn_growth":    info.get("earningsGrowth"),
            "gross_margin":   info.get("grossMargins"),
            "roe":            info.get("returnOnEquity"),
            "fcf":            info.get("freeCashflow"),
            "debt_equity":    info.get("debtToEquity"),
            "beta":           info.get("beta"),
            "analyst":        info.get("recommendationKey"),
            "target_price":   info.get("targetMeanPrice"),
            "sector_live":    info.get("sector", ""),
            "industry":       info.get("industry", ""),
            "w52_high":       info.get("fiftyTwoWeekHigh"),
            "w52_low":        info.get("fiftyTwoWeekLow"),
        }
    except Exception:
        return {}


def fetch_crypto_price(ticker: str) -> dict:
    """Fetch current price for a crypto ticker."""
    try:
        hist = yf.download(ticker, period="2d", progress=False)
        if not hist.empty:
            return {"live_price": float(hist["Close"].iloc[-1])}
    except Exception:
        pass
    return {}


def enrich_holdings(df: pd.DataFrame) -> pd.DataFrame:
    print("  Fetching live data for holdings", end="", flush=True)
    enriched = []
    for _, row in df.iterrows():
        ticker = row["ticker"]
        if is_crypto(ticker):
            extra = fetch_crypto_price(ticker)
        else:
            extra = fetch_info(ticker)
        enriched.append({**row.to_dict(), **extra})
        print(".", end="", flush=True)
    print(" done.")
    return pd.DataFrame(enriched)


# ── Portfolio display ─────────────────────────────────────────────────────────

def print_header(title: str):
    print(f"\n{'═'*62}")
    print(f"  {title}")
    print(f"{'═'*62}")


def portfolio_summary(df: pd.DataFrame):
    total = df["value_usd"].sum()
    print_header(f"PORTFOLIO SUMMARY  ·  {datetime.today().strftime('%Y-%m-%d')}")
    print(f"  Total value : ${total:>13,.2f}")
    print(f"  Holdings    : {len(df)}")

    # Sector allocation
    sector_totals = df.groupby("sector")["value_usd"].sum().sort_values(ascending=False)
    print(f"\n  {'Sector':<30} {'Value':>12}  {'%':>6}  Allocation")
    print(f"  {'─'*62}")
    for sector, val in sector_totals.items():
        pct = val / total * 100
        bar = "█" * max(1, int(pct / 1.5))
        print(f"  {sector:<30} ${val:>10,.0f}  {pct:>5.1f}%  {bar}")

    # Horizon allocation
    horizon_totals = df.groupby("horizon")["value_usd"].sum().sort_values(ascending=False)
    print(f"\n  {'Horizon':<22} {'Value':>12}  {'%':>6}")
    print(f"  {'─'*44}")
    for horizon, val in horizon_totals.items():
        pct = val / total * 100
        print(f"  {horizon:<22} ${val:>10,.0f}  {pct:>5.1f}%")


def top_holdings(df: pd.DataFrame, n: int = 10):
    total = df["value_usd"].sum()
    top = df.nlargest(n, "value_usd")
    print(f"\n  Top {n} Holdings:")
    print(f"  {'Ticker':<8} {'Value':>13}  {'%':>6}  {'Horizon':<18}  Sector")
    print(f"  {'─'*70}")
    for _, r in top.iterrows():
        pct = r["value_usd"] / total * 100
        live_note = ""
        if r.get("live_price"):
            live_note = f"  @ ${r['live_price']:.2f}"
        print(f"  {r['ticker']:<8} ${r['value_usd']:>11,.0f}  {pct:>5.1f}%  {r['horizon']:<18}  {r['sector']}{live_note}")


def valuation_snapshot(df: pd.DataFrame):
    """Show key valuation metrics for equity holdings."""
    equities = df[df["type"] == "Equity"].copy()
    if equities.empty or "fwd_pe" not in equities.columns:
        return
    cols = ["ticker", "live_price", "pe_ttm", "fwd_pe", "rev_growth", "gross_margin", "analyst"]
    display = equities[cols].copy()
    display = display.dropna(subset=["fwd_pe"], how="all")
    if display.empty:
        return

    print(f"\n  Valuation Snapshot (equities only):")
    print(f"  {'Ticker':<8} {'Price':>9} {'PE TTM':>8} {'Fwd PE':>8} {'RevGrw':>8} {'GrsMgn':>8}  Analyst")
    print(f"  {'─'*68}")
    for _, r in display.iterrows():
        price  = f"${r['live_price']:>8.2f}" if pd.notna(r.get("live_price")) else "       N/A"
        pe_ttm = f"{r['pe_ttm']:>8.1f}"     if pd.notna(r.get("pe_ttm"))    else "       N/A"
        fwd_pe = f"{r['fwd_pe']:>8.1f}"     if pd.notna(r.get("fwd_pe"))    else "       N/A"
        rev_g  = f"{r['rev_growth']*100:>7.1f}%" if pd.notna(r.get("rev_growth")) else "      N/A"
        gm     = f"{r['gross_margin']*100:>7.1f}%" if pd.notna(r.get("gross_margin")) else "      N/A"
        analyst = str(r.get("analyst") or "N/A")
        print(f"  {r['ticker']:<8} {price} {pe_ttm} {fwd_pe} {rev_g} {gm}  {analyst}")


# ── Stock screener ────────────────────────────────────────────────────────────

def score_candidate(info: dict) -> float:
    """
    Score a candidate 0–10 based on alignment with portfolio style:
    growth + quality + reasonable valuation + momentum.
    """
    score = 0.0

    # 1. Revenue growth (0–3 pts)
    rg = info.get("rev_growth") or 0
    score += min(rg, 0.5) / 0.5 * 3

    # 2. Forward P/E in growth-quality range (0–2 pts)
    fpe = info.get("fwd_pe")
    if fpe and fpe > 0:
        if 15 <= fpe <= 45:
            score += 2
        elif fpe < 15 or fpe <= 70:
            score += 1

    # 3. ROE > 15% (0–1.5 pts)
    roe = info.get("roe") or 0
    if roe > 0.25:
        score += 1.5
    elif roe > 0.15:
        score += 1.0

    # 4. Analyst bullish (0–2 pts)
    analyst = (info.get("analyst") or "").lower()
    if analyst == "strong_buy":
        score += 2
    elif analyst == "buy":
        score += 1.5

    # 5. Price within 15% of 52w high — momentum (0–1 pt)
    price = info.get("live_price")
    high  = info.get("w52_high")
    if price and high and high > 0:
        pct_from_high = price / high
        if pct_from_high >= 0.85:
            score += 1.0
        elif pct_from_high >= 0.70:
            score += 0.5

    # 6. Gross margin > 40% — software / quality bias (0–0.5 pts)
    gm = info.get("gross_margin") or 0
    if gm > 0.60:
        score += 0.5
    elif gm > 0.40:
        score += 0.25

    return round(score, 2)


def screen_candidates(existing_tickers: set) -> pd.DataFrame:
    universe = [t for t in SCREEN_UNIVERSE if t not in existing_tickers]
    print_header(f"SCREENING {len(universe)} CANDIDATES FOR NEW IDEAS")
    print(f"  Pulling data", end="", flush=True)

    rows = []
    for ticker in universe:
        info = fetch_info(ticker)
        if not info or not info.get("live_price"):
            print("·", end="", flush=True)
            continue
        info["ticker"] = ticker
        info["score"]  = score_candidate(info)
        rows.append(info)
        print(".", end="", flush=True)
    print(" done.\n")

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).sort_values("score", ascending=False)
    return df.head(15).reset_index(drop=True)


def print_candidates(df: pd.DataFrame):
    if df.empty:
        print("  No candidates found.")
        return

    print(f"  Ranked by: revenue growth · valuation · ROE · analyst rating · momentum\n")
    print(f"  {'#':<3} {'Ticker':<7} {'Name':<24} {'Price':>9} {'FwdPE':>7} {'RevGrw':>8} {'GrsMgn':>8} {'Score':>6}  Analyst")
    print(f"  {'─'*84}")

    for i, (_, r) in enumerate(df.iterrows(), 1):
        name    = str(r.get("name", ""))[:22]
        price   = f"${r['live_price']:>8.2f}"   if r.get("live_price")   else "       N/A"
        fwd_pe  = f"{r['fwd_pe']:>7.1f}"        if pd.notna(r.get("fwd_pe")) else "    N/A"
        rev_g   = f"{r['rev_growth']*100:>7.1f}%" if pd.notna(r.get("rev_growth")) else "     N/A"
        gm      = f"{r['gross_margin']*100:>7.1f}%" if pd.notna(r.get("gross_margin")) else "     N/A"
        score   = f"{r['score']:>6.2f}"
        analyst = str(r.get("analyst") or "N/A")
        sector  = str(r.get("sector_live") or "")[:20]
        print(f"  {i:<3} {r['ticker']:<7} {name:<24} {price} {fwd_pe} {rev_g} {gm} {score}  {analyst}  {sector}")

    print(f"\n  Score legend: 10 = perfect match · 7+ = strong candidate · <5 = weaker fit")


# ── Report ────────────────────────────────────────────────────────────────────

def save_report(holdings: pd.DataFrame, candidates: pd.DataFrame):
    total = holdings["value_usd"].sum()
    date  = datetime.today().strftime("%Y-%m-%d")
    lines = [
        f"# Portfolio Report — {date}",
        "",
        f"**Total value:** ${total:,.2f}  |  **Holdings:** {len(holdings)}",
        "",
        "## Sector Allocation",
        "",
    ]

    sector_df = holdings.groupby("sector")["value_usd"].sum().sort_values(ascending=False)
    for s, v in sector_df.items():
        lines.append(f"- **{s}**: ${v:,.0f} ({v/total*100:.1f}%)")

    lines += ["", "## Horizon Allocation", ""]
    horizon_df = holdings.groupby("horizon")["value_usd"].sum().sort_values(ascending=False)
    for h, v in horizon_df.items():
        lines.append(f"- **{h}**: ${v:,.0f} ({v/total*100:.1f}%)")

    if not candidates.empty:
        lines += [
            "", "## Screened Candidates", "",
            f"| # | Ticker | Name | Price | Fwd PE | Rev Growth | Gross Margin | Score | Analyst |",
            f"| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for i, (_, r) in enumerate(candidates.iterrows(), 1):
            name  = str(r.get("name", ""))[:22]
            price = f"${r['live_price']:.2f}"         if r.get("live_price")       else "N/A"
            fpe   = f"{r['fwd_pe']:.1f}"              if pd.notna(r.get("fwd_pe")) else "N/A"
            rg    = f"{r['rev_growth']*100:.1f}%"     if pd.notna(r.get("rev_growth")) else "N/A"
            gm    = f"{r['gross_margin']*100:.1f}%"   if pd.notna(r.get("gross_margin")) else "N/A"
            score = f"{r['score']:.2f}"
            lines.append(f"| {i} | {r['ticker']} | {name} | {price} | {fpe} | {rg} | {gm} | {score} | {r.get('analyst','N/A')} |")

    REPORT_FILE.write_text("\n".join(lines))
    print(f"\n  Report saved → {REPORT_FILE}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Portfolio analyzer + stock screener")
    parser.add_argument("--screen", action="store_true", help="Screen for new stock ideas")
    parser.add_argument("--report", action="store_true", help="Save markdown report")
    parser.add_argument("--fast",   action="store_true", help="Skip live yfinance enrichment")
    parser.add_argument("--top",    type=int, default=10, help="Number of top holdings to show (default 10)")
    args = parser.parse_args()

    holdings = load_holdings()

    if not args.fast:
        holdings = enrich_holdings(holdings)

    portfolio_summary(holdings)
    top_holdings(holdings, n=args.top)

    if not args.fast:
        valuation_snapshot(holdings)

    candidates = pd.DataFrame()
    if args.screen:
        existing = set(holdings["ticker"].str.upper())
        candidates = screen_candidates(existing)
        print_candidates(candidates)

    if args.report:
        save_report(holdings, candidates)

    print()


if __name__ == "__main__":
    main()
