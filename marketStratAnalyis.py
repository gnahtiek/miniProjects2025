import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"

# === LOAD DATA ===
data = yf.download(ticker, start=start_date, end=end_date)
data['SMA20'] = data['Close'].rolling(window=20).mean()
data['SMA50'] = data['Close'].rolling(window=50).mean()

# === STRATEGY SIGNALS ===
data['Signal'] = 0
data.loc[data['SMA20'] > data['SMA50'], 'Signal'] = 1
data.loc[data['SMA20'] < data['SMA50'], 'Signal'] = 0
data['Position'] = data['Signal'].diff()

# === RETURNS ===
data['Market Return'] = data['Close'].pct_change()
data['Strategy Return'] = data['Market Return'] * data['Signal'].shift(1)
data['Cumulative Market Return'] = (1 + data['Market Return']).cumprod()
data['Cumulative Strategy Return'] = (1 + data['Strategy Return']).cumprod()

# === PLOT BUY/SELL POINTS ===
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['SMA20'], label='SMA20', alpha=0.75)
plt.plot(data['SMA50'], label='SMA50', alpha=0.75)
plt.plot(data[data['Position'] == 1].index,
         data['Close'][data['Position'] == 1],
         '^', markersize=12, color='green', label='Buy')
plt.plot(data[data['Position'] == -1].index,
         data['Close'][data['Position'] == -1],
         'v', markersize=12, color='red', label='Sell')

plt.title(f"{ticker} Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === PLOT CUMULATIVE RETURNS ===
plt.figure(figsize=(14, 6))
plt.plot(data['Cumulative Market Return'], label='Buy & Hold')
plt.plot(data['Cumulative Strategy Return'], label='Strategy')
plt.title("Cumulative Return Comparison")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
