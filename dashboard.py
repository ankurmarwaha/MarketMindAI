import streamlit as st
import matplotlib.pyplot as plt

from data.price_fetcher import fetch_price_data
from analysis.price_insights import generate_price_insights
from analysis.classification import classify_stock
from data.news_fetcher import fetch_stock_news
from analysis.sentiment import analyse_sentiment
from ai.reasoning import generate_ai_explanation
from config.assets import ASSETS

st.set_page_config(page_title="MarketMind AI", layout="wide")

st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("## 📊 MarketMind AI")
st.caption("Explainable market intelligence • Informational only")
st.divider()


#st.title("📊 MarketMind AI — Stock Intelligence Dashboard")
#st.caption("Explainable, AI-powered market insights (Informational only)")

# Sidebar
#ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
#run = st.sidebar.button("Analyse Stock")

#asset_type = st.sidebar.selectbox("Asset Type",["Equity","Precious Metal","ETF"])

with st.sidebar:
    st.markdown("### Asset Selection")
#st.sidebar.header("Asset Selection")

asset_type = st.sidebar.selectbox(
    "Select Asset Type",
    list(ASSETS.keys())
)

asset_name = st.sidebar.selectbox(
    "Select Asset",
    list(ASSETS[asset_type].keys())
)

ticker = ASSETS[asset_type][asset_name]

run = st.button("Analyse Asset", use_container_width=True)
#run = st.sidebar.button("Analyse Asset")

normalized_asset_type = asset_type.lower().replace(" ", "_")

if run:
    with st.spinner("Fetching market data..."):
        price_df = fetch_price_data(ticker)
        insights = generate_price_insights(price_df)

        news = fetch_stock_news(ticker)
        sentiment = analyse_sentiment(news)

        classification = classify_stock(insights, sentiment,asset_type=normalized_asset_type)

        explanation = generate_ai_explanation(
            ticker, insights, sentiment, classification
        )

    # === TOP METRICS ===
    col1, col2, col3, col4 = st.columns(4)


    col1.metric("2Y Performance", f"{insights['price_change_pct']}%")
    col2.metric("Volatility (20D)", f"{insights['volatility_20d']}%")
    col3.metric("Max Drawdown", f"{insights['max_drawdown_pct']}%")
    #col4.metric("Signal", classification)

    #col1.metric("Price Change (2Y)", f"{insights['price_change_pct']}%")
    #col2.metric("20-Day Volatility", f"{insights['volatility_20d']}%")
    #col3.metric("Max Drawdown", f"{insights['max_drawdown_pct']}%")
    #col4.metric("Signal", classification)

    # === PRICE CHART ===
    
    def signal_badge(signal):
        colors = {
            "BUY": "green",
            "HOLD": "orange",
            "WATCH": "red"
        }

        return f"<span style='color:{colors[signal]}; font-weight:700'>{signal}</span>"

    
    st.markdown(
        f"### Signal: {signal_badge(classification)}",
        unsafe_allow_html=True
    )

    st.subheader("📈 Price Trend")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(price_df.index, price_df["Close"], label="Price", linewidth=2)
    ax.plot(price_df.index, price_df["Close"].rolling(50).mean(), label="MA 50", linestyle="--")
    ax.plot(price_df.index, price_df["Close"].rolling(200).mean(), label="MA 200", linestyle="--")


    ax.set_title("Price Trend")
    ax.set_ylabel("Price")
    ax.grid(alpha=0.3)
    ax.legend()

    st.pyplot(fig)

    # === SENTIMENT ===
    st.subheader("📰 News Sentiment")

    st.write(f"**Overall Sentiment:** {sentiment['sentiment_label']}")
    st.write(f"**Average Sentiment Score:** {sentiment['average_sentiment']}")

    # === AI EXPLANATION ===

    with st.container(border=True):
        st.markdown("### 🧠 AI Insight")
        st.write(explanation)
    #st.subheader("🧠 AI Explanation")

    #st.write(explanation)

    st.caption(
        "Disclaimer: This dashboard provides informational analysis only and does not constitute financial advice."
    )

