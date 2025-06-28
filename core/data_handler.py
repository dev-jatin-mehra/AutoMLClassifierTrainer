import os
import pandas as pd
import streamlit as st

def handle_file_upload(uploaded_file):
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        if st.session_state.get("file_bytes") != file_bytes:
            st.session_state["file_bytes"] = file_bytes
            st.session_state["file_name"] = uploaded_file.name
            st.session_state["file_path"] = os.path.join("uploads", uploaded_file.name)
            with open(st.session_state["file_path"], "wb") as f:
                f.write(file_bytes)

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.astype(str).str.strip().str.replace(" ", "_").str.replace("[^a-zA-Z0-9_]", "", regex=True)
    return df

def validate_data(df):
    missing_report = df.isnull().sum()
    low_row_count = df.shape[0] < 100

    if low_row_count or any(missing_report > 0):
        st.subheader("Data Validation Report")
        if low_row_count:
            st.warning("Dataset has fewer than 100 rows. Results may be unreliable.")
        if any(missing_report > 0):
            st.warning("Missing values detected")
            st.dataframe(missing_report[missing_report > 0].to_frame("Missing_Count"))
            if st.checkbox("Drop rows with missing values?"):
                df.dropna(inplace=True)
                st.success("Rows with missing values dropped.")
                st.dataframe(df.head())
    return df
