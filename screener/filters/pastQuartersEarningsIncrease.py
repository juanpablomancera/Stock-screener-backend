import yahoo_fin.stock_info as si

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

