"""Generate static V7b previews — both USD and INR tickers to verify currency."""
import sys, os
sys.path.insert(0, os.getcwd())
from app.sub_agents.report_generator.tools import _build_payload, _build_report_html

mock_state = {
    "market_analysis": {
        "current_price": 543.65,
        "market_cap": "₹54,365 Cr",
        "sentiment": "Cautiously Optimistic",
        "report": """## **Market Analysis Report for: ANANTRAJ.NS**

*Analysis based on: Anant Raj Limited*
Report Date: February 16, 2026

**1. Executive Summary:**

Anant Raj Limited (ANANTRAJ.NS) is undergoing a significant strategic shift, diversifying from traditional real estate into the high-growth data center segment, marked by a recent partnership with Airtel and aggressive expansion targets.
* The company reported strong financial results for Q3 FY26, with consolidated net profit increasing by 35% and total income rising by 22.1%, signaling robust operational performance.
* Despite positive financial trends and analyst "Strong Buy" recommendations with substantial price targets, market sentiment is mixed, with the stock recently experiencing marked declines due to high valuation and an escalating sell-off.

**2. Recent SEC Filings & Regulatory Information:**

Recent filings indicate aggressive expansion and partnership activity.
* Anant Raj has informed BSE and NSE about an upcoming Board of Directors meeting on January 31, 2026, to consider and approve the unaudited financial results (Standalone and Consolidated) for the quarter and nine months ending December 31, 2025.
* The company publicly announced strong Q3 FY26 earnings, with consolidated net profit up 35% to ₹264.13 crore and total income rising to ₹882.40 crore, as per regulatory filings.

**3. Recent News, Stock Performance Context & Market Sentiment:**

* **Significant News:** Anant Raj's shares jumped over 3.5% on February 4, 2026, following the announcement of a partnership between its subsidiary, Anant Raj Cloud, and Airtel's infrastructure provider Nxtra. The collaboration aims to develop fully operational AI-ready data centers across India.
* **Stock Performance Context:** Anant Raj shares experienced a significant drop of nearly 7% on February 14, 2026. The stock also closed down nearly 3% on February 13, 2026, as part of a broader market sell-off in the mid-cap real estate sector.

**4. Recent Analyst Commentary & Outlook:**

Analyst sentiment for Anant Raj remains broadly constructive, with most maintaining "Buy" or "Outperform" ratings.
* The average broker rating on Anant Raj is "Strong Buy," with 4 analysts giving a strong buy rating and 1 analyst a buy rating.
* Motilal Oswal and Nirmal have issued "Buy" recommendations with price targets ranging from ₹862 to ₹906.

**5. Narrative Positioning & Momentum Intelligence:**

Anant Raj's positioning reflects a company in a pivotal transition. The data center push represents a transformational bet on digital infrastructure.
* Content moat: Combined with partners like Airtel's Nxtra, Anant Raj could control significant data center capacity.
* Real estate stability: Traditional real estate operations continue to generate stable cash flows.

**6. Key Risks & Opportunities:**

Risks: High valuation at 6.60 times book value, low return on equity, execution risk on data center buildout.
Opportunities: Digital infrastructure demand, partnership with Airtel, government incentives for data centers, real estate cycle upswing.

**7. Bull Case (Why Investors Are Optimistic) and Bear Case (Why Skeptics Are Concerned):**

Bull Case: The data center pivot positions Anant Raj in one of India's fastest-growing infrastructure segments. The Airtel partnership de-risks execution substantially.

Bear Case: Current valuations leave little margin for error. Mid-cap real estate stocks are vulnerable to broader market corrections and rising interest rates.
"""
    },
    "technical_analysis": {
        "price": 543.65,
        "rsi": 56.89,
        "macd": "Bearish",
        "trend": "Downtrend",
        "rating": "HOLD",
        "sma_20": 554.67,
        "sma_50": 589.23,
        "bollinger_upper": 614.30,
        "bollinger_lower": 489.01,
        "support_levels": [501.24, 489.01],
        "resistance_levels": [554.67, 589.23, 614.30]
    },
    "oracle_forecast": {
        "predicted_price": 565.24,
        "model_confidence": 0.62,
        "forecast_horizon": "10 Days",
        "confidence_interval": [478.55, 651.93]
    },
    "quant_synthesis": {
        "overall_signal": "Balanced",
        "confidence_score": 55,
        "summary": """### Quantitative Convergence Profile

The model portfolio signals are in a state of **moderate divergence**, reflecting the tug-of-war between fundamental value and technical deterioration.

**Signal Matrix:**
- Oracle: Mildly Bullish (target ₹565.24 vs current ₹543.65, +4.0% asymmetry)
- Technical: Neutral (RSI 56.89 — mid-range)
- Momentum: Mildly Bearish (price below SMA-20 and SMA-50)

**Interpretation:**
The quantitative framework flags this as a **transition zone** where directional conviction is low. The Oracle's +4% asymmetry provides modest upside bias but insufficient for aggressive positioning.

**Risk-Reward Ratio:** 1.4x (marginal for new entries)
"""
    },
    "strategic_report": {
        "signal": "HOLD",
        "time_horizon": "2-4 Weeks",
        "narrative": """### Investment Thesis: Wait for Confirmation

Anant Raj presents a **watchlist candidate** with strong long-term fundamentals but near-term technical weakness.

**The Setup:**
1. Fundamental anchor: Data center expansion with Airtel partnership provides growth visibility.
2. Technical reality: RSI at 56.89 is neutral. Price is below both key SMAs, suggesting bearish momentum.
3. Oracle signal: The ₹565.24 target offers ~4% asymmetry — insufficient for high-conviction positioning.

**Recommended Action:**
* HOLD existing positions. Do not add at current levels.
* Set alerts at ₹555 (SMA-20 reclaim) for re-evaluation.
* If price reclaims ₹555 AND RSI holds above 60, upgrade to Accumulate.

**Risk Management:**
- Hard stop: ₹485 (below Bollinger lower band)
- Position size: Max 4% of portfolio given mid-cap volatility
"""
    }
}

# ── Indian ticker (INR)
payload = _build_payload("ANANTRAJ.NS", mock_state)
html = _build_report_html(payload)
with open("v7b_preview_anantraj.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"INR Preview: v7b_preview_anantraj.html ({len(html)} chars)")

# ── Quick USD ticker too
mock_state_usd = {
    "market_analysis": {"current_price": 76.87, "sentiment": "Cautiously Optimistic",
        "report": "**1. Executive Summary:**\nNetflix is strong.\n\n**2. Recent SEC Filings:**\nMultiple filings noted."},
    "technical_analysis": {"price": 76.87, "rsi": 24.79, "macd": "Bearish", "trend": "Downtrend",
        "sma_20": 82.34, "sma_50": 89.23, "bollinger_upper": 92.74, "bollinger_lower": 69.53,
        "support_levels": [76.25, 70.21], "resistance_levels": [82.34, 89.53]},
    "oracle_forecast": {"predicted_price": 76.82, "model_confidence": 0.74, "forecast_horizon": "10 Days",
        "confidence_interval": [72.50, 81.15]},
    "quant_synthesis": {"overall_signal": "Capitulation", "confidence_score": 35,
        "summary": "### Quantitative Convergence\nSignals: **extreme divergence**."},
    "strategic_report": {"signal": "HOLD", "time_horizon": "2-4 Weeks",
        "narrative": "### Investment Thesis\nCautious patience recommended."},
}
payload2 = _build_payload("NFLX", mock_state_usd)
html2 = _build_report_html(payload2)
with open("v7b_preview_nflx.html", "w", encoding="utf-8") as f:
    f.write(html2)
print(f"USD Preview: v7b_preview_nflx.html ({len(html2)} chars)")
