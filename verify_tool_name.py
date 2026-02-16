
from google.adk.tools import FunctionTool

def dummy_func():
    pass

try:
    tool = FunctionTool(func=dummy_func, name="test_tool")
    print("SUCCESS: FunctionTool accepts 'name' parameter.")
except TypeError:
    print("FAILURE: FunctionTool does NOT accept 'name' parameter.")
except Exception as e:
    print(f"ERROR: {e}")
