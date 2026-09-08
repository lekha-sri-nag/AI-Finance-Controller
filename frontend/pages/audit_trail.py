import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
access_token = st.session_state.get("access_token", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}

st.set_page_config(
    page_title="Audit Trail - AI Finance Controller",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Audit Trail")

st.write(
    "Review the complete financial control history of an invoice, "
    "including exceptions, risk assessment, AI decisions, "
    "investigation results, and human review decisions."
)

invoice_id = st.text_input(
    "Enter Invoice ID",
    value="INV-TEST-001"
)

if st.button("View Audit Trail"):

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

            if investigation_response.status_code == 200:

                data = investigation_response.json()

                invoice = data.get("invoice", {})
                risk = data.get("risk_result", {})
                recommendation = data.get("recommendation", {})
                investigation = data.get("investigation", {})
                exceptions = data.get("exceptions", [])

                # Decision history is optional.
                # If the endpoint is unavailable, the rest of
                # the audit trail can still be displayed.
                decisions = []

                if decision_response.status_code == 200:
                    decision_data = decision_response.json()

                if isinstance(decision_data, list):
                    decisions = decision_data
                else:
                    decisions = decision_data.get(
                    "decisions",
                    []
                )

                st.success("Audit data retrieved successfully.")

                # =====================================================
                # 1. INVOICE INFORMATION
                # =====================================================

                st.subheader("🧾 Invoice Information")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Invoice ID",
                        invoice.get(
                            "invoice_id",
                            "N/A"
                        )
                    )

                with col2:
                    st.metric(
                        "Vendor",
                        invoice.get(
                            "vendor_id",
                            "N/A"
                        )
                    )

                with col3:
                    st.metric(
                        "Amount",
                        f"₹{invoice.get('amount', 0):,.0f}"
                    )

                with col4:
                    st.metric(
                        "Status",
                        invoice.get(
                            "status",
                            "N/A"
                        )
                    )

                st.divider()

                # =====================================================
                # 2. AUDIT EVENTS
                # =====================================================

                st.subheader("🔍 Audit Events")

                events = [
                    (
                        "📥 Invoice Received",
                        (
                            f"Invoice "
                            f"{invoice.get('invoice_id', 'N/A')} "
                            "was received for financial processing."
                        )
                    ),
                    (
                        "⚠️ Exceptions Detected",
                        (
                            f"{len(exceptions)} financial control "
                            "exception(s) were detected."
                        )
                    ),
                    (
                        "🔴 Risk Assessment",
                        (
                            f"Risk score calculated as "
                            f"{risk.get('risk_score', 0)} "
                            f"({risk.get('risk_level', 'Unknown')})."
                        )
                    ),
                    (
                        "🤖 Root Cause Investigation",
                        investigation.get(
                            "conclusion",
                            "Investigation completed."
                        )
                    ),
                    (
                        "💳 Payment Decision",
                        (
                            f"Recommended action: "
                            f"{recommendation.get('action', 'N/A')}."
                        )
                    ),
                    (
                        "👤 Human Review",
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

                    with st.container(border=True):

                        st.write(
                            f"### {event_name}"
                        )

                        st.write(description)

                st.divider()

                # =====================================================
                # 3. RISK ASSESSMENT
                # =====================================================

                st.subheader("🔴 Risk Assessment")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Risk Score",
                        risk.get(
                            "risk_score",
                            0
                        )
                    )

                with col2:
                    st.metric(
                        "Risk Level",
                        risk.get(
                            "risk_level",
                            "Unknown"
                        )
                    )

                risk_factors = risk.get(
                    "risk_factors",
                    []
                )

                if risk_factors:

                    st.write("### Risk Factors")

                    for factor in risk_factors:
                        st.write(
                            f"• {factor}"
                        )

                st.divider()

                # =====================================================
                # 4. EXCEPTION HISTORY
                # =====================================================

                st.subheader("⚠️ Exception History")

                if exceptions:

                    for exception in exceptions:

                        with st.container(border=True):

                            st.write(
                                f"### "
                                f"{exception.get(
                                    'exception_type',
                                    'Unknown'
                                )}"
                            )

                            st.caption(
                                f"Severity: "
                                f"{exception.get(
                                    'severity',
                                    'Unknown'
                                )} | "
                                f"Status: "
                                f"{exception.get(
                                    'status',
                                    'Unknown'
                                )}"
                            )

                            st.write(
                                exception.get(
                                    "description",
                                    "No description available."
                                )
                            )

                else:

                    st.success(
                        "No exceptions recorded."
                    )

                st.divider()

                # =====================================================
                # 5. AI RECOMMENDATION
                # =====================================================

                st.subheader("🤖 AI Recommendation")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Recommended Action",
                        recommendation.get(
                            "action",
                            "N/A"
                        )
                    )

                with col2:
                    st.metric(
                        "Priority",
                        recommendation.get(
                            "priority",
                            "Unknown"
                        )
                    )

                with col3:
                    st.metric(
                        "Human Review",
                        (
                            "Required"
                            if recommendation.get(
                                "requires_human_review",
                                False
                            )
                            else
                            "Not Required"
                        )
                    )

                st.info(
                    recommendation.get(
                        "reason",
                        "No recommendation reason available."
                    )
                )

                st.divider()

                # =====================================================
                # 6. ROOT CAUSE INVESTIGATION
                # =====================================================

                st.subheader(
                    "🧠 AI Root Cause Investigation"
                )

                if investigation:

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Exceptions",
                            investigation.get(
                                "exceptions_count",
                                0
                            )
                        )

                    with col2:
                        st.metric(
                            "High-Risk Exceptions",
                            investigation.get(
                                "high_risk_exceptions",
                                0
                            )
                        )

                    with col3:
                        st.metric(
                            "Risk Level",
                            investigation.get(
                                "risk_level",
                                "Unknown"
                            )
                        )

                    root_causes = investigation.get(
                        "root_causes",
                        []
                    )

                    if root_causes:

                        st.write("### Root Causes")

                        for cause in root_causes:
                            st.write(
                                f"• {cause}"
                            )

                    st.write(
                        "### Investigation Conclusion"
                    )

                    st.info(
                        investigation.get(
                            "conclusion",
                            "No conclusion available."
                        )
                    )

                st.divider()

                # =====================================================
                # 7. HUMAN DECISION HISTORY
                # =====================================================

                st.subheader(
                    "👤 Human Decision History"
                )

                if decisions:

                    st.success(
                        f"{len(decisions)} human decision(s) "
                        "recorded for this invoice."
                    )

                    for index, decision in enumerate(
                        decisions,
                        start=1
                    ):

                        with st.container(border=True):

                            st.write(
                                f"### Decision #{index}"
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric(
                                    "Decision",
                                    decision.get(
                                        "decision",
                                        "N/A"
                                    )
                                )

                            with col2:
                                st.metric(
                                    "Reviewer",
                                    decision.get(
                                        "decided_by",
                                        "N/A"
                                    )
                                )

                            with col3:
                                st.metric(
                                    "Decision ID",
                                    decision.get(
                                        "decision_id",
                                        "N/A"
                                    )
                                )

                            st.write(
                                "**Recommendation ID:**",
                                decision.get(
                                    "recommendation_id",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Decision Time:**",
                                decision.get(
                                    "decided_at",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Reviewer Comments:**"
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
                        "No human decisions have been recorded "
                        "for this invoice."
                    )

                st.divider()

                # =====================================================
                # 8. FINAL AUDIT CONCLUSION
                # =====================================================

                st.subheader(
                    "🧠 Final Audit Conclusion"
                )

                st.info(
                    investigation.get(
                        "conclusion",
                        "No audit conclusion available."
                    )
                )

                # =====================================================
                # 9. HUMAN REVIEW STATUS
                # =====================================================

                st.subheader(
                    "👤 Human Review Status"
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
                "❌ Backend API is not running. "
                "Please make sure FastAPI is running on port 8000."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )