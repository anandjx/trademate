
import os
import sys

# Mock Env
os.environ["GOOGLE_CLOUD_PROJECT"] = "custom-ground-482813-s7"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

# Add app to path
sys.path.append("e:\\Cursor\\trademate")

try:
    from app.sub_agents.quant_synthesis.tools import synthesize_reports_func
    
    print("Testing synthesize_reports_func...")
    
    ticker = "AAPL"
    market = "Market Analyst says AAPL is great. Insider buying detected."
    technical = "RSI is 45. MACD bullish."
    oracle = "Forecast: Flat to slightly up."
    
    result = synthesize_reports_func(ticker, market, technical, oracle)
    print("Result:")
    print(result[:100] + "...")
    
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
