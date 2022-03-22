import yahoo_fin.stock_info as si

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
