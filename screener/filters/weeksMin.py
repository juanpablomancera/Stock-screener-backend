import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

def weeksMin(distanceToMin, allSymbols):
    yf.pdr_override()
    filteredSymbols = []
    start = dt.datetime.now() - dt.timedelta(weeks=52)
    now = dt.datetime.now()
    for symbol in allSymbols:
        try:
            df = pdr.get_data_yahoo(symbol, start, now)
            stockPrice = list(df["Adj Close"])[-1]
            low = df["Low"].min()
            actualDistance = ((stockPrice - low) / low) * 100
            if actualDistance > distanceToMin:
                filteredSymbols.append(symbol)

        except:
            print(f"Data from {symbol} not found")



    return filteredSymbols


