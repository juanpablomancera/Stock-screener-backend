import pandas as pd
from yahoo_fin import stock_info as si


def get_other_stocks():
    otherStocks = pd.DataFrame(si.tickers_other())
    otherStocks = list(symbol for symbol in otherStocks[0].values.tolist())

    return otherStocks