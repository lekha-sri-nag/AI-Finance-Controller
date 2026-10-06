import streamlit as st
import requests

from frontend.config import API_URL

# =========================================================
# AUTHENTICATION
# =========================================================

access_token = st.session_state.get("access_token", "")

user_data = st.session_state.get("user") or {}

username = user_data.get(
    "username",
    st.session_state.get("username", "Unknown User")
)

user_role = user_data.get("role", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Finance Controller",
    layout="wide"
)

# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 750;
        color: #1e293b;
        margin-top: 1rem;
        margin-bottom: 0.9rem;
    }

    .invoice-context {
        padding: 1rem 1.3rem;
        border-radius: 14px;
        color: white;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.22);
        margin-bottom: 1.4rem;
    }

    .metric-card {
        padding: 1.2rem;
        border-radius: 16px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        min-height: 115px;
    }

    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        margin-top: 0.35rem;
    }

    .risk-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #fff7ed, #fff1f2);
        border-left: 6px solid #f97316;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
        color: #334155;
    }

    .recommendation-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #eff6ff, #eef2ff);
        border-left: 6px solid #4f46e5;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
        color: #334155;
    }

    .exception-card {
        padding: 1rem 1.2rem;
        border-radius: 13px;
        background: linear-gradient(135deg, #fff1f2, #fef2f2);
        border-left: 5px solid #ef4444;
        box-shadow: 0 5px 15px rgba(15, 23, 42, 0.06);
        margin-bottom: 0.8rem;
        color: #334155;
    }

    .report-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #ecfdf5, #eff6ff);
        border: 1px solid #bfdbfe;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
        color: #334155;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">AI Finance Controller</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Financial Risk Dashboard - AI-assisted financial control and investigation',
    unsafe_allow_html=True
)

# =========================================================
# INVOICE CONTEXT
# =========================================================

invoice_id = st.session_state.get(
    "selected_invoice_id",
    "INV-TEST-001"
)

if not invoice_id:
    invoice_id = "INV-TEST-001"

st.markdown(
    f"""
    <div class="invoice-context">
        <strong>Active Invoice</strong><br>
        {invoice_id}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# INVESTIGATION DATA
# =========================================================

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

        # =================================================
        # KPI CARDS
        # =================================================

        st.markdown(
            '<div class="section-title">Financial Risk Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Invoice Amount</div>
                    <div class="metric-value">
                        &#8377;{invoice.get('amount', 0):,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Risk Score</div>
                    <div class="metric-value">
                        {risk.get('risk_score', 0)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Risk Level</div>
                    <div class="metric-value">
                        {risk.get('risk_level', 'Unknown')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Exceptions</div>
                    <div class="metric-value">
                        {len(exceptions)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # =================================================
        # RISK ASSESSMENT
        # =================================================

        st.markdown(
            '<div class="section-title">Risk Assessment</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="risk-panel">
                {risk.get(
                    "explanation",
                    "No risk explanation available."
                )}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # RECOMMENDATION
        # =================================================

        st.markdown(
            '<div class="section-title">Recommended Action</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="recommendation-panel">
                <strong>
                    {recommendation.get(
                        "action",
                        "No recommendation available."
                    )}
                </strong>
                <br><br>
                {recommendation.get(
                    "reason",
                    "No reason available."
                )}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # DETECTED EXCEPTIONS
        # =================================================

        st.markdown(
            '<div class="section-title">Detected Exceptions</div>',
            unsafe_allow_html=True
        )

        if exceptions:

            for exception in exceptions:

                st.markdown(
                    f"""
                    <div class="exception-card">
                        <strong>
                            {exception.get(
                                "exception_type",
                                "Unknown"
                            )}
                        </strong>
                        <br>
                        Severity:
                        {exception.get(
                            "severity",
                            "Unknown"
                        )}
                        <br><br>
                        {exception.get(
                            "description",
                            "No description available."
                        )}
                    </div>
                    """,
                    unsafe_allow_html=True
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

# =========================================================
# FINANCIAL ANALYSIS REPORT
# =========================================================

if user_role in {"admin", "finance_controller"}:

    st.divider()

    st.markdown(
        '<div class="section-title">Financial Analysis Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="report-panel">
            Download the latest financial analysis generated by
            the AI Finance Controller.
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        report_response = requests.get(
            f"{API_URL}/decisions/report/excel",
            headers=AUTH_HEADERS,
            timeout=30
        )

        if report_response.status_code == 200:

            st.download_button(
                label="Download Excel Report",
                data=report_response.content,
                file_name="financial_analysis_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument"
                    ".spreadsheetml.sheet"
                )
            )

        elif report_response.status_code == 404:

            st.info(
                "No Excel report is available yet. "
                "Process at least one invoice to generate "
                "the financial analysis report."
            )

        elif report_response.status_code == 401:

            st.error(
                "Your session has expired. Please log in again."
            )

        else:

            st.error(
                f"Could not retrieve Excel report. "
                f"Backend returned {report_response.status_code}"
            )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Could not download Excel report: {e}"
        )
