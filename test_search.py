
from app.sub_agents.market_analyst.tools import search_ticker_func

def test_search():
    query = "Adani Power"
    print(f"Searching for: {query}")
    result = search_ticker_func(query)
    print("Result:")
    print(result)

if __name__ == "__main__":
    test_search()
