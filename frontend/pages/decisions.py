import streamlit as st
import requests

from frontend.config import API_URL

st.set_page_config(
    page_title="Decisions - AI Finance Controller",
    layout="wide"
)

# =========================================================
# AUTHENTICATION
# =========================================================

access_token = st.session_state.get("access_token")
user_data = st.session_state.get("user") or {}

username = user_data.get(
    "username",
    st.session_state.get("username", "Unknown User")
)

user_role = user_data.get("role", "")

if not access_token:
    st.error("Please log in to access the Decision Center.")
    st.stop()

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}


# =========================================================
# PROFESSIONAL DECISION CENTER UI
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.35rem;
        font-weight: 750;
        letter-spacing: -0.5px;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.6rem;
    }

    .search-panel {
        padding: 1.25rem 1.35rem;
        border: 1px solid #dbe4f0;
        border-radius: 14px;
        background: linear-gradient(135deg, #f8fbff, #f3f6ff);
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 1.55rem;
        margin-bottom: 0.85rem;
    }

    .invoice-panel {
        padding: 1.25rem 1.35rem;
        border-radius: 14px;
        border: 1px solid #dbe4f0;
        background: #ffffff;
        margin-bottom: 1rem;
    }

    .metric-card {
        padding: 1.15rem 1.2rem;
        border-radius: 14px;
        border: 1px solid #dbe4f0;
        background: linear-gradient(145deg, #ffffff, #f7f9fc);
        min-height: 105px;
        margin-bottom: 0.8rem;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.45rem;
    }

    .metric-value {
        font-size: 1.35rem;
        font-weight: 750;
        color: #172033;
    }

    .risk-panel {
        padding: 1.3rem 1.4rem;
        border-radius: 14px;
        border: 1px solid #dbe4f0;
        background: linear-gradient(135deg, #f8faff, #eef2ff);
        margin: 0.8rem 0 1.2rem 0;
    }

    .risk-high {
        color: #b42318;
        font-weight: 750;
    }

    .risk-medium {
        color: #b54708;
        font-weight: 750;
    }

    .risk-low {
        color: #027a48;
        font-weight: 750;
    }

    .recommendation-panel {
        padding: 1.3rem 1.4rem;
        border-radius: 14px;
        border: 1px solid #c7d7fe;
        background: linear-gradient(135deg, #eef4ff, #f5f3ff);
        margin-bottom: 1.2rem;
    }

    .recommendation-title {
        color: #344054;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .recommendation-value {
        color: #1d2939;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 0.3rem;
    }

    .exception-card {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid #f2d5d5;
        background: #fff8f8;
        margin-bottom: 0.75rem;
    }

    .exception-title {
        font-weight: 750;
        color: #912018;
        margin-bottom: 0.35rem;
    }

    .exception-text {
        color: #475467;
        line-height: 1.5;
    }

    .review-panel {
        padding: 1.35rem;
        border-radius: 14px;
        border: 1px solid #cfd9e6;
        background: linear-gradient(135deg, #f8fafc, #f5f7fb);
        margin: 0.8rem 0 1.2rem 0;
    }

    .history-card {
        padding: 1.1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid #dbe4f0;
        background: #ffffff;
        margin-bottom: 0.8rem;
    }

    .history-title {
        font-size: 1rem;
        font-weight: 750;
        color: #172033;
        margin-bottom: 0.55rem;
    }

    .info-box {
        padding: 1rem 1.15rem;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin: 0.7rem 0;
    }

    .decision-success {
        padding: 1rem 1.15rem;
        border-radius: 12px;
        background: #ecfdf3;
        border: 1px solid #abefc6;
        color: #05603a;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    '<div class="main-title">Financial Decision Center</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Review AI-generated financial recommendations, assess risk, '
    'and record the final human control decision.'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Logged in as: {username}  |  Role: {user_role}"
)


# =========================================================
# INVOICE INPUT
# =========================================================

st.markdown(
    '<div class="section-title">Invoice Review</div>',
    unsafe_allow_html=True
)

invoice_id = st.text_input(
    "Invoice ID",
    value=st.session_state.get(
        "selected_invoice_id",
        "INV-TEST-001"
    )
)

review_clicked = st.button(
    "Review Decision",
    use_container_width=False
)



# =========================================================
# REVIEW DECISION
# =========================================================

if review_clicked:

    if not invoice_id:

        st.warning("Please enter an Invoice ID.")

    else:

        try:

            response = requests.get(
                f"{API_URL}/invoices/"
                f"{invoice_id}/investigation",
                headers=AUTH_HEADERS,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state["decision_data"] = data

                st.session_state[
                    "selected_invoice_id"
                ] = invoice_id

                st.success(
                    "Decision data retrieved successfully."
                )

            elif response.status_code == 401:

                st.error(
                    "Your session has expired. Please log in again."
                )
                st.stop()

            elif response.status_code == 403:

                st.error(
                    "You do not have permission to view this investigation."
                )
                st.stop()

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )
                st.stop()

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the backend."
            )
            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(
                f"Could not retrieve decision data: {e}"
            )
            st.stop()


# =========================================================
# DISPLAY REVIEWED DATA
# =========================================================

decision_data = st.session_state.get("decision_data")

if decision_data:

    invoice = decision_data.get(
        "invoice",
        {}
    )

    risk = decision_data.get(
        "risk_result",
        {}
    )

    exceptions = decision_data.get(
        "exceptions",
        []
    )

    investigation = decision_data.get(
        "investigation",
        {}
    )

    recommendation = decision_data.get(
        "recommendation",
        {}
    )

    human_review = True


    # =====================================================
    # INVOICE SUMMARY
    # =====================================================

    st.markdown(
        '<div class="section-title">Invoice Overview</div>',
        unsafe_allow_html=True
    )

    amount = invoice.get(
        "amount",
        "N/A"
    )

    amount_display = (
        f"&#8377; {amount}"
        if amount != "N/A"
        else "N/A"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Invoice ID</div>
                <div class="metric-value">{invoice.get("invoice_id", invoice_id)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Invoice Amount</div>
                <div class="metric-value">{amount_display}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Vendor</div>
                <div class="metric-value">{decision_data.get("vendor", {}).get("vendor_name", "N/A")}</div>            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # RISK ASSESSMENT
    # =====================================================

    st.markdown(
        '<div class="section-title">Risk Assessment</div>',
        unsafe_allow_html=True
    )

    risk_score = risk.get(
        "risk_score",
        risk.get("score", "N/A")
    )

    risk_level = risk.get(
        "risk_level",
        risk.get("level", "N/A")
    )

    risk_level_class = ""

    if isinstance(risk_level, str):

        if risk_level.lower() == "high":
            risk_level_class = "risk-high"

        elif risk_level.lower() == "medium":
            risk_level_class = "risk-medium"

        elif risk_level.lower() == "low":
            risk_level_class = "risk-low"

    st.markdown(
        f"""
        <div class="risk-panel">
            <div class="metric-label">Overall Risk</div>
            <div class="metric-value">
                Score: {risk_score}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <span class="{risk_level_class}">{risk_level}</span>
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
            "**Key Risk Factors**"
        )

        for factor in risk_factors:

            st.markdown(
                f"- {factor}"
            )

    else:

        st.success(
            "No major risk factors detected."
        )


    # =====================================================
    # EXCEPTIONS
    # =====================================================

    if exceptions:

        st.markdown(
            '<div class="section-title">Detected Exceptions</div>',
            unsafe_allow_html=True
        )

        for exception in exceptions:

            if not isinstance(exception, dict):
                continue

            exception_type = exception.get(
                "exception_type",
                exception.get("type", "Financial Exception")
            )

            severity = exception.get(
                "severity",
                "N/A"
            )

            description = exception.get(
                "description",
                exception.get(
                    "message",
                    "No description available."
                )
            )

            st.markdown(
                f"""
                <div class="exception-card">
                    <div class="exception-title">
                        {exception_type} | Severity: {severity}
                    </div>
                    <div class="exception-text">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    st.markdown(
        '<div class="section-title">AI Recommendation</div>',
        unsafe_allow_html=True
    )

    recommendation_value = recommendation.get(
        "action",
        recommendation.get(
            "recommendation",
            recommendation.get(
                "decision",
                "No recommendation available."
            )
        )
    )

    recommendation_reason = recommendation.get(
        "reason",
        recommendation.get(
            "explanation",
            recommendation.get(
                "rationale",
                ""
            )
        )
    )

    st.markdown(
        f"""
        <div class="recommendation-panel">
            <div class="recommendation-title">
                Recommended Financial Action
            </div>
            <div class="recommendation-value">
                {recommendation_value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if recommendation_reason:

        st.markdown(
            f'<div class="info-box"><strong>Rationale:</strong> '
            f'{recommendation_reason}</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # INVESTIGATION
    # =====================================================

    st.markdown(
        '<div class="section-title">Investigation Summary</div>',
        unsafe_allow_html=True
    )

    investigation_conclusion = investigation.get(
        "conclusion",
        "No investigation conclusion available."
    )

    st.markdown(
        f'<div class="info-box">{investigation_conclusion}</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # HUMAN REVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">Human Review Decision</div>',
        unsafe_allow_html=True
    )

    if human_review:

        can_submit_decision = user_role in {
            "admin",
            "finance_controller"
        }

        if can_submit_decision:

            st.warning(
                "This invoice requires human review before payment."
            )

            with st.form("human_review_form"):

                decision = st.radio(
                    "Select review outcome:",
                    [
                        "Approve",
                        "Reject",
                        "Hold",
                        "Block"
                    ]
                )

                reviewer_note = st.text_area(
                    "Reviewer Notes",
                    placeholder=(
                        "Enter your review comments..."
                    )
                )

                submit_decision = st.form_submit_button(
                    "Submit Review Decision"
                )

            # =================================================
            # SUBMIT HUMAN DECISION
            # =================================================

            if submit_decision:

                payload = {
                    "invoice_id": invoice_id,
                    "recommendation_id": (
                        f"REC-{invoice_id}"
                    ),
                    "decision": decision,
                    "comments": reviewer_note
                }

                try:

                    save_response = requests.post(
                        f"{API_URL}/decisions/",
                        headers=AUTH_HEADERS,
                        json=payload,
                        timeout=10
                    )


                    if save_response.status_code == 200:

                        result = save_response.json()

                        st.success(
                            "Human decision saved successfully."
                        )

                        if isinstance(result, dict):

                            saved = result
                            if isinstance(saved, dict):


                                st.write(
                                    "**Decision ID:**",
                                    saved.get(
                                        "decision_id",
                                        "N/A"
                                    )
                                )

                                st.write(
                                    "**Decision:**",
                                    saved.get(
                                        "decision",
                                        "N/A"
                                    )
                                )

                                st.write(
                                    "**Decision Maker:**",
                                    saved.get(
                                        "decided_by",
                                        username
                                    )
                                )

                                st.write(
                                    "**Comments:**",
                                    saved.get(
                                        "comments",
                                        ""
                                    )
                                )

    

                            else:

                                st.write(
                                    "**Decision:**",
                                    saved
                                )

                        else:

                            st.write(
                                "**Decision:**",
                                result
                            )


                    elif save_response.status_code == 403:

                        st.error(
                            "You do not have permission to submit final decisions."
                        )


                    elif save_response.status_code == 401:

                        st.error(
                            "Your session has expired. Please log in again."
                        )


                    else:

                        st.error(
                            f"Failed to save decision. "
                            f"Backend returned "
                            f"{save_response.status_code}"
                        )

                        st.write(
                            save_response.text
                        )


                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not save decision: {e}"
                    )


        else:

            st.info(
                "You can review this decision, but your role "
                "does not have permission to submit the final decision."
            )

            st.write(
                "Your current role:",
                f"**{user_role}**"
            )

            st.write(
                "Final decision submission is restricted "
                "to Admin and Finance Controller users."
            )


    else:

        st.success(
            "AI decision does not require human review."
        )


    # =====================================================
    # DECISION HISTORY
    # =====================================================

    st.markdown(
        '<div class="section-title">Decision History</div>',
        unsafe_allow_html=True
    )

    try:

        history_response = requests.get(
            f"{API_URL}/decisions/{invoice_id}",
            headers=AUTH_HEADERS,
            timeout=10
        )

        if history_response.status_code == 200:

            history_data = history_response.json()

            if isinstance(
                history_data,
                list
            ):

                decisions = history_data

            elif isinstance(
                history_data,
                dict
            ):

                decisions = history_data.get(
                    "decisions",
                    []
                )

            else:

                decisions = []


            if decisions:

                st.success(
                    f"{len(decisions)} decision(s) found."
                )

                for item in decisions:

                    if not isinstance(
                        item,
                        dict
                    ):
                        continue

                    decision_name = item.get(
                        "decision",
                        "Unknown"
                    )

                    decided_at = item.get(
                        "decided_at",
                        "Unknown"
                    )

                    

                    st.markdown(
                        f'<div class="history-title">'
                        f'{decision_name} - {decided_at}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        "**Decision ID:**",
                        item.get(
                            "decision_id",
                            "N/A"
                        )
                    )

                    st.write(
                        "**Recommendation ID:**",
                        item.get(
                            "recommendation_id",
                            "N/A"
                        )
                    )

                    st.write(
                        "**Decided By:**",
                        item.get(
                            "decided_by",
                            "N/A"
                        )
                    )

                    st.write(
                        "**Comments:**",
                        item.get(
                            "comments",
                            ""
                        )
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


            else:

                st.info(
                    "No human decisions have been recorded yet."
                )


        elif history_response.status_code == 401:

            st.error(
                "Your session has expired. Please log in again."
            )


        elif history_response.status_code == 403:

            st.error(
                "You do not have permission to view decision history."
            )


        else:

            st.error(
                "Could not retrieve decision history."
            )


    except requests.exceptions.RequestException as e:

        st.error(
            f"Could not retrieve decision history: {e}"
        )
