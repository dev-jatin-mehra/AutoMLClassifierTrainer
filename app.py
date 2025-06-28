import os
import streamlit as st
from core.trainer import train_model
from core.data_handler import handle_file_upload, load_data, validate_data
from core.session_manager import initialize_session
from components.sidebar import render_saved_models_sidebar, render_target_sidebar

os.makedirs("uploads", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Setup
st.set_page_config(page_title="AutoML CSV Classifier", layout="wide")
st.title("AutoML CSV Classifier Trainer")
initialize_session()

# Sidebar
render_saved_models_sidebar(st.session_state.sidebar_refresh)

# Upload
uploaded_file = st.file_uploader("Upload your cleaned CSV file", type=["csv"])
handle_file_upload(uploaded_file)

# Load + show data
if "file_path" in st.session_state:
    df = load_data(st.session_state["file_path"])
    st.success(f"File '{st.session_state['file_name']}' loaded successfully!")
    st.dataframe(df.head())

    df = validate_data(df)

    # Target selection in sidebar
    target, quick_mode = render_target_sidebar(df)

    # Train + Stop buttons
    col1, col2 = st.columns(2)
    train_clicked = col1.button("Train Model")
    stop_clicked = col2.button("Stop Training")

    if stop_clicked:
        st.session_state.training_in_progress = False
        st.warning("Training has been manually stopped.")

    # Train
    if train_clicked:
        train_model(df, target, quick_mode)
