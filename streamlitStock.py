import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Analysis", layout="wide")

st.title("📈 Stock Price Analysis")

# Dropdown to select ticker
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT):", value="AAPL")

if ticker:
    data = yf.download(ticker, start="2023-01-01", end="2024-01-01")
    
    st.subheader(f"{ticker} Closing Price")
    st.line_chart(data['Close'])

    # Moving Averages
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    data['SMA50'] = data['Close'].rolling(window=50).mean()

    st.subheader("Price with SMA20 & SMA50")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Close'], label='Close Price')
    ax.plot(data['SMA20'], label='SMA20')
    ax.plot(data['SMA50'], label='SMA50')
    ax.legend()
    st.pyplot(fig)

    # Daily Returns
    data['Daily Return (%)'] = data['Close'].pct_change() * 100
    st.subheader("Daily Return (%)")
    st.line_chart(data['Daily Return (%)'])