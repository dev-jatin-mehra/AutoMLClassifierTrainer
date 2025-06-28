import os
import streamlit as st
from db.model_store import get_all_models

def render_saved_models_sidebar(refresh_count):
    with st.sidebar:
        st.header("Saved Models")
        saved_models = get_all_models()

        if not saved_models:
            st.info("No models saved.")
        else:
            for i, model in enumerate(saved_models):
                st.markdown(f"""
                **{model['filename']}**
                - Target: `{model['target']}`
                - Uploaded: `{model['uploaded_at'].strftime('%Y-%m-%d %H:%M:%S')}`
                - Mode: {"Quick" if model['quick_mode'] else "Full"}
                """)
                if os.path.exists(model["csv_path"]):
                    with open(model["csv_path"], "rb") as f:
                        st.download_button("Download CSV", f.read(), os.path.basename(model["csv_path"]), key=f"csv_{i}")
                st.markdown("---")

def render_target_sidebar(df):
    with st.sidebar:
        st.header("Target Selection")
        target = st.selectbox("Select the target column", df.columns.to_list())
        quick_mode = st.toggle("⚡Quick Mode", value=True)
        if st.button("rerun"):
            st.rerun()
    return target, quick_mode
