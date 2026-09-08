import streamlit as st
import requests
# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

access_token = st.session_state.get(
    "access_token",
    ""
)

user_data = st.session_state.get("user") or {}

username = user_data.get(
    "username",
    st.session_state.get("username", "Unknown User")
)
username = user_data.get(
    "username",
    st.session_state.get(
        "username",
        "Unknown User"
    )
)

user_role = user_data.get(
    "role",
    ""
)

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Finance Controller")
st.subheader("Financial Risk Dashboard")

API_URL = "http://localhost:8000"
access_token = st.session_state.get("access_token", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

invoice_id = st.session_state.get(
    "selected_invoice_id",
    "INV-TEST-001"
)

if not invoice_id:
    invoice_id = "INV-TEST-001"
st.info(f"Dashboard is requesting invoice: {invoice_id}")
try:
    response = requests.get(
        f"{API_URL}/invoices/{invoice_id}/investigation",
        headers=AUTH_HEADERS,
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
# --------------------------------------------------
# EXCEL REPORT DOWNLOAD
# --------------------------------------------------

if user_role in {"admin", "finance_controller"}:

    st.divider()

    st.subheader("📊 Financial Analysis Report")

    report_path = (
        "data/reports/financial_analysis_report.xlsx"
    )

    try:

        with open(report_path, "rb") as report_file:

            report_data = report_file.read()

        st.download_button(
            label="📥 Download Excel Report",
            data=report_data,
            file_name="financial_analysis_report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

    except FileNotFoundError:

        st.info(
            "📄 No Excel report is available yet. "
            "Process at least one invoice to generate "
            "the financial analysis report."
        )