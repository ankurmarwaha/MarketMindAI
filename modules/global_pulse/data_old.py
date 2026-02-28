import yfinance as yf

INDICES = {
    "US": {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
    },
    "Europe": {
        "FTSE 100": "^FTSE",
        "DAX": "^GDAXI",
    },
    "Asia": {
        "Nikkei 225": "^N225",
        "Hang Seng": "^HSI",
    },
    "Commodities": {
        "Gold": "GC=F",
        "Crude Oil": "CL=F",
    }
}


def fetch_index_change(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")

    if len(hist) < 2:
        return 0.0

    prev_close = hist["Close"].iloc[-2]
    last_close = hist["Close"].iloc[-1]

    return round(((last_close - prev_close) / prev_close) * 100, 2)


def get_global_market_snapshot():
    snapshot = {}

    for region, assets in INDICES.items():
        snapshot[region] = {}
        for name, symbol in assets.items():
            try:
                change = fetch_index_change(symbol)
                snapshot[region][name] = change
            except Exception:
                snapshot[region][name] = None

    return snapshot

def get_index_history(ticker: str, period: str) -> pd.DataFrame:
    """
    Return DataFrame with columns: Date, Close
    """
    ...

