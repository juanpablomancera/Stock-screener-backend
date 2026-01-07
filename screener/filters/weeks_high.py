import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


def weeks_high(distanceToHigh, allSymbols):
    yf.pdr_override()
    filteredSymbols = []
    start = dt.datetime.now() - dt.timedelta(weeks=52)
    now = dt.datetime.now()
    for symbol in allSymbols:
        try:
            df = pdr.get_data_yahoo(symbol, start, now)
            stockPrice = list(df["Adj Close"])[-1]
            high = df["High"].max()
            actualDistance = ((high - stockPrice) / stockPrice) * 100
            if actualDistance < distanceToHigh:
                filteredSymbols.append(symbol)

        except:
            print(f"Data from {symbol} not found")



    return filteredSymbols


