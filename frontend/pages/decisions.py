import streamlit as st
import requests


from frontend.config import API_URL
st.set_page_config(
    page_title="Decisions - AI Finance Controller",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

access_token = st.session_state.get("access_token")
user_data = st.session_state.get("user") or {}

username = user_data.get(
    "username",
    st.session_state.get("username", "Unknown User")
)

user_role = user_data.get(
    "role",
    ""
)

if not access_token:
    st.error(
        "🔒 Please log in to access the Decision Center."
    )
    st.stop()

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("⚖️ Financial Decision Center")

st.write(
    "Review AI-generated payment decisions and record "
    "human decisions for financial control."
)

st.caption(
    f"Logged in as: {username} | Role: {user_role}"
)


# --------------------------------------------------
# INVOICE INPUT
# --------------------------------------------------

invoice_id = st.text_input(
    "Enter Invoice ID",
    value=st.session_state.get(
        "selected_invoice_id",
        "INV-TEST-001"
    )
)


# --------------------------------------------------
# REVIEW DECISION
# --------------------------------------------------

if st.button("Review Decision"):

    if not invoice_id:

        st.warning(
            "Please enter an Invoice ID."
        )

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

                # Save the reviewed invoice data so that it
                # remains available during Streamlit reruns.
                st.session_state["decision_data"] = data

                st.session_state[
                    "selected_invoice_id"
                ] = invoice_id

                st.success(
                    "Decision data retrieved successfully."
                )

            elif response.status_code == 401:

                st.error(
                    "🔒 Your session has expired. "
                    "Please log in again."
                )
                st.stop()

            elif response.status_code == 403:

                st.error(
                    "🚫 You do not have permission to "
                    "view this investigation."
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
                "❌ Backend API is not running. "
                "Please start FastAPI on port 8000."
            )
            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Could not retrieve decision data: {e}"
            )
            st.stop()


# --------------------------------------------------
# LOAD SAVED DECISION DATA
# --------------------------------------------------

data = st.session_state.get(
    "decision_data"
)


if data:

    invoice = data.get(
        "invoice",
        {}
    )

    risk = data.get(
        "risk_result",
        {}
    )

    recommendation = data.get(
        "recommendation",
        {}
    )

    investigation = data.get(
        "investigation",
        {}
    )


    # --------------------------------------------------
    # INVOICE SUMMARY
    # --------------------------------------------------

    st.subheader(
        "🧾 Invoice Summary"
    )

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
            "Amount",
            f"₹{invoice.get('amount', 0):,.0f}"
        )

    with col3:

        st.metric(
            "Risk Score",
            risk.get(
                "risk_score",
                0
            )
        )

    with col4:

        st.metric(
            "Risk Level",
            risk.get(
                "risk_level",
                "Unknown"
            )
        )

    st.divider()


    # --------------------------------------------------
    # AI DECISION
    # --------------------------------------------------

    st.subheader(
        "🤖 AI Decision"
    )

    action = recommendation.get(
        "action",
        "No recommendation available"
    )

    priority = recommendation.get(
        "priority",
        "Unknown"
    )

    human_review = recommendation.get(
        "requires_human_review",
        False
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Recommended Action",
            action
        )

    with col2:

        st.metric(
            "Priority",
            priority
        )

    with col3:

        st.metric(
            "Human Review",
            "Required"
            if human_review
            else "Not Required"
        )

    st.divider()


    # --------------------------------------------------
    # DECISION REASON
    # --------------------------------------------------

    st.subheader(
        "📋 Decision Reason"
    )

    st.info(
        recommendation.get(
            "reason",
            "No decision reason available."
        )
    )


    # --------------------------------------------------
    # RISK FACTORS
    # --------------------------------------------------

    st.subheader(
        "🔍 Decision Factors"
    )

    risk_factors = risk.get(
        "risk_factors",
        []
    )

    if risk_factors:

        for factor in risk_factors:

            st.write(
                f"• {factor}"
            )

    else:

        st.success(
            "No major risk factors detected."
        )


    # --------------------------------------------------
    # INVESTIGATION
    # --------------------------------------------------

    st.subheader(
        "🧠 Investigation Summary"
    )

    st.write(
        investigation.get(
            "conclusion",
            "No investigation conclusion available."
        )
    )

    st.divider()


    # --------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------

    st.subheader(
        "👤 Human Review Decision"
    )

    if human_review:

        # ----------------------------------------------
        # USERS WHO CAN SUBMIT FINAL DECISIONS
        # ----------------------------------------------

        can_submit_decision = user_role in {
            "admin",
            "finance_controller"
        }


        if can_submit_decision:

            st.warning(
                "This invoice requires human review "
                "before payment."
            )


            # ------------------------------------------
            # HUMAN DECISION FORM
            # ------------------------------------------

            with st.form(
                "human_review_form"
            ):

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


            # ------------------------------------------
            # SUBMIT HUMAN DECISION
            # ------------------------------------------

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


                    # ----------------------------------
                    # SUCCESS
                    # ----------------------------------

                    if save_response.status_code == 200:

                        result = save_response.json()

                        st.success(
                            "✅ Human decision saved successfully."
                        )


                        # Handle the backend response safely
                        if isinstance(result, dict):

                            saved = result.get(
                                "decision",
                                result
                            )


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


                    # ----------------------------------
                    # FORBIDDEN
                    # ----------------------------------

                    elif save_response.status_code == 403:

                        st.error(
                            "🚫 You do not have permission "
                            "to submit final decisions."
                        )


                    # ----------------------------------
                    # UNAUTHORIZED
                    # ----------------------------------

                    elif save_response.status_code == 401:

                        st.error(
                            "🔒 Your session has expired. "
                            "Please log in again."
                        )


                    # ----------------------------------
                    # OTHER BACKEND ERROR
                    # ----------------------------------

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


        # ----------------------------------------------
        # REVIEW-ONLY USERS
        # ----------------------------------------------

        else:

            st.info(
                "👀 You can review this decision, "
                "but your role does not have permission "
                "to submit the final decision."
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


    st.divider()


    # --------------------------------------------------
    # DECISION HISTORY
    # --------------------------------------------------

    st.subheader(
        "📜 Decision History"
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

                    with st.expander(
                        f"{item.get('decision', 'Unknown')} "
                        f"— "
                        f"{item.get('decided_at', 'Unknown')}"
                    ):

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


            else:

                st.info(
                    "No human decisions have been "
                    "recorded yet."
                )


        elif history_response.status_code == 401:

            st.error(
                "🔒 Your session has expired. "
                "Please log in again."
            )


        elif history_response.status_code == 403:

            st.error(
                "🚫 You do not have permission "
                "to view decision history."
            )


        else:

            st.error(
                "Could not retrieve decision history."
            )


    except requests.exceptions.RequestException as e:

        st.error(
            f"Could not retrieve decision history: {e}"
        )