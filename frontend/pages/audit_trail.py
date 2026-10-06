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

    .search-panel {
        padding: 1.35rem;
        border-radius: 16px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
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
        min-height: 112px;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.035em;
    }

    .metric-value {
        font-size: 1.45rem;
        color: #1e293b;
        font-weight: 800;
        margin-top: 0.3rem;
        word-break: break-word;
    }

    .event-card {
        padding: 1.2rem 1.3rem;
        border-radius: 14px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    .event-title {
        font-size: 1.05rem;
        font-weight: 750;
        color: #1e293b;
        margin-bottom: 0.45rem;
    }

    .event-description {
        color: #475569;
        line-height: 1.55;
    }

    .record-card {
        padding: 1.3rem;
        border-radius: 15px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    .record-title {
        font-size: 1.05rem;
        font-weight: 750;
        color: #1e293b;
        margin-bottom: 1rem;
    }

    .record-label {
        font-size: 0.76rem;
        color: #64748b;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.035em;
    }

    .record-value {
        color: #1e293b;
        font-weight: 650;
        margin-top: 0.2rem;
    }

    .info-box {
        padding: 1rem;
        border-radius: 11px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        line-height: 1.6;
        margin-top: 0.8rem;
    }

    .conclusion-panel {
        padding: 1.25rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #eff6ff, #f5f3ff);
        border: 1px solid #c7d2fe;
        color: #312e81;
        line-height: 1.65;
        margin-bottom: 1.2rem;
    }

    .timeline-line {
        border-left: 3px solid #c7d2fe;
        padding-left: 1rem;
        margin-left: 0.4rem;
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

st.markdown(
    '<div class="search-panel">',
    unsafe_allow_html=True
)

invoice_id = st.text_input(
    "Enter Invoice ID",
    value="INV-TEST-001"
)

view_audit = st.button(
    "View Audit Trail",
    use_container_width=False
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
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

                        st.markdown(
                            f"""
                            <div class="record-card">
                                <div class="record-title">
                                    {exception_type}
                                </div>

                                <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">

                                    <div>
                                        <div class="record-label">Severity</div>
                                        <div class="record-value">{severity}</div>
                                    </div>

                                    <div>
                                        <div class="record-label">Status</div>
                                        <div class="record-value">{status}</div>
                                    </div>

                                </div>

                                <div class="info-box">
                                    {description}
                                </div>
                            </div>
                            """,
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
                # 7. HUMAN DECISION HISTORY
                # =====================================================

                st.markdown(
                    '<div class="section-title">Human Decision History</div>',
                    unsafe_allow_html=True
                )

                if decisions:

                    st.success(
                        f"{len(decisions)} human decision(s) recorded for this invoice."
                    )

                    for index, decision in enumerate(
                        decisions,
                        start=1
                    ):

                        st.markdown(
                            f"""
                            <div class="record-card">
                                <div class="record-title">
                                    Decision #{index}
                                </div>

                                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;">

                                    <div>
                                        <div class="record-label">Decision</div>
                                        <div class="record-value">
                                            {decision.get("decision", "N/A")}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="record-label">Reviewer</div>
                                        <div class="record-value">
                                            {decision.get("decided_by", "N/A")}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="record-label">Decision ID</div>
                                        <div class="record-value">
                                            {decision.get("decision_id", "N/A")}
                                        </div>
                                    </div>

                                </div>

                                <div class="info-box">
                                    <strong>Recommendation ID:</strong>
                                    {decision.get("recommendation_id", "N/A")}
                                    <br><br>
                                    <strong>Decision Time:</strong>
                                    {decision.get("decided_at", "N/A")}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        comments = decision.get(
                            "comments",
                            ""
                        )

                        if comments:
                            st.info(
                                comments
                            )
                        else:
                            st.caption(
                                "No reviewer comments provided."
                            )

                else:

                    st.info(
                        "No human decisions have been recorded for this invoice."
                    )

                # =====================================================
                # 8. PERSISTED AUDIT RECORDS
                # =====================================================

                st.markdown(
                    '<div class="section-title">Persisted Audit Records</div>',
                    unsafe_allow_html=True
                )

                if audit_records:

                    st.success(
                        f"{len(audit_records)} persistent audit record(s) retrieved from the database."
                    )

                    for index, record in enumerate(
                        audit_records,
                        start=1
                    ):

                        st.markdown(
                            f"""
                            <div class="record-card">
                                <div class="record-title">
                                    Audit Record #{index}
                                </div>

                                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;">

                                    <div>
                                        <div class="record-label">Action</div>
                                        <div class="record-value">
                                            {record.get("action", "N/A")}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="record-label">Performed By</div>
                                        <div class="record-value">
                                            {record.get("performed_by", "N/A")}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="record-label">Audit ID</div>
                                        <div class="record-value">
                                            {record.get("audit_id", "N/A")}
                                        </div>
                                    </div>

                                </div>

                                <div class="info-box">
                                    <strong>Entity:</strong>
                                    {record.get("entity_type", "N/A")} /
                                    {record.get("entity_id", "N/A")}
                                    <br><br>

                                    <strong>Performed At:</strong>
                                    {record.get("performed_at", "N/A")}
                                    <br><br>

                                    <strong>Details:</strong><br>
                                    {record.get("details", "No details available.")}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No persistent audit records have been recorded for this invoice."
                    )

                # =====================================================
                # 9. FINAL AUDIT CONCLUSION
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
                # 10. HUMAN REVIEW STATUS
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

                        st.write(
                            f"**Latest Decision:** "
                            f"{latest_decision.get(
                                'decision',
                                'N/A'
                            )}"
                        )

                        st.write(
                            f"**Reviewed By:** "
                            f"{latest_decision.get(
                                'decided_by',
                                'N/A'
                            )}"
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
