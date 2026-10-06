import streamlit as st
import requests

from frontend.config import API_URL

st.set_page_config(
    page_title="Exceptions - AI Finance Controller",
    layout="wide"
)

# =========================================================
# PROFESSIONAL EXCEPTIONS UI
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    .status-panel {
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
        border: 1px solid #bbf7d0;
        color: #166534;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 750;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1.2rem;
    }

    .metric-card {
        padding: 1.25rem;
        border-radius: 15px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        min-height: 115px;
    }

    .metric-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
    }

    .metric-value {
        font-size: 1.55rem;
        color: #1e293b;
        font-weight: 800;
        margin-top: 0.3rem;
    }

    .exception-card {
        padding: 1.35rem;
        border-radius: 16px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.2rem;
    }

    .exception-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #1e293b;
        margin-bottom: 1rem;
    }

    .exception-label {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .exception-value {
        font-size: 0.98rem;
        color: #1e293b;
        font-weight: 650;
        margin-top: 0.2rem;
    }

    .description-box {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Invoice Exceptions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Detected financial control exceptions requiring review and resolution.</div>',
    unsafe_allow_html=True
)

access_token = st.session_state.get("access_token", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

invoice_id = st.session_state.get(
    "selected_invoice_id",
    "INV-TEST-001"
)

try:
    response = requests.get(
        f"{API_URL}/invoices/{invoice_id}/investigation",
        headers=AUTH_HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()

        invoice = data.get("invoice", {})
        exceptions = data.get("exceptions", [])

        st.markdown(
            '<div class="status-panel">Backend connected successfully</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Invoice ID</div>
                    <div class="metric-value">{invoice.get("invoice_id", "Unknown")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Exceptions</div>
                    <div class="metric-value">{len(exceptions)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            high_risk_count = sum(
                1
                for exception in exceptions
                if exception.get("severity") in ["High", "Critical"]
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">High / Critical</div>
                    <div class="metric-value">{high_risk_count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="section-title">Exception Details</div>',
            unsafe_allow_html=True
        )

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

                exception_id = exception.get(
                    "exception_id",
                    "Unknown"
                )

                with st.container():
                    st.markdown(
                        f'<div class="exception-card">'
                        f'<div class="exception-title">{i}. {exception_type}</div>'
                        f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;">'
                        f'<div><div class="exception-label">Severity</div>'
                        f'<div class="exception-value">{severity}</div></div>'
                        f'<div><div class="exception-label">Status</div>'
                        f'<div class="exception-value">{status}</div></div>'
                        f'<div><div class="exception-label">Exception ID</div>'
                        f'<div class="exception-value">{exception_id}</div></div>'
                        f'</div>'
                        f'<div class="description-box">'
                        f'<div class="exception-label">Description</div>'
                        f'<div style="margin-top:0.35rem;">{description}</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        else:
            st.success("No exceptions detected for this invoice.")

    else:
        st.error(
            f"Backend returned status code: {response.status_code}"
        )

except requests.exceptions.RequestException as e:
    st.error("Could not connect to the backend.")
    st.write(str(e))
