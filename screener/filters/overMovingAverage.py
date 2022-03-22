import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

def overMovingAverage(smaValue, allSymbols):
    yf.pdr_override()
    filteredSymbols = []
    smaString = "Sma_"+str(smaValue)
    start = dt.datetime.now() - dt.timedelta(days=300)
    now = dt.datetime.now()
    for symbol in allSymbols:
        try:
            df = pdr.get_data_yahoo(symbol,start,now)
            df[smaString] = df.iloc[:,4].rolling(window=smaValue).mean()
            sma = list(df[smaString])[-1]
            stockPrice = list(df["Adj Close"])[-1]
            if stockPrice > sma:
                filteredSymbols.append(symbol)
        except:
            print(f"Data from {symbol} not found")

    return filteredSymbols

