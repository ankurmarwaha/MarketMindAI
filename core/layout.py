import streamlit as st

def app_header():
    st.markdown("## 📊 MarketMind AI")
    st.caption("Global market intelligence • Educational • Informational only")
    st.divider()

def section(title, subtitle=None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

def kpi(label, value):
    st.metric(label, value)
