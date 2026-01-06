from screener.filters.allTimeHigh import allTimeHigh
from screener.filters.weeksHigh import weeksHigh
from screener.filters.weeksMin import weeksMin
from screener.filters.pastQuartersEarningsIncrease import pastQuartersEarningsIncrease
from screener.filters.pastQuartersEarningsSurpriseAverage import pastFourQuartersEarningsSurprise
from screener.filters.overMovingAverage import overMovingAverage
from screener.AllFilters import filterStocks
from screener.CheckFilters import checkFilters

filters = {
    allTimeHigh: "",
    weeksHigh: "",
    weeksMin: "",
    pastFourQuartersEarningsSurprise: "",
    overMovingAverage: "",
    pastQuartersEarningsIncrease: ""
}

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


