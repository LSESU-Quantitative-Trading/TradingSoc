import matplotlib
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def getStockData():
    ticker = yf.Ticker('BTC-GBP')
    df = ticker.history(period="max")
    return df

df = getStockData()

plt.figure(figsize=(10,10))
plt.plot(df.index, df['Close'])
plt.xlabel("date")
plt.ylabel("$ price")
plt.title("Historic Closing Price of Bitcoin")

df["SMA1"] = df['Close'].rolling(window=7).mean()
df["SMA2"] = df['Close'].rolling(window=14).mean()

plt.plot(df['SMA1'], 'g--', label="SMA1")
plt.plot(df['SMA2'], 'r--', label="SMA2")
plt.plot(df['Close'], label="Closing Prices")

prices = np.array(df["Close"])
maPrices = np.array(df["SMA1"])
diffs = maPrices - prices
diffs[np.isnan(diffs)] = 0
diffs = (((diffs - np.amin(diffs)) / (np.amax(diffs) - np.amin(diffs))) * 2) - 1
holding = 0
money = 10000
df["Backtest"] = df['Close']
for i in range(len(prices)):
    volume = diffs[i] * 1
    if (diffs[i] < 0 and holding >= volume) or (diffs[i] > 0 and money >= volume):
        holding += volume
        money -= volume * prices[i]
    df["Backtest"][i] = money + (holding * prices[i])

plt.plot(df["Backtest"], label="Backtest")

plt.legend()
plt.show()