import yfinance as yf

def fetch_price_data(ticker, period="2y"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)

    if df.empty:
        raise ValueError("No data found for this ticker")

    return df

