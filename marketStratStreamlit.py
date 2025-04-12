import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Moving Average Crossover Strategy", layout="wide")
st.title("📈 Moving Average Crossover Strategy")

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))
short_window = st.sidebar.slider("Short-term SMA Window", min_value=5, max_value=50, value=20)
long_window = st.sidebar.slider("Long-term SMA Window", min_value=20, max_value=100, value=50)

# --- Load Data ---
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df

data = load_data(ticker, start_date, end_date)

# --- Calculate SMAs and Signals ---
data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
data['Signal'] = 0
data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
data['Position'] = data['Signal'].diff()

# --- Plot Prices and Signals ---
st.subheader(f"{ticker} Price Chart with Buy/Sell Signals")

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(data['Close'], label='Close Price', alpha=0.5)
ax.plot(data['SMA_Short'], label=f"SMA{short_window}")
ax.plot(data['SMA_Long'], label=f"SMA{long_window}")
ax.plot(data[data['Position'] == 1].index, 
        data['Close'][data['Position'] == 1], 
        '^', markersize=10, color='green', label='Buy Signal')
ax.plot(data[data['Position'] == -1].index, 
        data['Close'][data['Position'] == -1], 
        'v', markersize=10, color='red', label='Sell Signal')
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid()
st.pyplot(fig)

# --- Strategy vs Market Performance ---
data['Market Return'] = data['Close'].pct_change()
data['Strategy Return'] = data['Market Return'] * data['Signal'].shift(1)
data['Cumulative Market Return'] = (1 + data['Market Return']).cumprod()
data['Cumulative Strategy Return'] = (1 + data['Strategy Return']).cumprod()

st.subheader("📊 Cumulative Returns")

fig2, ax2 = plt.subplots(figsize=(14, 5))
ax2.plot(data['Cumulative Market Return'], label='Buy & Hold Strategy')
ax2.plot(data['Cumulative Strategy Return'], label='Moving Average Strategy')
ax2.set_xlabel("Date")
ax2.set_ylabel("Cumulative Return")
ax2.legend()
ax2.grid()
st.pyplot(fig2)

# --- Show raw data if checked ---
if st.checkbox("Show Raw Data"):
    st.write(data.tail(50))
