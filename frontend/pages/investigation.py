import streamlit as st
import requests

from frontend.config import API_URL

st.set_page_config(
    page_title="Investigation - AI Finance Controller",
    layout="wide"
)

# =========================================================
# PROFESSIONAL INVESTIGATION UI
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
        margin-bottom: 1.5rem;
    }

    .search-panel {
        padding: 1.3rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #eff6ff, #eef2ff);
        border: 1px solid #c7d2fe;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 750;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1.2rem;
    }

    .metric-card {
        padding: 1.2rem;
        border-radius: 15px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        min-height: 120px;
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

    .invoice-panel {
        padding: 1.2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #eff6ff, #f5f3ff);
        border-left: 6px solid #2563eb;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .risk-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #fff7ed, #fff1f2);
        border-left: 6px solid #f97316;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .exception-card {
        padding: 1rem 1.2rem;
        border-radius: 13px;
        background: linear-gradient(135deg, #fff1f2, #fef2f2);
        border-left: 5px solid #ef4444;
        box-shadow: 0 5px 15px rgba(15, 23, 42, 0.06);
        margin-bottom: 0.8rem;
    }

    .ai-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #f5f3ff, #eef2ff);
        border-left: 6px solid #7c3aed;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        margin-bottom: 1rem;
    }

    .root-cause {
        padding: 0.85rem 1rem;
        border-radius: 10px;
        background: #faf5ff;
        border: 1px solid #ddd6fe;
        margin-bottom: 0.6rem;
        color: #4c1d95;
    }

    .recommendation-panel {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #ecfdf5, #eff6ff);
        border-left: 6px solid #059669;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
        margin-bottom: 1rem;
    }

    .evidence-card {
        padding: 1rem 1.2rem;
        border-radius: 13px;
        background: linear-gradient(135deg, #f8fafc, #eff6ff);
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">Invoice Investigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-assisted financial investigation, root-cause analysis, evidence review, and risk assessment</div>',
    unsafe_allow_html=True
)

access_token = st.session_state.get("access_token", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

# =========================================================
# INVOICE SEARCH
# =========================================================

st.markdown(
    '<div class="section-title">Investigation Workspace</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="search-panel"><strong>Investigate a financial transaction</strong><br>Enter an invoice ID to retrieve its complete investigation and evidence chain.</div>',
    unsafe_allow_html=True
)

invoice_id = st.text_input(
    "Invoice ID",
    value=st.session_state.get(
        "selected_invoice_id",
        "INV-TEST-001"
    )
)

if st.button("Investigate Invoice", use_container_width=False):

    if not invoice_id:
        st.warning("Please enter an Invoice ID.")

    else:

        try:

            response = requests.get(
                f"{API_URL}/invoices/{invoice_id}/investigation",
                headers=AUTH_HEADERS,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    "Investigation data retrieved successfully."
                )

                invoice = data.get("invoice", {})
                risk = data.get("risk_result", {})
                exceptions = data.get("exceptions", [])
                investigation = data.get("investigation", {})
                recommendation = data.get("recommendation", {})
                evidence = data.get("evidence", [])

                # =================================================
                # INVOICE DETAILS
                # =================================================

                st.markdown(
                    '<div class="section-title">Invoice Details</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Invoice ID</div>
                            <div class="metric-value">
                                {invoice.get("invoice_id", "N/A")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Vendor</div>
                            <div class="metric-value">
                                {invoice.get("vendor_id", "N/A")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Amount</div>
                            <div class="metric-value">
                                &#8377;{invoice.get("amount", 0):,.0f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col4:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Quantity</div>
                            <div class="metric-value">
                                {invoice.get("quantity", 0)}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =================================================
                # RISK ASSESSMENT
                # =================================================

                st.markdown(
                    '<div class="section-title">Risk Assessment</div>',
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Risk Score</div>
                            <div class="metric-value">
                                {risk.get("risk_score", 0)}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Risk Level</div>
                            <div class="metric-value">
                                {risk.get("risk_level", "Unknown")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="risk-panel">
                        <strong>Risk Explanation</strong><br><br>
                        {risk.get("explanation", "No risk explanation available.")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =================================================
                # EXCEPTIONS
                # =================================================

                st.markdown(
                    '<div class="section-title">Detected Exceptions</div>',
                    unsafe_allow_html=True
                )

                if exceptions:

                    for exception in exceptions:

                        with st.expander(
                            f"{exception.get('severity', 'Unknown')} - "
                            f"{exception.get('exception_type', 'Unknown')}"
                        ):

                            st.markdown(
                                f"""
                                <div class="exception-card">
                                    <strong>Exception ID:</strong>
                                    {exception.get("exception_id", "N/A")}
                                    <br><br>
                                    <strong>Status:</strong>
                                    {exception.get("status", "N/A")}
                                    <br><br>
                                    <strong>Description:</strong>
                                    {exception.get("description", "N/A")}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:

                    st.success("No exceptions detected.")

                # =================================================
                # AI ROOT CAUSE INVESTIGATION
                # =================================================

                st.markdown(
                    '<div class="section-title">AI Root Cause Investigation</div>',
                    unsafe_allow_html=True
                )

                if investigation:

                    st.markdown(
                        f"""
                        <div class="ai-panel">
                            <strong>Investigation Status:</strong>
                            {investigation.get("investigation_status", "Unknown")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">Exceptions</div>
                                <div class="metric-value">
                                    {investigation.get("exceptions_count", 0)}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">High-Risk Exceptions</div>
                                <div class="metric-value">
                                    {investigation.get("high_risk_exceptions", 0)}
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
                                    {investigation.get("risk_level", "Unknown")}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        '<div class="section-title">Root Causes</div>',
                        unsafe_allow_html=True
                    )

                    root_causes = investigation.get(
                        "root_causes",
                        []
                    )

                    if root_causes:

                        for cause in root_causes:

                            st.markdown(
                                f"""
                                <div class="root-cause">
                                    - {cause}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.info("No root causes identified.")

                    st.markdown(
                        '<div class="section-title">Investigation Conclusion</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="ai-panel">
                            {investigation.get(
                                "conclusion",
                                "No conclusion available."
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
                        <strong>{recommendation.get(
                            "action",
                            "No recommendation available."
                        )}</strong>
                        <br><br>
                        <strong>Reason</strong><br>
                        {recommendation.get(
                            "reason",
                            "No reason available."
                        )}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if recommendation.get(
                    "requires_human_review",
                    False
                ):

                    st.warning(
                        "Human review is required."
                    )

                # =================================================
                # EVIDENCE
                # =================================================

                st.markdown(
                    '<div class="section-title">Evidence Chain</div>',
                    unsafe_allow_html=True
                )

                if evidence:

                    for item in evidence:

                        with st.expander(
                            item.get(
                                "source_type",
                                "Evidence"
                            )
                        ):

                            st.markdown(
                                f"""
                                <div class="evidence-card">
                                    <strong>Source Reference:</strong>
                                    {item.get("source_reference", "N/A")}
                                    <br><br>
                                    <strong>Description:</strong>
                                    {item.get("description", "N/A")}
                                    <br><br>
                                    <strong>Confidence:</strong>
                                    {item.get("confidence", "N/A")}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:

                    st.info("No evidence available.")

            else:

                st.error(
                    f"Investigation failed. "
                    f"Backend returned status "
                    f"{response.status_code}."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the backend. "
                "Please make sure the FastAPI server is running."
            )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Investigation request failed: {e}"
            )
