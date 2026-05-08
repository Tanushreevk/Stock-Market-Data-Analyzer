# ==========================================
# Stock Market Data Analyzer
# ==========================================

# Import required libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
import os

# ==========================================
# USER INPUT
# ==========================================

ticker = input("Enter Stock Ticker (Example: AAPL): ").upper()

start_date = input("Enter Start Date (YYYY-MM-DD): ")

end_date = input("Enter End Date (YYYY-MM-DD): ")

# ==========================================
# FETCH STOCK DATA
# ==========================================

print("\nFetching stock market data...\n")

stock_data = yf.download(
    ticker,
    start=start_date,
    end=end_date
)
# Fix multi-level columns issue

if isinstance(stock_data.columns, pd.MultiIndex):
    stock_data.columns = stock_data.columns.get_level_values(0)

# ==========================================
# CHECK DATA
# ==========================================

if stock_data.empty:
    print("No data found.")
    exit()

print("Stock data fetched successfully!\n")

# ==========================================
# SAVE CSV FILE
# ==========================================

csv_path = f"data/{ticker}_stock_data.csv"

stock_data.to_csv(csv_path)

print(f"CSV file saved at: {csv_path}")

# ==========================================
# DATA CLEANING
# ==========================================

print("\nCleaning data...\n")

stock_data.dropna(inplace=True)

# ==========================================
# DAILY RETURNS
# ==========================================

stock_data['Daily Return'] = stock_data['Close'].pct_change()

# ==========================================
# MOVING AVERAGES
# ==========================================

stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()

stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()

# ==========================================
# VOLATILITY
# ==========================================

volatility = stock_data['Daily Return'].std()

# ==========================================
# HIGHEST & LOWEST PRICE
# ==========================================

highest_price = stock_data['High'].max()

lowest_price = stock_data['Low'].min()
# ==========================================
# PRINT SUMMARY
# ==========================================

print("\n========== STOCK SUMMARY ==========")

print(f"Ticker: {ticker}")

print(f"Highest Price: {highest_price:.2f}")

print(f"Lowest Price: {lowest_price:.2f}")

print(f"Volatility: {volatility:.4f}")

print("===================================\n")

# ==========================================
# BASIC TREND INSIGHTS
# ==========================================

latest_close = stock_data['Close'].iloc[-1]

average_close = stock_data['Close'].mean()

print("========== MARKET INSIGHTS ==========")

if latest_close > average_close:
    print("Market Trend: Bullish (Above Average)")
else:
    print("Market Trend: Bearish (Below Average)")

if volatility > 0.02:
    print("Risk Level: High Volatility")
else:
    print("Risk Level: Moderate Volatility")

print("=====================================\n")

# ==========================================
# VISUALIZATION 1
# Closing Price Chart
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(stock_data['Close'])

plt.title(f"{ticker} Closing Price")

plt.xlabel("Date")

plt.ylabel("Price")

plt.savefig(f"images/{ticker}_closing_price.png")

plt.close()

print("Closing price chart saved.")

# ==========================================
# VISUALIZATION 2
# Moving Average Chart
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(stock_data['Close'], label='Closing Price')

plt.plot(stock_data['MA20'], label='20-Day MA')

plt.plot(stock_data['MA50'], label='50-Day MA')

plt.title(f"{ticker} Moving Average Analysis")

plt.xlabel("Date")

plt.ylabel("Price")

plt.legend()

plt.savefig(f"images/{ticker}_moving_average.png")

plt.close()

print("Moving average chart saved.")

# ==========================================
# VISUALIZATION 3
# Daily Return Distribution
# ==========================================

plt.figure(figsize=(10, 5))

sns.histplot(
    stock_data['Daily Return'].dropna(),
    bins=50
)

plt.title(f"{ticker} Daily Return Distribution")

plt.savefig(f"images/{ticker}_returns_distribution.png")

plt.close()

print("Return distribution chart saved.")

# ==========================================
# GENERATE REPORT
# ==========================================

report = f"""
=====================================
STOCK MARKET ANALYSIS REPORT
=====================================

Ticker: {ticker}

Analysis Period:
{start_date} to {end_date}

Highest Price:
{highest_price:.2f}

Lowest Price:
{lowest_price:.2f}

Volatility:
{volatility:.4f}

Average Daily Return:
{stock_data['Daily Return'].mean():.4f}

=====================================
Project completed successfully!
=====================================
"""

report_path = f"reports/{ticker}_report.txt"

with open(report_path, "w") as file:
    file.write(report)

print(f"\nReport saved at: {report_path}")

print("\nAll analysis completed successfully!")