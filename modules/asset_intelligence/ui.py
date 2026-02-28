import streamlit as st
import plotly.express as px

from modules.asset_intelligence.data import fetch_asset_history
from modules.asset_intelligence.indicators import add_indicators, classify_trend
from modules.asset_intelligence.narrative import generate_asset_summary


def render():

    st.markdown("### 📊 Asset Intelligence")
    st.caption("Deep analysis of individual assets")

    from modules.asset_intelligence.data import (
        fetch_asset_history,
        search_suggestions
    )

    # --- Search box ---
    query = st.text_input("Search Company", "Apple")

    selected_symbol = None
    selected_name = None

    if query:
        suggestions = search_suggestions(query)

        if suggestions:
            option_labels = [s["label"] for s in suggestions]

            selected = st.selectbox(
                "Select Company",
                option_labels
            )

            chosen = next(
                s for s in suggestions if s["label"] == selected
            )

            selected_symbol = chosen["symbol"]
            selected_name = chosen["name"]

    if not selected_symbol:
        return

    if selected_symbol:
        df, symbol, company_name = fetch_asset_history(selected_symbol)
    else:
        return

    if df is None or df.empty:
        st.error("No market data found. Try another company or ticker.")
        return
    df = add_indicators(df)

    trend = classify_trend(df)

    volatility = "High" if df["Volatility"].iloc[-1] > 0.02 else "Moderate"
    drawdown = round(df["Drawdown"].iloc[-1] * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Trend", trend)
    col2.metric("Volatility", volatility)
    col3.metric("Drawdown", f"{drawdown}%")

    fig = px.line(
        df,
        x="Date",
        y=["Close", "MA20", "MA50"],
        title=f"{company_name} ({symbol}) Price Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    summary = generate_asset_summary(trend, volatility, drawdown)

    st.info(summary)