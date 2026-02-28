import streamlit as st
from modules.global_pulse.data import get_global_market_snapshot


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


def render():
    st.markdown("### 🌍 Global Market Pulse")
    st.caption("A snapshot of global market performance")

    snapshot = get_global_market_snapshot()

    for region, assets in snapshot.items():
        st.markdown(f"#### {region}")

        cols = st.columns(len(assets))

        for col, (name, change) in zip(cols, assets.items()):
            with col:
                arrow_icon = arrow(change)
                colour = color(change)

                value = "N/A" if change is None else f"{change}%"

                st.markdown(
                    f"""
                    <div style="padding:12px; border-radius:8px; border:1px solid #eee">
                        <div style="font-size:14px; font-weight:600">{name}</div>
                        <div style="font-size:22px; color:{colour}">
                            {arrow_icon} {value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()

    st.caption(
        "This view provides high-level market context and should be used "
        "to understand overall market direction before analysing individual assets."
    )

