import streamlit as st
import pandas as pd

def streamlitUI(uploaded_file):
    st.set_page_config(
        page_title="GA4 Audit Agent",
        page_icon="📊",
        layout="wide"
    )

    st.sidebar.title("GA4 Audit Agent")

    st.sidebar.write(
        """
        ### Instructions

        1. Upload CSV or Excel
        2. Verify the data
        3. Click Start Audit
        """
    )

    st.title("📊 GA4 Audit Agent")

    uploaded_file = st.file_uploader(
        "Upload Website List",
        type=["csv", "xlsx"]
    )
    return uploaded_file
