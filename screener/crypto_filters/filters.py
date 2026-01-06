import numpy as np
import requests

KRAKEN_BASE_URL="https://api.kraken.com/0/public"

def price_above_sma(symbol, interval=60, periods=50):
    r = requests.get(f"{KRAKEN_BASE_URL}/OHLC", params={
        "pair": symbol,
        "interval": interval
    }).json()

    pair = list(r["result"].keys())[0]
    closes = [float(c[4]) for c in r["result"][pair][-periods:]]

    sma = float(np.mean(closes))
    current_price = float(closes[-1])

    return bool(current_price > sma)

def volume_spike(symbol, interval=60, periods=30, multiplier=1.5):
    r = requests.get(f"{KRAKEN_BASE_URL}/OHLC", params={
        "pair": symbol,
        "interval": interval
    }).json()

    pair = list(r["result"].keys())[0]
    volumes = [float(c[6]) for c in r["result"][pair][-periods:]]

    avg_volume = sum(volumes[:-1]) / (periods - 1)
    return volumes[-1] > avg_volume * multiplier


def volatility_expansion(symbol, interval=60, periods=20):
    r = requests.get(f"{KRAKEN_BASE_URL}/OHLC", params={
        "pair": symbol,
        "interval": interval
    }).json()

    pair = list(r["result"].keys())[0]
    candles = r["result"][pair][-periods:]

    ranges = [(float(c[2]) - float(c[3])) for c in candles]
    avg_range = sum(ranges[:-1]) / (periods - 1)

    return ranges[-1] > avg_range


def orderbook_imbalance(symbol, depth=25):
    r = requests.get(f"{KRAKEN_BASE_URL}/Depth", params={
        "pair": symbol,
        "count": depth
    }).json()

    pair = list(r["result"].keys())[0]
    bids = r["result"][pair]["bids"]
    asks = r["result"][pair]["asks"]

    bid_vol = sum(float(b[1]) for b in bids)
    ask_vol = sum(float(a[1]) for a in asks)

    return bid_vol > ask_vol


def tight_spread(symbol, max_spread_pct=0.1):
    r = requests.get(f"{KRAKEN_BASE_URL}/Ticker", params={
        "pair": symbol
    }).json()

    pair = list(r["result"].keys())[0]
    bid = float(r["result"][pair]["b"][0])
    ask = float(r["result"][pair]["a"][0])

    spread_pct = ((ask - bid) / ask) * 100
    return spread_pct < max_spread_pct
