import streamlit as st
import plotly.express as px
from modules.risk_indicator.data import get_risk_signals, get_signal_history
from modules.risk_indicator.logic import compute_risk_regime, explain_regime


def render():
    st.markdown("### ⚠️ Risk-On / Risk-Off Indicator")
    st.caption("Market regime based on cross-asset risk signals")

    # Timeframe selector
    timeframe = st.radio(
        "Timeframe",
        ["1D", "1W", "1M"],
        horizontal=True,
        index=0
    )

    signals = get_risk_signals(timeframe)
    regime, total_score, scores = compute_risk_regime(signals)
    explanation = explain_regime(regime, scores)

    # Header card
    st.markdown(
        f"""
        <div style="padding:16px; border-radius:10px; border:1px solid #ddd; margin-bottom:12px;">
            <div style="font-size:22px; font-weight:700;">{regime}</div>
            <div style="color:#555">Risk Score: {total_score}</div>
            <div style="margin-top:8px;">{explanation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Signal Breakdown")

    for name, change in signals.items():
        score = scores.get(name, 0)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"**{name}**")
            st.metric("Change (%)", "N/A" if change is None else change)
            st.write(f"Signal Score: **{score}**")

        with col2:
            hist = get_signal_history(name, timeframe=timeframe)
            if hist is not None and len(hist) > 0:
                fig = px.line(hist, x="Date", y="Close", height=180)
                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis_title=None,
                    yaxis_title=None,
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("Trend unavailable")

        st.divider()

    st.caption(
        "The timeframe changes both the signal calculation and the trend context. "
        "Short-term (1D) reflects immediate sentiment, while 1W and 1M show broader regime shifts."
    )
