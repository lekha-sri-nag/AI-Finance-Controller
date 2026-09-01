import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Investigation - AI Finance Controller",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Invoice Investigation")
st.write(
    "Investigate an invoice by reviewing exceptions, risk, "
    "root causes, evidence, and recommended action."
)

invoice_id = st.text_input(
    "Enter Invoice ID",
    value="INV-013"
)

if st.button("Investigate Invoice"):

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

                st.success(
                    "Investigation data retrieved successfully."
                )

                invoice = data.get("invoice", {})
                risk = data.get("risk_result", {})
                exceptions = data.get("exceptions", [])
                investigation = data.get("investigation", {})
                recommendation = data.get("recommendation", {})
                evidence = data.get("evidence", [])

                # Invoice Details
                st.subheader("🧾 Invoice Details")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Invoice ID",
                        invoice.get("invoice_id", "N/A")
                    )

                with col2:
                    st.metric(
                        "Vendor",
                        invoice.get("vendor_id", "N/A")
                    )

                with col3:
                    st.metric(
                        "Amount",
                        f"₹{invoice.get('amount', 0):,.0f}"
                    )

                with col4:
                    st.metric(
                        "Quantity",
                        invoice.get("quantity", 0)
                    )

                st.divider()

                # Risk Assessment
                st.subheader("🔴 Risk Assessment")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Risk Score",
                        risk.get("risk_score", 0)
                    )

                with col2:
                    st.metric(
                        "Risk Level",
                        risk.get("risk_level", "Unknown")
                    )

                st.info(
                    risk.get(
                        "explanation",
                        "No risk explanation available."
                    )
                )

                # Exceptions
                st.subheader("⚠️ Detected Exceptions")

                if exceptions:
                    for exception in exceptions:

                        with st.expander(
                            f"{exception.get('severity', 'Unknown')} — "
                            f"{exception.get('exception_type', 'Unknown')}"
                        ):
                            st.write(
                                "**Exception ID:**",
                                exception.get(
                                    "exception_id",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Status:**",
                                exception.get(
                                    "status",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Description:**",
                                exception.get(
                                    "description",
                                    "N/A"
                                )
                            )
                else:
                    st.success("No exceptions detected.")

                # Root Cause Investigation
                st.subheader("🤖 AI Root Cause Investigation")

                if investigation:

                    st.success(
                        "Investigation Status: "
                        + investigation.get(
                            "investigation_status",
                            "Unknown"
                        )
                    )

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

                    st.write("### 🔍 Root Causes")

                    root_causes = investigation.get(
                        "root_causes",
                        []
                    )

                    for cause in root_causes:
                        st.write(f"• {cause}")

                    st.write("### 🧠 Investigation Conclusion")

                    st.info(
                        investigation.get(
                            "conclusion",
                            "No conclusion available."
                        )
                    )

                # Recommendation
                st.subheader("💡 Recommended Action")

                st.warning(
                    recommendation.get(
                        "action",
                        "No recommendation available."
                    )
                )

                st.write(
                    "**Reason:**",
                    recommendation.get(
                        "reason",
                        "No reason available."
                    )
                )

                if recommendation.get(
                    "requires_human_review",
                    False
                ):
                    st.warning(
                        "👤 Human review is required."
                    )

                # Evidence
                st.subheader("📂 Evidence")

                if evidence:

                    for item in evidence:

                        with st.expander(
                            item.get(
                                "source_type",
                                "Evidence"
                            )
                        ):

                            st.write(
                                "**Source Reference:**",
                                item.get(
                                    "source_reference",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Description:**",
                                item.get(
                                    "description",
                                    "N/A"
                                )
                            )

                            st.write(
                                "**Confidence:**",
                                item.get(
                                    "confidence",
                                    "N/A"
                                )
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
                "❌ Backend API is not running. "
                "Please start FastAPI on port 8000."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )
