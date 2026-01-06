from screener.get_tickers.getSP500 import getSP500

def filterStocks(filters):
    filteredStocks = getSP500()
    for filterFunction, value in filters.items():
        if value:
            filteredStocks = filterFunction(int(value), filteredStocks)
    return filteredStocks