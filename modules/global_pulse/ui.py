import streamlit as st
import plotly.express as px
from modules.global_pulse.data import get_global_market_snapshot, get_index_history


def arrow(change):
    if change is None:
        return "—"
    if change > 0:
        return "↑"
    if change < 0:
        return "↓"
    return "→"


def color(change):
    if change is None:
        return "gray"
    if change > 0:
        return "green"
    if change < 0:
        return "red"
    return "orange"


def compute_market_mood(snapshot):
    positives = 0
    negatives = 0

    for _, assets in snapshot.items():
        for _, info in assets.items():
            change = info.get("change") if isinstance(info, dict) else info

            if change is None:
                continue
            if change > 0:
                positives += 1
            elif change < 0:
                negatives += 1

    if positives > negatives * 1.5:
        return "🟢 Risk-On / Bullish"
    elif negatives > positives * 1.5:
        return "🔴 Risk-Off / Defensive"
    else:
        return "🟡 Mixed / Neutral"


def generate_summary(mood):
    if "Risk-On" in mood:
        return "Markets are broadly positive, indicating risk appetite and supportive conditions for equities."
    if "Risk-Off" in mood:
        return "Markets are defensive today, suggesting caution, capital preservation, and elevated uncertainty."
    return "Markets are mixed, with no strong directional conviction across major regions."


@st.cache_data(ttl=900)
def cached_snapshot(timeframe):
    return get_global_market_snapshot(timeframe)


@st.cache_data(ttl=900)
def cached_history(ticker, period):
    return get_index_history(ticker, period=period)


def render():
    st.markdown("### 🌍 Global Market Pulse")
    st.caption("A snapshot of global market performance")

    # Timeframe selector
    timeframe = st.radio(
        "Timeframe",
        ["1D", "1W", "1M"],
        horizontal=True,
        index=0
    )

    period_map = {
        "1D": "5d",
        "1W": "1mo",
        "1M": "3mo",
    }

    snapshot = cached_snapshot(timeframe)

    # Market mood + summary
    mood = compute_market_mood(snapshot)
    summary = generate_summary(mood)

    st.markdown(
        f"""
        <div style="padding:12px; border-radius:8px; border:1px solid #ddd; margin-bottom:12px;">
            <strong>Market Mood:</strong> {mood}<br/>
            <span style="color:#555">{summary}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render regions
    for region, assets in snapshot.items():
        st.markdown(f"#### {region}")

        cols = st.columns(len(assets))

        for col, (name, info) in zip(cols, assets.items()):
            if isinstance(info, dict):
                change = info.get("change")
                ticker = info.get("ticker")
            else:
                change = info
                ticker = None

            with col:
                arrow_icon = arrow(change)
                colour = color(change)
                value = "N/A" if change is None else f"{change}%"

                st.markdown(
                    f"""
                    <div style="padding:12px; border-radius:8px; border:1px solid #eee; margin-bottom:8px;">
                        <div style="font-size:14px; font-weight:600">{name}</div>
                        <div style="font-size:22px; color:{colour}">
                            {arrow_icon} {value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Mini trend chart
                if ticker:
                    try:
                        hist = cached_history(ticker, period_map[timeframe])
                        if hist is not None and len(hist) > 0:
                            fig = px.line(
                                hist,
                                x="Date",
                                y="Close",
                                height=150,
                            )
                            fig.update_layout(
                                margin=dict(l=10, r=10, t=10, b=10),
                                xaxis_title=None,
                                yaxis_title=None,
                                showlegend=False,
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        st.caption("Trend unavailable")

        st.divider()

    st.caption(
        "This view provides high-level market context and should be used "
        "to understand overall market direction before analysing individual assets."
    )
