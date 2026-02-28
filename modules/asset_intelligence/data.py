import yfinance as yf
import pandas as pd
import streamlit as st
import requests


def search_ticker(query: str):
    """
    Resolve company name → ticker using Yahoo Finance search API.
    """

    url = "https://query2.finance.yahoo.com/v1/finance/search"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "q": query,
        "quotesCount": 5,
        "newsCount": 0,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()

        quotes = data.get("quotes", [])

        for q in quotes:
            # Prefer equities
            if q.get("quoteType") == "EQUITY":
                symbol = q.get("symbol")
                name = q.get("shortname") or q.get("longname")
                return symbol, name

        # fallback: first result
        if quotes:
            q = quotes[0]
            return q.get("symbol"), q.get("shortname")

    except Exception:
        pass

    return None, None


@st.cache_data(ttl=900)
def fetch_asset_history(query: str, period: str = "1y"):

    symbol, company_name = search_ticker(query)

    if symbol is None:
        return None, None, None

    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)

    if data is None or len(data) == 0:
        return None, None, None

    data = data.reset_index()

    return data, symbol, company_name

import requests


def search_suggestions(query: str):
    """
    Return list of company suggestions from Yahoo Finance.
    """

    if len(query) < 2:
        return []

    url = "https://query2.finance.yahoo.com/v1/finance/search"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "q": query,
        "quotesCount": 8,
        "newsCount": 0,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()

        suggestions = []

        for q in data.get("quotes", []):
            if q.get("quoteType") == "EQUITY":
                symbol = q.get("symbol")
                name = q.get("shortname") or q.get("longname")

                if symbol and name:
                    suggestions.append({
                        "label": f"{name} ({symbol})",
                        "symbol": symbol,
                        "name": name
                    })

        return suggestions

    except Exception:
        return []