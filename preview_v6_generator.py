
import json
import sys
import os

# Add project root to path so we can import app modules
sys.path.insert(0, os.getcwd())

from app.sub_agents.report_generator.tools_v6 import _build_report_html, _build_payload

# Mock Data State simulating a full agent run
mock_state = {
    "market_analysis": {
        "current_price": 450.25,
        "market_cap": "1.2T",
        "sentiment": "Cautiously Optimistic",
        "report": """
### Market Intelligence
**NVIDIA (NVDA)** continues to dominate the AI hardware narrative, though recent supply chain constraints have tempered short-term exuberance.
*   **Key Driver:** H100 demand remains outstripped by supply until Q3.
*   **Risk:** Geopolitical chip export controls remain a primary overhang.
*   **Sentiment:** Institutional accumulation verified in dark pool data.
        """
    },
    "technical_analysis": {
        "price": 450.25,
        "rsi": 62.5,
        "macd": "Bullish Divergence",
        "trend": "Uptrend",
        "rating": "Buy",
        "support_levels": [430.0, 415.0],
        "resistance_levels": [465.0, 480.0]
    },
    "oracle_predictor": {
        "predicted_price": 485.00,
        "model_confidence": 0.88,
        "forecast_horizon": "14 Days",
        "confidence_interval": [470.0, 500.0]
    },
    "quant_synthesis": {
        "overall_signal": "Accumulate",
        "confidence_score": 85,
        "summary": """
### Synthesis
Quantitative models indicate a **Strong Buy** signal effectively. The convergence of **Oracle's 88% confidence** upside target and **Constructive Technicals** supports a long position.
*   **Conviction:** High (8.5/10)
*   **Asymmetry:** +7.7% projected upside vs 3% downside risk to immediate support.
        """
    },
    "strategic_report": {
        "signal": "LONG_VOL",
        "time_horizon": "2 Weeks",
        "narrative": """
### Strategic Blueprint: Project AETHER
**Primary Thesis:** Long volatility exposure via call spreads is favored given the compressed IV rank (12%) and imminent product announcement.
1.  **Entry:** Limit buy at $448-450 zone.
2.  **Stop:** Hard close below $430 (20-day SMA violation).
3.  **Target:** $485 (Oracle Mean Reversion).

*Constraint:* Avoid leverage exceeding 2x given macro-event risk next week.
        """
    }
}

def generate_preview():
    print("Generating V6 Versailles Preview...")
    
    # simulate the payload build
    payload = _build_payload("NVDA", mock_state)
    
    # generate html
    html = _build_report_html(payload)
    
    # save
    outfile = "v6_preview_nvda.html"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"✅ Preview generated: {os.path.abspath(outfile)}")

if __name__ == "__main__":
    generate_preview()
