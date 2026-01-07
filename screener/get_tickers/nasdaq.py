import pandas as pd
from yahoo_fin import stock_info as si


def get_nasdaq():

    nasdaq = pd.DataFrame( si.tickers_nasdaq() )
    nasdaq = list( symbol for symbol in nasdaq[0].values.tolist() )

    return nasdaq

