import streamlit as st


def validate_dataframe(df):

    required_columns = [
        "site",
        "measurement_id"
    ]

    missing = []

    for column in required_columns:

        if column not in df.columns:
            missing.append(column)

    if missing:

        st.error(
            f"Missing Columns: {missing}"
        )

        st.stop()

    return True