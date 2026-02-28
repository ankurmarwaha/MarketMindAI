import yfinance as yf
import pandas as pd
import streamlit as st

SIGNALS = {
    "S&P 500": "^GSPC",
    "VIX": "^VIX",
    "Gold": "GC=F",
    "USD Index": "DX-Y.NYB",
    "US 10Y Treasury": "^TNX",
}

TIMEFRAME_MAP = {
    "1D": {"hist": "5d", "change": "5d"},
    "1W": {"hist": "1mo", "change": "1mo"},
    "1M": {"hist": "3mo", "change": "3mo"},
}


@st.cache_data(ttl=900)
def fetch_history(symbol: str, period: str = "3mo") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    hist = hist.reset_index()
    return hist

def get_latest_change(symbol: str, period: str = "5d") -> float | None:
    try:
        hist = fetch_history(symbol, period)
        if hist is None or len(hist) < 2:
            return None
        prev_close = hist["Close"].iloc[-2]
        last_close = hist["Close"].iloc[-1]
        if prev_close == 0 or pd.isna(prev_close) or pd.isna(last_close):
            return None
        return round(((last_close - prev_close) / prev_close) * 100, 2)
    except Exception:
        return None

def get_risk_signals(timeframe: str = "1D"):
    data = {}
    tf = TIMEFRAME_MAP.get(timeframe, TIMEFRAME_MAP["1D"])

    for name, symbol in SIGNALS.items():
        try:
            hist = fetch_history(symbol, tf["change"])
            change = compute_change_from_history(hist)
            data[name] = change
        except Exception:
            data[name] = None

    return data


@st.cache_data(ttl=900)
def get_signal_history(name: str, timeframe: str = "1D") -> pd.DataFrame:
    symbol = SIGNALS.get(name)
    if not symbol:
        return pd.DataFrame(columns=["Date", "Close"])

    tf = TIMEFRAME_MAP.get(timeframe, TIMEFRAME_MAP["1D"])
    hist = fetch_history(symbol, tf["hist"])

    if hist is None or len(hist) == 0:
        return pd.DataFrame(columns=["Date", "Close"])

    return hist[["Date", "Close"]].copy()

def compute_change_from_history(hist: pd.DataFrame) -> float | None:
    if hist is None or len(hist) < 2:
        return None

    first_close = hist["Close"].iloc[0]
    last_close = hist["Close"].iloc[-1]

    if first_close == 0 or pd.isna(first_close) or pd.isna(last_close):
        return None

    return round(((last_close - first_close) / first_close) * 100, 2)
