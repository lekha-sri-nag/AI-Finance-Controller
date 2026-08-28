import streamlit as st
import requests

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Finance Controller")
st.subheader("AI-powered financial control and invoice investigation system")

st.divider()

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Check backend status
try:
    response = requests.get(f"{API_URL}/health", timeout=5)

    if response.status_code == 200:
        st.success("🟢 Backend API is connected")
    else:
        st.error("🔴 Backend API returned an error")

except requests.exceptions.RequestException:
    st.error("🔴 Backend API is not running")

st.divider()

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Invoices", "1")

with col2:
    st.metric("Exceptions", "5")

with col3:
    st.metric("Critical Risk", "1")

with col4:
    st.metric("Human Review", "Required")

st.divider()

st.header("Invoice Risk Overview")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
        **Invoice:** INV-013

        **Vendor:** XYZ Traders

        **Amount:** ₹75,000

        **Purchase Order:** ₹50,000

        **Invoice Quantity:** 100

        **Received Quantity:** 80
        """
    )

with col2:
    st.error(
        """
        ### 🔴 Critical Risk

        **Risk Score:** 100

        **Risk Level:** Critical

        **Recommended Action:** Block Payment

        **Human Review:** Required
        """
    )

st.divider()

st.header("Detected Exceptions")

exceptions = [
    "Amount Mismatch",
    "Missing Approval",
    "Quantity Mismatch",
    "Policy Violation",
    "Vendor Anomaly"
]

for exception in exceptions:
    st.warning(f"⚠️ {exception}")

st.divider()

st.header("Recommendation")

st.write(
    "The system recommends blocking payment because multiple "
    "financial control violations were detected."
)

if st.button("🔍 View Investigation"):
    st.info(
        "Investigation view will be connected to the backend in the next step."
    )