import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import random

def getStockData():
    ticker = yf.Ticker('ASC')
    df = ticker.history(period="1y") #https://yahooquery.dpguthrie.com/guide/ticker/historical/
    return df

df = getStockData()

# plt.figure(figsize=(10,10))
# plt.plot(df.index, df['Close'])
# plt.xlabel("date")
# plt.ylabel("$ price")
# plt.title("Historic Closing Price of Bitcoin")

df["Close"] /= df["Close"][0]

df["SMA1"] = df['Close'].rolling(window=7).mean()
df["SMA2"] = df['Close'].rolling(window=14).mean()

plt.plot(df['SMA1'], 'g--', label="SMA1")
plt.plot(df['SMA2'], 'r--', label="SMA2")
plt.plot(df['Close'], label="Closing Prices")

prices = np.array(df["Close"])
backtestMax = prices * 0
for sim in range(100000):
    holding = 0
    money = 10
    df["Backtest"] = df['Close'] * 0
    out = [money]
    for i in range(len(prices)):
        volume = random.uniform(-holding,money/prices[i])
        holding += volume
        money -= volume * prices[i]
        out.append((money + (holding * prices[i])) / out[0])
    out = out[1:]
    df["Backtest"] = out
    if np.array(df["Backtest"])[-1] > backtestMax[-1]:
        backtestMax = df["Backtest"].copy()
    if sim % 50 == 0:
        plt.clf()
        plt.plot(df['Close'], label="Closing Prices")
        plt.plot(df["Backtest"], label="Current")
        print("sim",sim)
        plt.plot(backtestMax, label="Best")
        plt.legend()
        plt.pause(0.001)
plt.legend()
plt.show()