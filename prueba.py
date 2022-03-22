import pandas as pd
import datetime as dt
import yahoo_fin.stock_info as si
import yfinance as yf
from pandas_datareader import data as pdr

def getSP500():
    payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]
    df = first_table
    df.head()
    symbols = df['Symbol'].values.tolist()
    return symbols

def allTimeHigh(distanceToHigh, allSymbols):
    yf.pdr_override()
    filteredSymbols = []
    start = dt.datetime.now() - dt.timedelta(weeks=2000)
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


def pastQuartersEarningsIncrease(rate, allSymbols):
    filteredSymbols = []

    for symbol in allSymbols:
        pastEarnings = []
        try:
            earnings = si.get_earnings_history(symbol)
            for earning in earnings:
                actualEarning = earning["epsactual"]
                if actualEarning:
                    pastEarnings.append(actualEarning)
            firstQuarter = ((pastEarnings[3] - pastEarnings[4]) / pastEarnings[4]) * 100
            secondQuarter = ((pastEarnings[2] - pastEarnings[3]) / pastEarnings[3]) * 100
            thirdQuarter = ((pastEarnings[1] - pastEarnings[2]) / pastEarnings[2]) * 100
            fourthQuarter = ((pastEarnings[0] - pastEarnings[1]) / pastEarnings[1]) * 100
            averageRate = (firstQuarter + secondQuarter + thirdQuarter + fourthQuarter)/4
            if averageRate > rate:
                filteredSymbols.append(symbol)

        except:
            print(f"Data from {symbol} not found")

    return filteredSymbols

def pastFourQuartersEarningsSurprise(surpriseRate, allSymbols):
    filteredSymbols = []

    for symbol in allSymbols:
        pastSurpriseRate = []
        try:
            earnings = si.get_earnings_history(symbol)
            for earning in earnings:
                if earning['epssurprisepct']:
                    pastSurpriseRate.append(earning['epssurprisepct'])
            currentRate = (pastSurpriseRate[0] + pastSurpriseRate[1] + pastSurpriseRate[2] + pastSurpriseRate[3]) / 4
            if currentRate > surpriseRate:
                filteredSymbols.append(symbol)
        except:
            print(f"Data from {symbol} not found")
    return filteredSymbols


def weeksHigh(distanceToHigh, allSymbols):
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


filters = {
    allTimeHigh: "",
    weeksHigh: "",
    weeksMin: "",
    pastFourQuartersEarningsSurprise: "",
    overMovingAverage: "",
    pastQuartersEarningsIncrease: ""
}

def checkFilters(filters):
    newFilters = {}
    for function, value in filters.items():
        if value:
            newFilters[function] = value
    return newFilters

def filterStocks(filters):
    filteredStocks = getSP500()[:30]
    for filterFunction, value in filters.items():
        if value:
            filteredStocks = filterFunction(int(value), filteredStocks)
    return filteredStocks

def setFilters(data):
        filters[allTimeHigh] = data["allHigh"]
        filters[weeksHigh] = data["weeksHigh"]
        filters[weeksMin] = data["weeksMin"]
        filters[pastFourQuartersEarningsSurprise] = data["pastEarningsSurprise"]
        filters[overMovingAverage] = data["movingAverage"]
        filters[pastQuartersEarningsIncrease] = data["pastEarningsIncrease"]


def results(data):
    setFilters(data)
    filter = checkFilters(filters)
    results = filterStocks(filter)
    return results