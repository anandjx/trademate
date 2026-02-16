import sys
import os
import logging

# Ensure we can import from 'app'
sys.path.append(os.getcwd())

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

print("--- ORACLE DEBUG START ---")
print("1. Importing tools...")

try:
    from app.sub_agents.oracle_predictor.tools import clean_and_forecast_func
    print("   Success.")
except ImportError as e:
    print(f"   IMPORT ERROR: {e}")
    sys.exit(1)

target = "NVDA"
print(f"2. Running clean_and_forecast_func('{target}')...")

try:
    # Run the function synchronously
    result_json = clean_and_forecast_func(target)
    
    print("\n3. --- FUNCTION RETURNED ---")
    print(f"Result Type: {type(result_json)}")
    print(f"Result Preview: {result_json[:200]}...")
    
    # Verify it is valid JSON
    import json
    data = json.loads(result_json)
    
    if data.get("status") == "success":
        print("\n✅ SUCCESS: Forecast Generated.")
        print(f"   Forecast Count: {len(data.get('forecast', []))}")
        print(f"   Last Real Price: {data.get('last_real_price')}")
    else:
        print("\n❌ FAILURE: Tool returned error status.")
        print(f"   Error: {data.get('error_message')}")
        print(f"   Raw: {data}")

except Exception as e:
    print("\n❌ CRASH: Uncaught Exception during execution.")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n--- ORACLE DEBUG END ---")
