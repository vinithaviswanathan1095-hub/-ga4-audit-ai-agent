import os
import streamlit as st
import pandas as pd

from validation import validate_dataframe
from audit import open_website
from ai_analyzer import analyze_all_results
from logger import write_log


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="GA4 Audit AI Agent",
    page_icon="📊",
    layout="wide"
)

# Create output folder
os.makedirs(
    "output",
    exist_ok=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("GA4 Audit AI Agent")

st.sidebar.markdown(
    """
### Instructions

1. Upload CSV or Excel
2. Validate the file
3. Click **Start Audit**
4. Review AI Report
5. Download Results
"""
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("📊 GA4 Audit AI Agent")

st.write(
    """
This application validates Google Analytics 4 Measurement IDs
across multiple websites and generates an AI-powered audit report.
"""
)

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Website List",
    type=["csv", "xlsx"]
)

# =====================================================
# PROCESS FILE
# =====================================================

if uploaded_file is not None:

    # ---------------------------------------------
    # Read File
    # ---------------------------------------------

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # ---------------------------------------------
    # Validate Input File
    # ---------------------------------------------

    validate_dataframe(df)

    st.success("✅ File Validation Successful")

    st.dataframe(df)

    # ---------------------------------------------
    # Display Metrics
    # ---------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Websites",
            len(df)
        )

    with col2:
        st.metric(
            "Measurement IDs",
            df["measurement_id"].count()
        )

    # ---------------------------------------------
    # Start Audit Button
    # ---------------------------------------------

    start = st.button("▶ Start Audit")

    if start:

        write_log("======================================")
        write_log("GA4 AUDIT STARTED")
        write_log("======================================")

        progress = st.progress(0)

        status = st.empty()

        results = []

        total_sites = len(df)

        # =========================================
        # Audit Each Website
        # =========================================

        for index, row in df.iterrows():

            site = row["site"]

            expected_measurement_id = row["measurement_id"]

            status.write(
                f"Auditing ({index + 1}/{total_sites}) : {site}"
            )

            write_log(
                f"Starting Audit : {site}"
            )

            result = open_website(
                site,
                expected_measurement_id
            )

            results.append(

                {
                    "site": site,

                    "expected_measurement_id": expected_measurement_id,

                    "found_measurement_id": result["found_measurement_id"],

                    "cookies_accepted": result["cookies_accepted"],

                    "status": result["status"],

                    "reason": result["reason"]

                }

            )

            progress.progress(
                (index + 1) / total_sites
            )

        # =========================================
        # Audit Complete
        # =========================================

        status.success("✅ Audit Completed")

        write_log("Audit Completed Successfully")

        # =========================================
        # Convert Results to DataFrame
        # =========================================

        results_df = pd.DataFrame(results)

        # =========================================
        # Save CSV
        # =========================================

        output_csv = "output/audit_results.csv"

        results_df.to_csv(
            output_csv,
            index=False
        )

        # =========================================
        # Generate AI Report (ONE API CALL)
        # =========================================

        write_log(
            "Sending audit results to AI..."
        )

        ai_report = analyze_all_results(
            results
        )

        write_log(
            "AI Report Generated Successfully"
        )

        # =========================================
        # Display Results
        # =========================================

        st.subheader("📋 Audit Results")

        st.dataframe(
            results_df,
            use_container_width=True
        )

        # =========================================
        # Display AI Report
        # =========================================

        st.subheader("🤖 AI Audit Report")

        st.markdown(ai_report)

        # =========================================
        # Download CSV
        # =========================================

        st.download_button(
            label="📥 Download Audit Results (CSV)",
            data=results_df.to_csv(index=False),
            file_name="audit_results.csv",
            mime="text/csv"
        )

        # =========================================
        # Download AI Report
        # =========================================

        st.download_button(
            label="📥 Download AI Report",
            data=ai_report,
            file_name="GA4_AI_Report.md",
            mime="text/markdown"
        )

        write_log("======================================")
        write_log("GA4 AUDIT FINISHED")
        write_log("======================================")