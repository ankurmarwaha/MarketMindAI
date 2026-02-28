import pandas as pd


def add_indicators(df: pd.DataFrame):

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    df["Returns"] = df["Close"].pct_change()
    df["Volatility"] = df["Returns"].rolling(20).std()

    df["Rolling_Max"] = df["Close"].cummax()
    df["Drawdown"] = (df["Close"] - df["Rolling_Max"]) / df["Rolling_Max"]

    return df


def classify_trend(df):
    if df is None or len(df) == 0:
        return "Unavailable"

    last = df.iloc[-1]

    if last["MA20"] > last["MA50"] > last["MA200"]:
        return "🟢 Strong Uptrend"
    elif last["MA20"] < last["MA50"] < last["MA200"]:
        return "🔴 Downtrend"
    else:
        return "🟡 Sideways"