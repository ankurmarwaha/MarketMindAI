def generate_asset_summary(trend, volatility, drawdown):

    return (
        f"The asset is currently in a {trend.lower()} environment. "
        f"Volatility levels are {volatility}, while the maximum drawdown "
        f"suggests recent risk conditions remain controlled."
    )