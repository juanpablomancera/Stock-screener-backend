import pandas as pd
from yahoo_fin import stock_info as si


def get_dow():
    dow = pd.DataFrame( si.tickers_dow() )
    dow = list( symbol for symbol in dow[0].values.tolist() )

    return dow