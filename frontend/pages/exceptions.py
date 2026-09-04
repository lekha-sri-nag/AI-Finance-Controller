import streamlit as st
import requests

st.set_page_config(
    page_title="Exceptions - AI Finance Controller",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Invoice Exceptions")
st.subheader("Detected Financial Control Exceptions")

API_URL = "http://127.0.0.1:8000"

invoice_id = st.session_state.get(
    "selected_invoice_id",
    "INV-TEST-001"
)

try:
    response = requests.get(
        f"{API_URL}/invoices/{invoice_id}/investigation",
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()

        invoice = data.get("invoice", {})
        exceptions = data.get("exceptions", [])

        st.success("Backend connected successfully")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Invoice ID",
                invoice.get("invoice_id", "Unknown")
            )

        with col2:
            st.metric(
                "Total Exceptions",
                len(exceptions)
            )

        with col3:
            high_risk_count = sum(
                1
                for exception in exceptions
                if exception.get("severity") in ["High", "Critical"]
            )
            st.metric(
                "High/Critical",
                high_risk_count
            )

        st.divider()

        if exceptions:
            for i, exception in enumerate(exceptions, start=1):

                exception_type = exception.get(
                    "exception_type",
                    "Unknown Exception"
                )

                severity = exception.get(
                    "severity",
                    "Unknown"
                )

                description = exception.get(
                    "description",
                    "No description available."
                )

                status = exception.get(
                    "status",
                    "Unknown"
                )

                with st.container(border=True):
                    st.subheader(
                        f"{i}. {exception_type}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Severity:** {severity}")
                        st.write(f"**Status:** {status}")

                    with col2:
                        st.write(
                            f"**Exception ID:** "
                            f"{exception.get('exception_id', 'Unknown')}"
                        )

                    st.write("**Description:**")
                    st.write(description)

        else:
            st.success("No exceptions detected for this invoice.")

    else:
        st.error(
            f"Backend returned status code: {response.status_code}"
        )

except requests.exceptions.RequestException as e:
    st.error("Could not connect to the backend.")
    st.write(str(e))
