import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
import numpy as np

def getStockData():
    ticker = yf.Ticker('TSLA')
    df = ticker.history(period="max")
    stockData = df['Close']
    return np.array(stockData)