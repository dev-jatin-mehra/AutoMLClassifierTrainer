import streamlit as st

def initialize_session():
    if "training_in_progress" not in st.session_state:
        st.session_state.training_in_progress = False
    if "sidebar_refresh" not in st.session_state:
        st.session_state.sidebar_refresh = 0
