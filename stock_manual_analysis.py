import pandas as pd
import numpy as np
import yfinance as yf
import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set chart style
sns.set_style("darkgrid")

# ------------------ Ticker Search ------------------
def find_ticker(query):
    query = query.strip()

    if query.isupper() and ' ' not in query and len(query) <= 5:
        return query

    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotes_count": 5, "country": "United States"}
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()

    data = json.loads(resp.content.decode("utf-8"))
    quotes = data.get("quotes", [])
    if not quotes:
        answer = input(f"No search results found for '{query}'. Use '{query.upper()}' as ticker? (y/n): ")
        if answer.lower().startswith('y'):
            return query.upper()
        else:
            raise ValueError(f"No ticker found for '{query}'")

    print("Top ticker matches found:")
    for idx, q in enumerate(quotes[:5]):
        shortname = q.get("shortname", "")
        symbol = q.get("symbol", "")
        print(f"{idx+1}. {symbol} — {shortname}")

    choice = input("Enter the number of the correct ticker (or press Enter for 1): ")
    if choice.isdigit() and 1 <= int(choice) <= len(quotes[:5]):
        return quotes[int(choice)-1].get("symbol")
    else:
        return quotes[0].get("symbol")

# ------------------ Technical Indicators ------------------
def SMA(series, period):
    return series.rolling(window=period).mean()

def EMA(series, period):
    return series.ewm(span=period, adjust=False).mean()

def RSI(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def MACD(series, fast=12, slow=26, signal=9):
    ema_fast = EMA(series, fast)
    ema_slow = EMA(series, slow)
    macd = ema_fast - ema_slow
    macd_signal = EMA(macd, signal)
    return macd, macd_signal

def Bollinger_Bands(series, period=20, std_dev=2):
    sma = SMA(series, period)
    rolling_std = series.rolling(period).std()
    upper = sma + std_dev * rolling_std
    lower = sma - std_dev * rolling_std
    return upper, lower

# ------------------ Signals ------------------
def generate_signals(data):
    signals = pd.DataFrame(index=data.index)
    signals['Short_Term'] = 0
    signals['Long_Term'] = 0

    # RSI: short-term signals
    signals.loc[data['RSI'] < 30, 'Short_Term'] = 1
    signals.loc[data['RSI'] > 70, 'Short_Term'] = -1

    # SMA crossover: long-term signals
    signals.loc[data['SMA_20'] > data['SMA_50'], 'Long_Term'] = 1
    signals.loc[data['SMA_20'] < data['SMA_50'], 'Long_Term'] = -1

    return signals

# ------------------ Backtesting ------------------
def backtest(data, signals):
    df = data.copy()
    df['Position'] = signals['Long_Term'].shift(1).fillna(0)
    df['Daily_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'] * df['Daily_Return']
    total_return = (1 + df['Strategy_Return']).cumprod()[-1] - 1
    return total_return

# ------------------ Indicator Calculation ------------------
def calculate_indicators(data):
    close = data['Close'].squeeze()
    data['SMA_20'] = SMA(close, 20)
    data['SMA_50'] = SMA(close, 50)
    data['EMA_20'] = EMA(close, 20)
    data['RSI'] = RSI(close, 14)
    data['MACD'], data['MACD_signal'] = MACD(close)
    data['Upper_BB'], data['Lower_BB'] = Bollinger_Bands(close)
    return data

# ------------------ Data Fetch ------------------
def download_data(ticker, start="2020-01-01", end=None):
    data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    data['Close'] = data['Close'].squeeze()
    return data

# ------------------ Plotting ------------------
def plot_stock_analysis(data, signals, ticker):
    dates = data.index
    close = data['Close']

    fig, axes = plt.subplots(4, 1, figsize=(14, 18), sharex=True)

    # ---- Price + SMA/EMA + Bollinger Bands ----
    axes[0].plot(dates, close, label='Close', color='black')
    axes[0].plot(dates, data['SMA_20'], label='SMA 20', color='blue')
    axes[0].plot(dates, data['SMA_50'], label='SMA 50', color='green')
    axes[0].plot(dates, data['EMA_20'], label='EMA 20', color='orange')
    axes[0].fill_between(dates, data['Upper_BB'], data['Lower_BB'], color='gray', alpha=0.2, label='Bollinger Bands')

    buy_signals = signals.index[signals['Long_Term'] == 1]
    sell_signals = signals.index[signals['Long_Term'] == -1]
    axes[0].scatter(buy_signals, close.loc[buy_signals], marker='^', color='green', s=100, label='Buy')
    axes[0].scatter(sell_signals, close.loc[sell_signals], marker='v', color='red', s=100, label='Sell')

    axes[0].set_title(f'{ticker} — Price, SMA, EMA, and Bollinger Bands')
    axes[0].legend()

    # ---- RSI ----
    axes[1].plot(dates, data['RSI'], label='RSI', color='purple')
    axes[1].axhline(70, color='red', linestyle='--')
    axes[1].axhline(30, color='green', linestyle='--')
    axes[1].set_title('Relative Strength Index (RSI)')
    axes[1].legend()

    # ---- MACD ----
    axes[2].plot(dates, data['MACD'], label='MACD', color='blue')
    axes[2].plot(dates, data['MACD_signal'], label='Signal', color='red')
    axes[2].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axes[2].set_title('MACD & Signal Line')
    axes[2].legend()

   
    # ---- Volume ----
    volume = data['Volume'].squeeze()  # Ensure it's 1D
    axes[3].bar(dates, volume, color='skyblue', linewidth=0.5)
    axes[3].set_title('Volume')
    axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()

# ------------------ Print Indicator Summary ------------------
def print_latest_indicators(data):
    last_row = data.iloc[-1]
    print("\nLatest Technical Indicator Values:")
    indicators = ['SMA_20', 'SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_signal', 'Upper_BB', 'Lower_BB']
    for ind in indicators:
        value = last_row[ind]
        if isinstance(value, pd.Series):
            value = value.squeeze()
        print(f"{ind:<12}: {float(value):.2f}")

# ------------------ Main ------------------
def main():
    ticker_input = input("Enter stock ticker or company name: ")
    ticker = find_ticker(ticker_input)
    print(f"Using ticker: {ticker}")

    data = download_data(ticker)
    if data.empty:
        print("No historical data found.")
        return

    data = calculate_indicators(data)
    signals = generate_signals(data)

    print("\nSample signals (last 5 rows):")
    print(signals.tail())

    strategy_return = backtest(data, signals)
    print(f"\nTotal strategy return since {data.index[0].date()}: {strategy_return*100:.2f}%")

    print_latest_indicators(data)
    plot_stock_analysis(data, signals, ticker)


if __name__ == "__main__":
    main()
