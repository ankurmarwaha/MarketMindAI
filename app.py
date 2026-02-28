import streamlit as st

from core.layout import app_header
from core.state import get_app_state


# ---------------------------------------------------------
# App Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 📊 MarketMind AI")
    st.caption("Global market intelligence")

    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "🌍 Global Market Pulse",
            "⚠️ Risk Indicator",
            "📊 Asset Intelligence",
            "🔥 Top Movers",
            "🧠 Market Themes",
            "📅 Global Events",
            "📝 Daily Summary",
        ],
    )

    st.divider()
    st.caption("Educational • Informational only")


# ---------------------------------------------------------
# Shared Header
# ---------------------------------------------------------
app_header()

# Shared application state
state = get_app_state()


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "🏠 Home":

    st.markdown("### 🌍 Today’s Market Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Global Markets", "Mixed")
    col2.metric("Risk Mode", "⚠️ Neutral")
    col3.metric("Volatility", "Moderate")

    st.divider()

    st.markdown("### 🔄 What Changed Since Yesterday")

    with st.container(border=True):
        st.write(
            "Global markets showed mixed performance as investors balanced "
            "economic data with central bank expectations. Defensive assets "
            "remained steady, suggesting a cautious but stable environment."
        )

    st.divider()

    st.markdown("### 🚀 Explore Market Intelligence")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("📊 **Asset Intelligence**")
        st.caption("Analyse stocks, precious metals, and ETFs")

    with c2:
        st.markdown("🔥 **Top Movers**")
        st.caption("See what moved global markets today and why")

    with c3:
        st.markdown("🧠 **Market Themes**")
        st.caption("Understand the narratives driving markets")

    st.divider()

    st.caption(
        "MarketMind AI helps you understand markets through context and explanation. "
        "This platform is educational and does not provide financial advice."
    )


# ---------------------------------------------------------
# GLOBAL MARKET PULSE (Placeholder)
# ---------------------------------------------------------
elif page == "🌍 Global Market Pulse":
    from modules.global_pulse.ui import render
    render()


    #st.markdown("### 🌍 Global Market Pulse")
    #st.info(
    #    "This module will provide a real-time snapshot of global markets "
   #    "across regions, asset classes, and major indices."
   # )


# ---------------------------------------------------------
# RISK INDICATOR (Placeholder)
# ---------------------------------------------------------
elif page == "⚠️ Risk Indicator":

    from modules.risk_indicator.ui import render
    render()



# ---------------------------------------------------------
# ASSET INTELLIGENCE (Placeholder)
# ---------------------------------------------------------
elif page == "📊 Asset Intelligence":

    from modules.asset_intelligence.ui import render
    render()


# ---------------------------------------------------------
# TOP MOVERS (Placeholder)
# ---------------------------------------------------------
elif page == "🔥 Top Movers":

    st.markdown("### 🔥 Top Movers")
    st.info(
        "This module will highlight top gainers and losers across global "
        "markets, along with explanations for the moves."
    )


# ---------------------------------------------------------
# MARKET THEMES (Placeholder)
# ---------------------------------------------------------
elif page == "🧠 Market Themes":

    st.markdown("### 🧠 Market Themes")
    st.info(
        "This module will identify key market narratives and trends shaping "
        "global asset performance."
    )


# ---------------------------------------------------------
# GLOBAL EVENTS (Placeholder)
# ---------------------------------------------------------
elif page == "📅 Global Events":

    st.markdown("### 📅 Global Events")
    st.info(
        "This module will track important upcoming macroeconomic and "
        "geopolitical events and explain why they matter."
    )


# ---------------------------------------------------------
# DAILY SUMMARY (Placeholder)
# ---------------------------------------------------------
elif page == "📝 Daily Summary":

    st.markdown("### 📝 Daily Market Summary")
    st.info(
        "This module will generate a concise AI-driven summary of the day’s "
        "market activity and key takeaways."
    )

