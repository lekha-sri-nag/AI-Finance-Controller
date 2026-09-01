import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Decisions - AI Finance Controller",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Financial Decision Center")

st.write(
    "Review AI-generated payment decisions and record human "
    "decisions for financial control."
)

invoice_id = st.text_input(
    "Enter Invoice ID",
    value="INV-013"
)

if st.button("Review Decision"):

    if not invoice_id:
        st.warning("Please enter an Invoice ID.")

    else:
        try:
            response = requests.get(
                f"{API_URL}/invoices/{invoice_id}/investigation",
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                invoice = data.get("invoice", {})
                risk = data.get("risk_result", {})
                recommendation = data.get("recommendation", {})
                investigation = data.get("investigation", {})

                st.success("Decision data retrieved successfully.")

                # --------------------------------------------------
                # INVOICE SUMMARY
                # --------------------------------------------------

                st.subheader("🧾 Invoice Summary")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Invoice ID",
                        invoice.get("invoice_id", "N/A")
                    )

                with col2:
                    st.metric(
                        "Amount",
                        f"₹{invoice.get('amount', 0):,.0f}"
                    )

                with col3:
                    st.metric(
                        "Risk Score",
                        risk.get("risk_score", 0)
                    )

                with col4:
                    st.metric(
                        "Risk Level",
                        risk.get("risk_level", "Unknown")
                    )

                st.divider()

                # --------------------------------------------------
                # AI DECISION
                # --------------------------------------------------

                st.subheader("🤖 AI Decision")

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
                        "Required" if human_review else "Not Required"
                    )

                st.divider()

                # --------------------------------------------------
                # DECISION REASON
                # --------------------------------------------------

                st.subheader("📋 Decision Reason")

                st.info(
                    recommendation.get(
                        "reason",
                        "No decision reason available."
                    )
                )

                # --------------------------------------------------
                # RISK FACTORS
                # --------------------------------------------------

                st.subheader("🔍 Decision Factors")

                risk_factors = risk.get(
                    "risk_factors",
                    []
                )

                if risk_factors:
                    for factor in risk_factors:
                        st.write(f"• {factor}")
                else:
                    st.success("No major risk factors detected.")

                # --------------------------------------------------
                # INVESTIGATION
                # --------------------------------------------------

                st.subheader("🧠 Investigation Summary")

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

                st.subheader("👤 Human Review Decision")

                if human_review:

                    st.warning(
                        "This invoice requires human review before payment."
                    )

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
                        placeholder="Enter your review comments..."
                    )

                    if st.button("Submit Review Decision"):

                        payload = {
                            "invoice_id": invoice_id,
                            "recommendation_id": f"REC-{invoice_id}",
                            "decision": decision,
                            "decided_by": "finance_reviewer",
                            "comments": reviewer_note
                        }

                        try:

                            save_response = requests.post(
                                f"{API_URL}/decisions/",
                                json=payload,
                                timeout=10
                            )

                            if save_response.status_code == 200:

                                result = save_response.json()

                                st.success(
                                    "✅ Human decision saved successfully."
                                )

                                saved = result.get(
                                    "decision",
                                    {}
                                )

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
                                    "**Decided By:**",
                                    saved.get(
                                        "decided_by",
                                        "N/A"
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

                    st.success(
                        "AI decision does not require human review."
                    )

                st.divider()

                # --------------------------------------------------
                # DECISION HISTORY
                # --------------------------------------------------

                st.subheader("📜 Decision History")

                try:

                    history_response = requests.get(
                        f"{API_URL}/decisions/{invoice_id}",
                        timeout=10
                    )

                    if history_response.status_code == 200:

                        history_data = history_response.json()

                        decisions = history_data.get(
                            "decisions",
                            []
                        )

                        if decisions:

                            st.success(
                                f"{len(decisions)} decision(s) found."
                            )

                            for item in decisions:

                                with st.expander(
                                    f"{item.get('decision', 'Unknown')} "
                                    f"— {item.get('decided_at', 'Unknown')}"
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
                                "No human decisions have been recorded yet."
                            )

                    else:

                        st.error(
                            "Could not retrieve decision history."
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not retrieve decision history: {e}"
                    )

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Backend API is not running. "
                "Please start FastAPI on port 8000."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )
