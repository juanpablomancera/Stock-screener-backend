from screener.gettickers.getSP500 import getSP500

def filterStocks(filters):
    filteredStocks = getSP500()[:30]
    for filterFunction, value in filters.items():
        if value:
            filteredStocks = filterFunction(int(value), filteredStocks)
    return filteredStocks