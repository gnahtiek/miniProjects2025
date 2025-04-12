import yfinance as yf
import pandas as pd

# Get stock data (e.g., Apple)
data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")
data["SMA20"] = data["Close"].rolling(window=20).mean()
data["SMA50"] = data["Close"].rolling(window=50).mean()

data[["Close", "SMA20", "SMA50"]].plot(figsize=(12,6)) #SMA plot example of 20 and 50 days for AAPL
data["Signal"] = 0
data["Signal"][20:] = \
    (data["SMA20"][20:] > data["SMA50"][20:]).astype(int)

data["Position"] = data["Signal"].diff()
# Buy: Position = 1, Sell: Position = -1
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(data["Close"], label='Close Price')
plt.plot(data["SMA20"], label='SMA20')
plt.plot(data["SMA50"], label='SMA50')

# Mark buy/sell
plt.plot(data[data["Position"] == 1].index,
         data["SMA20"][data["Position"] == 1],
         '^', markersize=10, color='g', label='Buy')

plt.plot(data[data["Position"] == -1].index,
         data["SMA20"][data["Position"] == -1],
         'v', markersize=10, color='r', label='Sell')

plt.legend()
plt.title('Moving Average Crossover Strategy')
plt.show()
data['Return'] = data['Close'].pct_change()
data['Strategy'] = data['Return'] * data['Signal'].shift(1)
(data[['Return', 'Strategy']] + 1).cumprod().plot(figsize=(12,6))
plt.title('Cumulative Returns')
plt.legend(['Market', 'Strategy'])

# Calculate daily percentage return
data['Daily Return (%)'] = data['Close'].pct_change() * 100

# Drop NaN and compute volatility
volatility = data['Daily Return (%)'].dropna().std()

print(f"Volatility of AAPL in 2023: {volatility:.2f}%")

