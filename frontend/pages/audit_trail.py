import streamlit as st
import requests

from frontend.config import API_URL

st.set_page_config(
    page_title="Audit Trail - AI Finance Controller",
    layout="wide"
)

# =========================================================
# PROFESSIONAL AUDIT TRAIL UI
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.65rem;
        font-weight: 850;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }

    .subtitle {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .search-panel {
        padding: 1.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 55%, #fdf2f8 100%);
        border: 1px solid #c7d2fe;
        box-shadow: 0 12px 30px rgba(79, 70, 229, 0.10);
        margin-bottom: 1.8rem;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #172554;
        margin-top: 2.2rem;
        margin-bottom: 1.15rem;
        padding-left: 0.8rem;
        border-left: 5px solid #6366f1;
        line-height: 1.25;
    }

    .metric-card {
        padding: 1.3rem;
        border-radius: 17px;
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe4f0;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.07);
        min-height: 118px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.12);
    }

    .metric-label {
        font-size: 0.76rem;
        color: #6366f1;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.055em;
    }

    .metric-value {
        font-size: 1.48rem;
        color: #172554;
        font-weight: 850;
        margin-top: 0.35rem;
        word-break: break-word;
    }

    .event-card {
        padding: 1.25rem 1.4rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe4f0;
        border-left: 5px solid #6366f1;
        box-shadow: 0 7px 20px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .event-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #312e81;
        margin-bottom: 0.45rem;
    }

    .event-description {
        color: #475569;
        line-height: 1.6;
    }

    .record-card {
        padding: 1.35rem;
        border-radius: 17px;
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe4f0;
        box-shadow: 0 7px 20px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .record-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #312e81;
        margin-bottom: 1rem;
    }

    .record-label {
        font-size: 0.74rem;
        color: #6366f1;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .record-value {
        color: #172554;
        font-weight: 700;
        margin-top: 0.25rem;
    }

    .info-box {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #eff6ff, #f5f3ff);
        border: 1px solid #c7d2fe;
        color: #334155;
        line-height: 1.65;
        margin-top: 0.9rem;
    }

    .conclusion-panel {
        padding: 1.45rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #dbeafe 0%, #ede9fe 52%, #fce7f3 100%);
        border: 1px solid #c4b5fd;
        color: #312e81;
        line-height: 1.7;
        margin-bottom: 1.3rem;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.10);
    }

    .timeline-line {
        border-left: 4px solid #818cf8;
        padding-left: 1.1rem;
        margin-left: 0.4rem;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 11px;
        min-height: 44px;
        border: 1px solid #c7d2fe;
    }

    div[data-testid="stButton"] button {
        border-radius: 11px;
        min-height: 44px;
        font-weight: 750;
        border: 1px solid #4f46e5;
        box-shadow: 0 7px 18px rgba(79, 70, 229, 0.18);
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Audit Trail</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Review the complete financial control history of an invoice, from detection and investigation through recommendation and human decision.</div>',
    unsafe_allow_html=True
)

access_token = st.session_state.get("access_token", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

invoice_id = st.text_input(
    "Enter Invoice ID",
    value="INV-TEST-001"
)

view_audit = st.button(
    "View Audit Trail",
    use_container_width=False
)

if view_audit:

    if not invoice_id:
        st.warning("Please enter an Invoice ID.")

    else:

        try:
            # ---------------------------------------------------------
            # GET INVESTIGATION DATA
            # ---------------------------------------------------------

            investigation_response = requests.get(
                f"{API_URL}/invoices/{invoice_id}/investigation",
                headers=AUTH_HEADERS,
                timeout=10
            )

            # ---------------------------------------------------------
            # GET HUMAN DECISION HISTORY
            # ---------------------------------------------------------

            decision_response = requests.get(
                f"{API_URL}/decisions/{invoice_id}",
                headers=AUTH_HEADERS,
                timeout=10
            )

            # ---------------------------------------------------------
            # GET PERSISTENT AUDIT RECORDS
            # ---------------------------------------------------------

            audit_response = requests.get(
                f"{API_URL}/decisions/{invoice_id}/audit",
                headers=AUTH_HEADERS,
                timeout=10
            )

            if investigation_response.status_code == 200:

                data = investigation_response.json()

                invoice = data.get("invoice", {})
                risk = data.get("risk_result", {})
                recommendation = data.get("recommendation", {})
                investigation = data.get("investigation", {})
                exceptions = data.get("exceptions", [])

                decisions = []
                audit_records = []

                if decision_response.status_code == 200:
                    decision_data = decision_response.json()

                    if isinstance(decision_data, list):
                        decisions = decision_data
                    else:
                        decisions = decision_data.get(
                            "decisions",
                            []
                        )

                if audit_response.status_code == 200:
                    audit_data = audit_response.json()

                    if isinstance(audit_data, list):
                        audit_records = audit_data

                st.success("Audit data retrieved successfully.")

                # =====================================================
                # 1. INVOICE INFORMATION
                # =====================================================

                st.markdown(
                    '<div class="section-title">Invoice Information</div>',
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
                    amount = invoice.get("amount", 0) or 0

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Amount</div>
                            <div class="metric-value">
                                &#8377;{amount:,.0f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col4:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Status</div>
                            <div class="metric-value">
                                {invoice.get("status", "N/A")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =====================================================
                # 2. AUDIT EVENTS
                # =====================================================

                st.markdown(
                    '<div class="section-title">Audit Events</div>',
                    unsafe_allow_html=True
                )

                events = [
                    (
                        "Invoice Received",
                        (
                            f"Invoice "
                            f"{invoice.get('invoice_id', 'N/A')} "
                            "was received for financial processing."
                        )
                    ),
                    (
                        "Exceptions Detected",
                        (
                            f"{len(exceptions)} financial control "
                            "exception(s) were detected."
                        )
                    ),
                    (
                        "Risk Assessment",
                        (
                            f"Risk score calculated as "
                            f"{risk.get('risk_score', 0)} "
                            f"({risk.get('risk_level', 'Unknown')})."
                        )
                    ),
                    (
                        "Root Cause Investigation",
                        investigation.get(
                            "conclusion",
                            "Investigation completed."
                        )
                    ),
                    (
                        "Payment Decision",
                        (
                            f"Recommended action: "
                            f"{recommendation.get('action', 'N/A')}."
                        )
                    ),
                    (
                        "Human Review",
                        (
                            "Human review is required."
                            if recommendation.get(
                                "requires_human_review",
                                False
                            )
                            else
                            "Human review is not required."
                        )
                    )
                ]

                for event_name, description in events:

                    st.markdown(
                        f"""
                        <div class="event-card">
                            <div class="event-title">
                                {event_name}
                            </div>
                            <div class="event-description">
                                {description}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =====================================================
                # 3. RISK ASSESSMENT
                # =====================================================

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

                risk_factors = risk.get(
                    "risk_factors",
                    []
                )

                if risk_factors:

                    st.markdown(
                        '<div class="section-title">Risk Factors</div>',
                        unsafe_allow_html=True
                    )

                    for factor in risk_factors:
                        st.markdown(
                            f"- {factor}"
                        )

                # =====================================================
                # 4. EXCEPTION HISTORY
                # =====================================================

                st.markdown(
                    '<div class="section-title">Exception History</div>',
                    unsafe_allow_html=True
                )

                if exceptions:

                    for exception in exceptions:

                        exception_type = exception.get(
                            "exception_type",
                            "Unknown"
                        )

                        severity = exception.get(
                            "severity",
                            "Unknown"
                        )

                        status = exception.get(
                            "status",
                            "Unknown"
                        )

                        description = exception.get(
                            "description",
                            "No description available."
                        )

                        exception_html = (
                            '<div class="record-card">'
                            '<div class="record-title">'
                            f'{exception_type}'
                            '</div>'
                            '<div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">'
                            '<div>'
                            '<div class="record-label">Severity</div>'
                            f'<div class="record-value">{severity}</div>'
                            '</div>'
                            '<div>'
                            '<div class="record-label">Status</div>'
                            f'<div class="record-value">{status}</div>'
                            '</div>'
                            '</div>'
                            '<div class="info-box">'
                            f'{description}'
                            '</div>'
                            '</div>'
                        )

                        st.markdown(
                            exception_html,
                            unsafe_allow_html=True
                        )

                else:

                    st.success(
                        "No exceptions recorded."
                    )

                # =====================================================
                # 5. AI RECOMMENDATION
                # =====================================================

                st.markdown(
                    '<div class="section-title">AI Recommendation</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Recommended Action</div>
                            <div class="metric-value">
                                {recommendation.get("action", "N/A")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Priority</div>
                            <div class="metric-value">
                                {recommendation.get("priority", "Unknown")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    human_review_text = (
                        "Required"
                        if recommendation.get(
                            "requires_human_review",
                            False
                        )
                        else
                        "Not Required"
                    )

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Human Review</div>
                            <div class="metric-value">
                                {human_review_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.info(
                    recommendation.get(
                        "reason",
                        "No recommendation reason available."
                    )
                )

                # =====================================================
                # 6. ROOT CAUSE INVESTIGATION
                # =====================================================

                st.markdown(
                    '<div class="section-title">AI Root Cause Investigation</div>',
                    unsafe_allow_html=True
                )

                if investigation:

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

                    root_causes = investigation.get(
                        "root_causes",
                        []
                    )

                    if root_causes:

                        st.markdown(
                            '<div class="section-title">Root Causes</div>',
                            unsafe_allow_html=True
                        )

                        for cause in root_causes:
                            st.markdown(
                                f"- {cause}"
                            )

                    st.markdown(
                        '<div class="section-title">Investigation Conclusion</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="conclusion-panel">
                            {investigation.get(
                                "conclusion",
                                "No conclusion available."
                            )}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =====================================================
                # 7. FINAL AUDIT CONCLUSION
                # =====================================================

                st.markdown(
                    '<div class="section-title">Final Audit Conclusion</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="conclusion-panel">
                        {investigation.get(
                            "conclusion",
                            "No audit conclusion available."
                        )}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =====================================================
                # 8. HUMAN REVIEW STATUS
                # =====================================================

                st.markdown(
                    '<div class="section-title">Human Review Status</div>',
                    unsafe_allow_html=True
                )

                human_review_required = recommendation.get(
                    "requires_human_review",
                    False
                )

                if human_review_required:

                    if decisions:

                        latest_decision = decisions[0]

                        st.warning(
                            "Human review has been recorded."
                        )

                    else:

                        st.error(
                            "Human review is required, "
                            "but no human decision has been recorded yet."
                        )

                else:

                    st.success(
                        "This invoice does not require human review."
                    )

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{investigation_response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the backend."
            )
