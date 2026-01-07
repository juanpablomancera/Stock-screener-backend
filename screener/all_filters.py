from screener.get_tickers.sp500 import get_sp500

def filter_stocks(filters):
    filteredStocks = get_sp500()
    for filterFunction, value in filters.items():
        if value:
            filteredStocks = filterFunction(int(value), filteredStocks)
    return filteredStocks