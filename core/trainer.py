import os
import streamlit as st
from pycaret.classification import setup, compare_models, pull, save_model
from db.model_store import save_model_metadata
from components.sidebar import render_saved_models_sidebar

def train_model(df, target, quick_mode):
    st.session_state.training_in_progress = True
    try:
        st.info("Training in progress...")
        with st.spinner("Setting up environment..."):
            setup(data=df, target=target, fold=3 if quick_mode else 10, verbose=False)

        include = ['lr', 'rf', 'dt'] if quick_mode else None
        with st.spinner("Running AutoML..."):
            best_model = compare_models(include=include)

        if not st.session_state.training_in_progress:
            st.warning("Training stopped.")
            return

        result_df = pull()
        st.subheader("Model LeaderBoard")
        st.dataframe(result_df)

        model_filename = os.path.join("models", f"{st.session_state['file_name'].split('.')[0]}_model")
        save_model(best_model, model_filename)

        inserted = save_model_metadata(
            model_path=f"{model_filename}.pkl",
            filename=st.session_state["file_name"].split(".")[0],
            target=target,
            df_columns=df.columns.tolist(),
            quick_mode=quick_mode,
            metrics_dict=result_df.to_dict(),
            csv_path=st.session_state["file_path"]
        )

        if inserted:
            st.success("Model metadata saved to DB.")
            st.session_state.sidebar_refresh += 1
        else:
            st.warning("This model already exists.")

        with open(f"{model_filename}.pkl", "rb") as f:
            st.download_button(
                label="📦 Download Trained Model",
                data=f.read(),
                file_name=os.path.basename(f"{model_filename}.pkl"),
                mime="application/octet-stream"
            )

    except Exception as e:
        st.error(f"Training failed: {e}")
    finally:
        st.session_state.training_in_progress = False
