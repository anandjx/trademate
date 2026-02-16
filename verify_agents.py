
import sys
import os
from unittest.mock import MagicMock

# MOCK ADK completely
# We need to mock 'google' first if it doesn't exist
if "google" not in sys.modules:
    sys.modules["google"] = MagicMock()
if "google.adk" not in sys.modules:
    sys.modules["google.adk"] = MagicMock()
if "google.adk.tools" not in sys.modules:
    sys.modules["google.adk.tools"] = MagicMock()

def mock_tool(func):
    return func
sys.modules["google.adk.tools"].tool = mock_tool

# Now import the tools
import pandas as pd
from app.sub_agents.technical_analyst.tools import get_technical_indicators
from app.sub_agents.market_analyst.tools import get_market_data, search_ticker

def test_search():
    print("\nTesting Ticker Search...")
    query = "United Airlines"
    try:
        result = search_ticker(query)
        print(f"✅ Search Result for '{query}':")
        print(result)
        if "UAL" in result:
             print("✅ Correct ticker found.")
        else:
             print("❌ Ticker UAL not found.")
    except Exception as e:
        print(f"❌ Search Failed: {e}")

def test_technical_agent():
    print("Testing TechnicalIndicatorsAgent...")
    ticker = "AAPL"
    try:
        result = get_technical_indicators(ticker)
        print(f"✅ Technical Agent Result for {ticker}:")
        print(result[:200] + "...") # Print start of JSON
        if "RSI" in result and "SMA_20" in result:
            print("✅ key indicators found.")
        else:
            print("❌ Missing key indicators.")
    except Exception as e:
        print(f"❌ Technical Agent Failed: {e}")

def test_market_agent():
    print("\nTesting MarketSenseAgent...")
    ticker = "MSFT"
    try:
        result = get_market_data(ticker)
        print(f"✅ Market Agent Result for {ticker}:")
        print(result[:200] + "...")
        if "market_cap" in result:
            print("✅ Market Cap found.")
        else:
            print("❌ Market data missing.")
    except Exception as e:
        print(f"❌ Market Agent Failed: {e}")

if __name__ == "__main__":
    test_search()
    test_technical_agent()
    test_market_agent()
