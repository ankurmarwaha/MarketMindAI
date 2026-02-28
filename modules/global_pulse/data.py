import yfinance as yf
import pandas as pd
import streamlit as st

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

# Map UI timeframe -> yfinance period
PERIOD_MAP = {
    "1D": "2d",   # need at least 2 days to compute change
    "1W": "7d",
    "1M": "1mo",
}


@st.cache_data(ttl=900)
def fetch_history(symbol: str, period: str) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    hist = hist.reset_index()
    return hist


def compute_change_from_history(hist: pd.DataFrame) -> float | None:
    if hist is None or len(hist) < 2:
        return None

    prev_close = hist["Close"].iloc[-2]
    last_close = hist["Close"].iloc[-1]

    if prev_close == 0 or pd.isna(prev_close) or pd.isna(last_close):
        return None

    return round(((last_close - prev_close) / prev_close) * 100, 2)


def get_global_market_snapshot(timeframe: str = "1D"):
    """
    Returns:
    {
        "US": {
            "S&P 500": {"ticker": "^GSPC", "change": 0.6},
            ...
        },
        ...
    }
    """
    snapshot = {}
    period = PERIOD_MAP.get(timeframe, "2d")

    for region, assets in INDICES.items():
        snapshot[region] = {}
        for name, symbol in assets.items():
            try:
                hist = fetch_history(symbol, period)
                change = compute_change_from_history(hist)
                snapshot[region][name] = {
                    "ticker": symbol,
                    "change": change
                }
            except Exception:
                snapshot[region][name] = {
                    "ticker": symbol,
                    "change": None
                }

    return snapshot


@st.cache_data(ttl=900)
def get_index_history(ticker: str, period: str) -> pd.DataFrame:
    """
    Return DataFrame with columns: Date, Close
    """
    hist = fetch_history(ticker, period)

    if hist is None or len(hist) == 0:
        return pd.DataFrame(columns=["Date", "Close"])

    # Keep only what UI needs
    df = hist[["Date", "Close"]].copy()
    return df
