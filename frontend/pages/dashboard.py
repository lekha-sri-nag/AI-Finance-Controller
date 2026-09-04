import streamlit as st
import requests

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Finance Controller")
st.subheader("Financial Risk Dashboard")

API_URL = "http://localhost:8000"

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
        risk = data.get("risk_result", {})
        recommendation = data.get("recommendation", {})
        exceptions = data.get("exceptions", [])

        st.success("Backend connected successfully")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Invoice Amount",
                f"₹{invoice.get('amount', 0):,.0f}"
            )

        with col2:
            st.metric(
                "Risk Score",
                risk.get("risk_score", 0)
            )

        with col3:
            st.metric(
                "Risk Level",
                risk.get("risk_level", "Unknown")
            )

        with col4:
            st.metric(
                "Exceptions",
                len(exceptions)
            )

        st.divider()

        st.subheader("🚨 Risk Assessment")

        st.write(
            risk.get(
                "explanation",
                "No risk explanation available."
            )
        )

        st.subheader("📋 Recommended Action")

        st.warning(
            recommendation.get(
                "action",
                "No recommendation available."
            )
        )

        st.write(
            recommendation.get(
                "reason",
                "No reason available."
            )
        )

        st.subheader("⚠️ Detected Exceptions")

        if exceptions:
            for exception in exceptions:
                st.write(
                    f"**{exception.get('exception_type', 'Unknown')}** "
                    f"— {exception.get('severity', 'Unknown')}"
                )
                st.caption(
                    exception.get(
                        "description",
                        "No description available."
                    )
                )
        else:
            st.info("No exceptions detected.")

    else:
        st.error(
            f"Backend returned status code: {response.status_code}"
        )

except requests.exceptions.RequestException as e:
    st.error("Could not connect to the backend.")
    st.write(str(e))
