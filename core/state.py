import streamlit as st

def get_app_state():
    if "app_state" not in st.session_state:
        st.session_state.app_state = {
            "risk_mode": "Neutral",
            "last_summary": None
        }
    return st.session_state.app_state

