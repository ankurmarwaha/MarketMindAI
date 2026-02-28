def classify_stock(insights, sentiment, asset_type="stock"):
    volatility = insights["volatility_20d"]
    drawdown = insights["max_drawdown_pct"]
    above_50 = insights["above_50_ma"]
    above_200 = insights["above_200_ma"]

    if asset_type == "precious_metal":
       if insights["above_200_ma"] and insights["volatility_20d"] <=3.5:
          return "HOLD"
       if insights["volatility"] > 5:
          return "WATCH"
       return "HOLD"

    sentiment_label = sentiment["sentiment_label"]

    # BUY conditions
    if (
        above_50 and
        above_200 and
        volatility <= 2.5 and
        drawdown >= -20 and
        sentiment_label != "Negative"
    ):
        return "BUY"

    # WATCH conditions
    if (
        not above_200 or
        volatility > 4 or
        drawdown < -30 or
        (sentiment_label == "Negative" and not above_50)
    ):
        return "WATCH"

    # Otherwise
    return "HOLD"

