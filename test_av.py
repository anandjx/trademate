
import sys
import os
from unittest.mock import MagicMock

# Robust Mocking
if "google" not in sys.modules:
    sys.modules["google"] = MagicMock()
if "google.adk" not in sys.modules:
    sys.modules["google.adk"] = MagicMock()
if "google.adk.tools" not in sys.modules:
    sys.modules["google.adk.tools"] = MagicMock()

# Now imports work
from dotenv import load_dotenv
load_dotenv("app/.env")

from app.sub_agents.technical_analyst.tools import download_data

def test_av():
    print("Testing Alpha Vantage Integration...")
    ticker = "IBM" 
    try:
        df = download_data(ticker)
        print(f"✅ Success! Fetched {len(df)} rows for {ticker}.")
        print(df.tail())
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_av()
