import requests
import streamlit as st


st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)


st.title("💰 AI Finance Controller")
st.subheader("AI-powered financial control and invoice investigation system")

st.divider()


API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------
# BACKEND CONNECTION
# ---------------------------------------------------------

try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if response.status_code == 200:
        st.success("🟢 Backend API is connected")
    else:
        st.error("🔴 Backend API returned an error")

except requests.exceptions.RequestException:
    st.error("🔴 Backend API is not running")


st.divider()


# ---------------------------------------------------------
# INVOICE UPLOAD
# ---------------------------------------------------------

st.header("📤 Upload Invoice")


uploaded_file = st.file_uploader(
    "Upload an invoice file",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel (.xlsx) invoice file."
)


if uploaded_file is not None:

    if st.button("🚀 Upload & Validate Invoice"):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                f"{API_URL}/ingestion/invoices",
                files=files,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.success(result["message"])

                st.write(
                    f"**File:** {result['file_name']}  \n"
                    f"**Records validated:** {result['record_count']}"
                )

                st.subheader("Validated Invoices")

                st.dataframe(
                    result["invoices"],
                    use_container_width=True
                )

                st.session_state["validated_invoices"] = result["invoices"]

                st.session_state["uploaded_file_name"] = (
                    uploaded_file.name
                )

            else:

                error_detail = response.json().get(
                    "detail",
                    "Invoice upload failed."
                )

                st.error(
                    f"❌ {error_detail}"
                )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"❌ Could not connect to backend: {exc}"
            )


# ---------------------------------------------------------
# PROCESS INVOICE
# ---------------------------------------------------------

if "validated_invoices" in st.session_state:

    st.divider()

    st.header("🔍 Process Invoice")

    invoices = st.session_state["validated_invoices"]

    invoice_ids = [
        invoice["invoice_id"]
        for invoice in invoices
    ]

    selected_invoice = st.selectbox(
        "Select an invoice to process",
        invoice_ids
    )


    if st.button("⚙️ Run Finance Controller"):

        try:

            response = requests.post(
                f"{API_URL}/invoices/"
                f"{selected_invoice}/process-from-data",
                params={
                    "file_name": st.session_state[
                        "uploaded_file_name"
                    ]
                },
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.session_state["processed_result"] = result
                st.session_state["selected_invoice_id"] = selected_invoice

                st.success(
                    "✅ Invoice processed successfully."
                )

            else:

                error_detail = response.json().get(
                    "detail",
                    "Invoice processing failed."
                )

                st.error(
                    f"❌ {error_detail}"
                )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"❌ Could not connect to backend: {exc}"
            )


# ---------------------------------------------------------
# FINANCE CONTROLLER RESULT
# ---------------------------------------------------------

if "processed_result" in st.session_state:

    result = st.session_state["processed_result"]

    invoice = result["invoice"]
    exceptions = result["exceptions"]
    risk = result["risk_result"]
    recommendation = result["recommendation"]


    st.divider()

    st.header("📊 Finance Controller Result")


    # -----------------------------------------------------
    # INVOICE INFORMATION
    # -----------------------------------------------------

    st.subheader("🧾 Invoice Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Invoice",
            invoice["invoice_id"]
        )

    with col2:
        st.metric(
            "Vendor",
            invoice["vendor_id"]
        )

    with col3:
        st.metric(
            "Amount",
            f"₹{invoice['amount']:,.2f}"
        )

    with col4:
        st.metric(
            "Quantity",
            invoice["quantity"]
        )


    # -----------------------------------------------------
    # RISK ASSESSMENT
    # -----------------------------------------------------

    st.subheader("⚠️ Risk Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Risk Score",
            risk["risk_score"]
        )

    with col2:

        if risk["risk_level"] == "Critical":

            st.error(
                f"🔴 {risk['risk_level']} Risk"
            )

        elif risk["risk_level"] == "High":

            st.warning(
                f"🟠 {risk['risk_level']} Risk"
            )

        else:

            st.info(
                f"🟢 {risk['risk_level']} Risk"
            )

    st.write(
        f"**Explanation:** {risk['explanation']}"
    )


    # -----------------------------------------------------
    # EXCEPTIONS
    # -----------------------------------------------------

    st.subheader("🚨 Detected Exceptions")

    if exceptions:

        for exception in exceptions:

            st.warning(
                f"⚠️ **{exception['exception_type']}**  \n"
                f"{exception['description']}"
            )

    else:

        st.success(
            "✅ No financial control exceptions detected."
        )


    # -----------------------------------------------------
    # AI RECOMMENDATION
    # -----------------------------------------------------

    st.subheader("🤖 AI Recommendation")

    if recommendation["action"] == "Block Payment":

        st.error(
            f"""
### 🔴 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}

**Human Review:** Required
"""
        )

    elif recommendation["action"] == "Hold Payment":

        st.warning(
            f"""
### 🟠 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}
"""
        )

    else:

        st.success(
            f"""
### 🟢 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}
"""
        )


    # -----------------------------------------------------
    # RISK FACTORS
    # -----------------------------------------------------

    st.subheader("📌 Risk Factors")

    for factor in risk["risk_factors"]:

        st.write(
            f"• {factor}"
        )


    st.divider()

    st.info(
        "Human review is required before the final financial "
        "decision is made."
    )
