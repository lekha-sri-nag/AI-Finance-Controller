import requests
import streamlit as st

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)


API_URL = "http://127.0.0.1:8000"


# =========================================================
# AUTHENTICATION
# =========================================================

def login_user(username, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": username,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


def logout():
    keys_to_remove = [
        "access_token",
        "user",
        "validated_invoices",
        "uploaded_file_name",
        "document_upload",
        "processed_result",
        "selected_invoice_id",
        "ocr_result"
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)

    st.rerun()


# Initialize authentication state
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "user" not in st.session_state:
    st.session_state["user"] = None


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state["access_token"]:

    st.title("💰 AI Finance Controller")
    st.subheader("Secure Financial Control System")

    st.divider()

    st.markdown("### 🔐 Login")

    with st.form("login_form"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login_button:

        if not username or not password:

            st.warning(
                "Please enter both username and password."
            )

        else:

            result = login_user(
                username,
                password
            )

            if result:

                st.session_state["access_token"] = (
                    result["access_token"]
                )

                st.session_state["user"] = (
                    result["user"]
                )

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    st.stop()


# =========================================================
# AUTHENTICATED APPLICATION
# =========================================================

current_user = st.session_state["user"]
access_token = st.session_state["access_token"]

user_role = current_user.get("role", "")

PROCESSING_ROLES = [
    "admin",
    "finance_controller"
]


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)

with header_col1:

    st.title("💰 AI Finance Controller")

    st.subheader(
        "AI-powered financial control and invoice investigation system"
    )

with header_col2:

    st.write(
        f"👤 **{current_user['username']}**"
    )

    st.caption(
        f"Role: {current_user['role']}"
    )

    if st.button(
        "Logout",
        use_container_width=True
    ):
        logout()


st.divider()


# =========================================================
# AUTHENTICATED REQUEST HELPER
# =========================================================

AUTH_HEADERS = {
    "Authorization": f"Bearer {access_token}"
}


# =========================================================
# BACKEND CONNECTION
# =========================================================

try:

    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if response.status_code == 200:

        st.success(
            "🟢 Backend API is connected"
        )

    else:

        st.error(
            "🔴 Backend API returned an error"
        )

except requests.exceptions.RequestException:

    st.error(
        "🔴 Backend API is not running"
    )


st.divider()


# =========================================================
# ROLE INFORMATION
# =========================================================

if user_role == "finance_reviewer":

    st.info(
        "👀 **Reviewer Mode:** You have read-only access to "
        "financial analysis, exceptions, investigations, evidence, "
        "decisions, and audit history. Invoice upload, processing, "
        "and final decision submission are restricted."
    )


# =========================================================
# INVOICE UPLOAD
# =========================================================

if user_role in PROCESSING_ROLES:

    st.header("📤 Upload Invoice")

    uploaded_file = st.file_uploader(
        "Upload an invoice file",
        type=[
            "csv",
            "xlsx",
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "tiff",
            "bmp"
        ],
        help=(
            "Upload CSV, Excel, PDF, or image invoice files. "
            "PDF and image invoices are processed using OCR."
        )
    )

    if uploaded_file is not None:

        if st.button(
            "🚀 Upload & Validate Invoice"
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                file_extension = (
                    uploaded_file.name.lower().split(".")[-1]
                )


                # -------------------------------------------------
                # CSV / EXCEL INGESTION
                # -------------------------------------------------

                if file_extension in ["csv", "xlsx"]:

                    response = requests.post(
                        f"{API_URL}/ingestion/invoices",
                        files=files,
                        headers=AUTH_HEADERS,
                        timeout=30
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            result["message"]
                        )

                        st.write(
                            f"**File:** {result['file_name']}  \n"
                            f"**Records validated:** "
                            f"{result['record_count']}"
                        )

                        st.subheader(
                            "Validated Invoices"
                        )

                        st.dataframe(
                            result["invoices"],
                            use_container_width=True
                        )

                        st.session_state[
                            "validated_invoices"
                        ] = result["invoices"]

                        st.session_state[
                            "uploaded_file_name"
                        ] = uploaded_file.name

                        st.session_state[
                            "document_upload"
                        ] = False

                        st.session_state.pop(
                            "ocr_result",
                            None
                        )

                    elif response.status_code == 401:

                        st.error(
                            "❌ Your session has expired. "
                            "Please log in again."
                        )

                    elif response.status_code == 403:

                        st.error(
                            "❌ You do not have permission "
                            "to upload invoices."
                        )

                    else:

                        try:

                            error_detail = response.json().get(
                                "detail",
                                "Invoice upload failed."
                            )

                        except ValueError:

                            error_detail = (
                                "Invoice upload failed."
                            )

                        st.error(
                            f"❌ {error_detail}"
                        )


                # -------------------------------------------------
                # PDF / IMAGE OCR INGESTION
                # -------------------------------------------------

                else:

                    response = requests.post(
                        f"{API_URL}/ingestion/invoice-document",
                        files=files,
                        headers=AUTH_HEADERS,
                        timeout=60
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state[
                            "ocr_result"
                        ] = result

                        st.success(
                            result.get(
                                "message",
                                "Invoice document processed successfully."
                            )
                        )


                        # -------------------------------------------------
                        # OCR SUMMARY
                        # -------------------------------------------------

                        st.subheader(
                            "🔎 OCR Extraction Summary"
                        )

                        average_confidence = result.get(
                            "average_confidence"
                        )

                        review_required = result.get(
                            "review_required",
                            False
                        )

                        extraction_complete = result.get(
                            "extraction_complete",
                            False
                        )

                        summary_col1, summary_col2, summary_col3 = (
                            st.columns(3)
                        )

                        with summary_col1:

                            if average_confidence is not None:

                                st.metric(
                                    "OCR Confidence",
                                    f"{average_confidence:.2f}%"
                                )

                            else:

                                st.metric(
                                    "OCR Confidence",
                                    "N/A"
                                )

                        with summary_col2:

                            if extraction_complete:

                                st.success(
                                    "✅ Extraction Complete"
                                )

                            else:

                                st.warning(
                                    "⚠️ Incomplete Extraction"
                                )

                        with summary_col3:

                            if review_required:

                                st.warning(
                                    "⚠️ Manual Review Required"
                                )

                            else:

                                st.success(
                                    "✅ Review Not Required"
                                )


                        # -------------------------------------------------
                        # LOW CONFIDENCE FIELDS
                        # -------------------------------------------------

                        low_confidence_fields = result.get(
                            "low_confidence_fields",
                            []
                        )

                        if low_confidence_fields:

                            st.warning(
                                "⚠️ Some invoice fields have low OCR "
                                "confidence and should be manually verified."
                            )

                            st.write(
                                "**Fields requiring verification:**"
                            )

                            for field in low_confidence_fields:

                                st.write(
                                    f"• {field}"
                                )

                        elif review_required:

                            st.warning(
                                "⚠️ This invoice requires manual review "
                                "before financial processing."
                            )


                        # -------------------------------------------------
                        # OCR EXTRACTED TEXT
                        # -------------------------------------------------

                        st.subheader(
                            "📝 OCR Extracted Text"
                        )

                        extracted_text = result.get(
                            "extracted_text",
                            ""
                        )

                        st.text_area(
                            "Extracted invoice text",
                            extracted_text,
                            height=250
                        )


                        # -------------------------------------------------
                        # EXTRACTED INVOICE FIELDS
                        # -------------------------------------------------

                        st.subheader(
                            "📋 Extracted Invoice Fields"
                        )

                        parsed_fields = result.get(
                            "parsed_fields",
                            {}
                        )

                        if parsed_fields:

                            st.json(
                                parsed_fields
                            )

                        else:

                            st.info(
                                "No structured invoice fields were returned."
                            )


                        # -------------------------------------------------
                        # FIELD CONFIDENCE
                        # -------------------------------------------------

                        field_confidence = result.get(
                            "field_confidence",
                            {}
                        )

                        if field_confidence:

                            st.subheader(
                                "🎯 Field Confidence"
                            )

                            confidence_rows = []

                            for field_name, confidence in (
                                field_confidence.items()
                            ):

                                confidence_rows.append(
                                    {
                                        "Field": field_name,
                                        "Confidence": (
                                            f"{confidence:.2f}%"
                                            if isinstance(
                                                confidence,
                                                (int, float)
                                            )
                                            else str(confidence)
                                        )
                                    }
                                )

                            st.dataframe(
                                confidence_rows,
                                use_container_width=True,
                                hide_index=True
                            )


                        # -------------------------------------------------
                        # VALIDATION RESULT
                        # -------------------------------------------------

                        if result.get(
                            "validation_success"
                        ):

                            st.success(
                                "✅ Invoice successfully extracted "
                                "and validated."
                            )

                            invoice = result.get(
                                "invoice"
                            )

                            if invoice:

                                st.subheader(
                                    "🧾 Validated Invoice"
                                )

                                st.dataframe(
                                    [invoice],
                                    use_container_width=True,
                                    hide_index=True
                                )

                                st.session_state[
                                    "validated_invoices"
                                ] = [invoice]

                                st.session_state[
                                    "uploaded_file_name"
                                ] = uploaded_file.name

                                st.session_state[
                                    "document_upload"
                                ] = True

                        else:

                            st.warning(
                                "⚠️ Invoice could not be fully validated."
                            )

                            validation_error = result.get(
                                "validation_error"
                            )

                            if validation_error:

                                st.error(
                                    f"❌ {validation_error}"
                                )

                            missing_fields = parsed_fields.get(
                                "missing_fields",
                                []
                            )

                            if missing_fields:

                                st.info(
                                    "Missing fields: "
                                    + ", ".join(
                                        missing_fields
                                    )
                                )

                            st.session_state.pop(
                                "validated_invoices",
                                None
                            )

                    elif response.status_code == 401:

                        st.error(
                            "❌ Your session has expired. "
                            "Please log in again."
                        )

                    elif response.status_code == 403:

                        st.error(
                            "❌ You do not have permission "
                            "to upload invoice documents."
                        )

                    else:

                        try:

                            error_detail = response.json().get(
                                "detail",
                                "Invoice document processing failed."
                            )

                        except ValueError:

                            error_detail = (
                                "Invoice document processing failed."
                            )

                        st.error(
                            f"❌ {error_detail}"
                        )

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"❌ Could not connect to backend: {exc}"
                )


# =========================================================
# REVIEWER READ-ONLY UPLOAD AREA
# =========================================================

elif user_role == "finance_reviewer":

    st.header("📤 Invoice Upload")

    st.warning(
        "🔒 Invoice upload is restricted for Finance Reviewers."
    )

    st.caption(
        "Your role is read-only. You can review processed "
        "financial information from the other application pages."
    )


# =========================================================
# PROCESS INVOICE
# =========================================================

if (
    user_role in PROCESSING_ROLES
    and "validated_invoices" in st.session_state
):

    st.divider()

    st.header(
        "🔍 Process Invoice"
    )

    invoices = st.session_state[
        "validated_invoices"
    ]

    invoice_ids = [
        invoice["invoice_id"]
        for invoice in invoices
    ]

    selected_invoice = st.selectbox(
        "Select an invoice to process",
        invoice_ids
    )

    if st.button(
        "⚙️ Run Finance Controller"
    ):

        try:

            # -------------------------------------------------
            # DOCUMENT / OCR PROCESSING
            # -------------------------------------------------

            if st.session_state.get(
                "document_upload",
                False
            ):

                response = requests.post(
                    f"{API_URL}/invoices/"
                    f"{selected_invoice}/process-document",
                    params={
                        "file_name": st.session_state[
                            "uploaded_file_name"
                        ]
                    },
                    headers=AUTH_HEADERS,
                    timeout=60
                )


            # -------------------------------------------------
            # CSV / EXCEL PROCESSING
            # -------------------------------------------------

            else:

                response = requests.post(
                    f"{API_URL}/invoices/"
                    f"{selected_invoice}/process-from-data",
                    params={
                        "file_name": st.session_state[
                            "uploaded_file_name"
                        ]
                    },
                    headers=AUTH_HEADERS,
                    timeout=30
                )


            if response.status_code == 200:

                result = response.json()

                st.session_state[
                    "processed_result"
                ] = result

                st.session_state[
                    "selected_invoice_id"
                ] = selected_invoice

                st.success(
                    "✅ Invoice processed successfully."
                )

            elif response.status_code == 401:

                st.error(
                    "❌ Your session has expired. "
                    "Please log in again."
                )

            elif response.status_code == 403:

                st.error(
                    "❌ You do not have permission "
                    "to process invoices."
                )

            else:

                try:

                    error_detail = response.json().get(
                        "detail",
                        "Invoice processing failed."
                    )

                except ValueError:

                    error_detail = (
                        "Invoice processing failed."
                    )

                st.error(
                    f"❌ {error_detail}"
                )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"❌ Could not connect to backend: {exc}"
            )


# =========================================================
# FINANCE CONTROLLER RESULT
# =========================================================

if "processed_result" in st.session_state:

    result = st.session_state[
        "processed_result"
    ]

    invoice = result["invoice"]
    exceptions = result["exceptions"]
    risk = result["risk_result"]
    recommendation = result["recommendation"]

    st.divider()

    st.header(
        "📊 Finance Controller Result"
    )


    # -----------------------------------------------------
    # INVOICE INFORMATION
    # -----------------------------------------------------

    st.subheader(
        "🧾 Invoice Information"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Invoice",
            invoice["invoice_id"]
        )

    with col2:

        st.metric(
            "Vendor",
            invoice["vendor_id"]
        )

    with col3:

        st.metric(
            "Amount",
            f"₹{invoice['amount']:,.2f}"
        )

    with col4:

        st.metric(
            "Quantity",
            invoice["quantity"]
        )


    # -----------------------------------------------------
    # RISK ASSESSMENT
    # -----------------------------------------------------

    st.subheader(
        "⚠️ Risk Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Risk Score",
            risk["risk_score"]
        )

    with col2:

        if risk["risk_level"] == "Critical":

            st.error(
                f"🔴 {risk['risk_level']} Risk"
            )

        elif risk["risk_level"] == "High":

            st.warning(
                f"🟠 {risk['risk_level']} Risk"
            )

        else:

            st.info(
                f"🟢 {risk['risk_level']} Risk"
            )

    st.write(
        f"**Explanation:** "
        f"{risk['explanation']}"
    )


    # -----------------------------------------------------
    # EXCEPTIONS
    # -----------------------------------------------------

    st.subheader(
        "🚨 Detected Exceptions"
    )

    if exceptions:

        for exception in exceptions:

            st.warning(
                f"⚠️ **{exception['exception_type']}**  \n"
                f"{exception['description']}"
            )

    else:

        st.success(
            "✅ No financial control exceptions detected."
        )


    # -----------------------------------------------------
    # AI RECOMMENDATION
    # -----------------------------------------------------

    st.subheader(
        "🤖 AI Recommendation"
    )

    if recommendation["action"] == "Block Payment":

        st.error(
            f"""
### 🔴 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}

**Human Review:** Required
"""
        )

    elif recommendation["action"] == "Hold Payment":

        st.warning(
            f"""
### 🟠 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}
"""
        )

    else:

        st.success(
            f"""
### 🟢 {recommendation["action"]}

**Priority:** {recommendation["priority"]}

**Reason:** {recommendation["reason"]}
"""
        )


    # -----------------------------------------------------
    # RISK FACTORS
    # -----------------------------------------------------

    st.subheader(
        "📌 Risk Factors"
    )

    for factor in risk["risk_factors"]:

        st.write(
            f"• {factor}"
        )


    st.divider()

    st.info(
        "Human review is required before the final financial "
        "decision is made."
    )


# =========================================================
# ADMIN - USER MANAGEMENT
# =========================================================

if current_user["role"] == "admin":

    st.divider()

    st.header("👥 User Management")

    st.caption(
        "Admin-only area for managing finance system users and roles."
    )


    # -----------------------------------------------------
    # VIEW USERS
    # -----------------------------------------------------

    st.subheader("📋 Existing Users")

    try:

        users_response = requests.get(
            f"{API_URL}/users/",
            headers=AUTH_HEADERS,
            timeout=10
        )

        if users_response.status_code == 200:

            users = users_response.json()

            if users:

                display_users = [
                    {
                        "User ID": user["user_id"],
                        "Username": user["username"],
                        "Role": user["role"],
                        "Status": (
                            "Active"
                            if user["is_active"]
                            else "Inactive"
                        )
                    }
                    for user in users
                ]

                st.dataframe(
                    display_users,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No users found."
                )

        elif users_response.status_code == 403:

            st.error(
                "❌ You do not have permission to view users."
            )

        elif users_response.status_code == 401:

            st.error(
                "❌ Your session has expired. "
                "Please log in again."
            )

        else:

            st.error(
                "❌ Failed to load users."
            )

    except requests.exceptions.RequestException as exc:

        st.error(
            f"❌ Could not connect to backend: {exc}"
        )


    # -----------------------------------------------------
    # CREATE USER
    # -----------------------------------------------------

    st.subheader("➕ Create New User")

    with st.form("create_user_form"):

        new_username = st.text_input(
            "Username",
            placeholder="e.g. reviewer1"
        )

        new_password = st.text_input(
            "Temporary Password",
            type="password",
            help="Password must contain at least 8 characters."
        )

        new_role = st.selectbox(
            "Assign Role",
            [
                "finance_controller",
                "finance_reviewer",
                "auditor"
            ]
        )

        create_user_button = st.form_submit_button(
            "Create User",
            use_container_width=True
        )


    if create_user_button:

        if not new_username.strip():

            st.warning(
                "Please enter a username."
            )

        elif len(new_password) < 8:

            st.warning(
                "Password must contain at least 8 characters."
            )

        else:

            try:

                create_response = requests.post(
                    f"{API_URL}/users/",
                    json={
                        "username": new_username.strip(),
                        "password": new_password,
                        "role": new_role
                    },
                    headers=AUTH_HEADERS,
                    timeout=10
                )

                if create_response.status_code == 200:

                    result = create_response.json()

                    st.success(
                        f"✅ User '{new_username.strip()}' "
                        f"created successfully."
                    )

                    st.json(
                        result["user"]
                    )

                    st.rerun()

                elif create_response.status_code == 409:

                    st.error(
                        "❌ Username already exists."
                    )

                elif create_response.status_code == 401:

                    st.error(
                        "❌ Your session has expired. "
                        "Please log in again."
                    )

                elif create_response.status_code == 403:

                    st.error(
                        "❌ You do not have permission "
                        "to create users."
                    )

                else:

                    try:

                        error_detail = create_response.json().get(
                            "detail",
                            "User creation failed."
                        )

                    except ValueError:

                        error_detail = (
                            "User creation failed."
                        )

                    st.error(
                        f"❌ {error_detail}"
                    )

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"❌ Could not connect to backend: {exc}"
                )