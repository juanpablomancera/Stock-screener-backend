from screener.filters.all_time_high import all_time_high
from screener.filters.weeks_high import weeks_high
from screener.filters.weeks_min import weeks_min
from screener.filters.past_quarters_earnings_increase import past_quarters_earnings_increase
from screener.filters.past_quarters_earnings_surprise_average import past_four_quarters_earnings_surprise
from screener.filters.over_moving_average import over_moving_average
from screener.all_filters import filter_stocks
from screener.check_filters import check_filters

filters = {
    all_time_high: "",
    weeks_high: "",
    weeks_min: "",
    past_four_quarters_earnings_surprise: "",
    over_moving_average: "",
    past_quarters_earnings_increase: ""
}

def set_filters(data):
        filters[all_time_high] = data["allHigh"]
        filters[weeks_high] = data["weeksHigh"]
        filters[weeks_min] = data["weeksMin"]
        filters[past_four_quarters_earnings_surprise] = data["pastEarningsSurprise"]
        filters[over_moving_average] = data["movingAverage"]
        filters[past_quarters_earnings_increase] = data["pastEarningsIncrease"]


def results(data):
    set_filters(data)
    filter = check_filters(filters)
    results = filter_stocks(filter)
    return results


