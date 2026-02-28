import numpy as np


def generate_price_insights(df):
    insights = {}

    # Daily returns
    df["returns"] = df["Close"].pct_change()

    # Price change (2 years or full period)
    insights["price_change_pct"] = round(
        ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100, 2
    )

    # Volatility (20-day rolling)
    insights["volatility_20d"] = round(
        df["returns"].rolling(20).std().iloc[-1] * 100, 2
    )

    # Moving averages
    df["ma_50"] = df["Close"].rolling(50).mean()
    df["ma_200"] = df["Close"].rolling(200).mean()

    insights["above_50_ma"] = df["Close"].iloc[-1] > df["ma_50"].iloc[-1]
    insights["above_200_ma"] = df["Close"].iloc[-1] > df["ma_200"].iloc[-1]

    # Max drawdown
    cumulative_max = df["Close"].cummax()
    drawdown = (df["Close"] - cumulative_max) / cumulative_max
    insights["max_drawdown_pct"] = round(drawdown.min() * 100, 2)

    return insights

