import streamlit as st
import requests
import pandas as pd
import base64
import json

BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Risk Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styling for badges / cards / login screen
st.markdown("""
<style>
.badge {
    display: inline-block;
    padding: 4px 13px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    color: white;
    margin-left: 6px;
    white-space: nowrap;
}
.risk-meta {
    color: #888;
    font-size: 0.85rem;
    margin-top: -8px;
}
.login-hero {
    text-align: center;
    margin-top: 20px;
    margin-bottom: 6px;
}
.login-hero h1 {
    font-size: 2.1rem;
    margin-bottom: 0;
}
.login-hero p {
    color: #888;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
PRIORITIES = ["Critical", "High", "Medium", "Low"]
STATUSES   = ["Open", "In Progress", "Mitigated", "Monitoring"]
TYPES      = ["Security", "Infrastructure", "Operational", "Compliance", "External"]
ROLES      = ["Admin", "Manager", "Employee"]

PRIORITY_COLORS = {"Critical": "#dc2626", "High": "#ea580c", "Medium": "#d97706", "Low": "#16a34a"}
STATUS_COLORS   = {"Open": "#2563eb", "In Progress": "#d97706", "Mitigated": "#16a34a", "Monitoring": "#7c3aed"}
ROLE_COLORS      = {"Admin": "#dc2626", "Manager": "#d97706", "Employee": "#16a34a"}
LOG_LEVEL_COLORS = {"ERROR": "#dc2626", "WARNING": "#d97706", "INFO": "#16a34a", "DEBUG": "#2563eb"}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def api(method, path, **kwargs):
    """Central API caller — attaches auth header automatically."""
    headers = kwargs.pop("headers", {})
    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state['token']}"
    try:
        resp = getattr(requests, method)(f"{BASE}{path}", headers=headers, **kwargs)
        return resp
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot reach FastAPI server. Is it running on port 8000?")
        return None

def show_response(resp):
    """Display API response using only what the backend actually returned — no fixed extra lines."""
    if resp is None:
        return
    if resp.status_code in (200, 201):
        try:
            data = resp.json()
        except Exception:
            if resp.text:
                st.success(resp.text)
            return
        if isinstance(data, (dict, list)):
            st.json(data)
        else:
            st.success(str(data))
    elif resp.status_code == 401:
        st.error("⛔ Session expired. Please logout and login again.")
    elif resp.status_code == 403:
        st.error("⛔ You are not authorized to perform this action.")
    elif resp.status_code == 404:
        try:
            st.warning(resp.json().get("detail", "Not found."))
        except Exception:
            st.warning("Not found.")
    else:
        st.error(f"Error {resp.status_code}: {resp.text}")

def is_admin():
    return st.session_state.get('role') == 'Admin'

def is_manager_or_above():
    return st.session_state.get('role') in ('Admin', 'Manager')

def badge_html(text, color):
    return f'<span class="badge" style="background-color:{color};">{text}</span>'

def extract_person(value):
    if isinstance(value, dict):
        return (value.get('user_name') or '-', value.get('user_role') or '', value.get('user_email') or '')
    return (value or 'Not Assigned', '', '')

def decode_token(token):
    """Decode a JWT's payload (email + role) locally, without needing a backend call."""
    try:
        payload_b64 = token.split('.')[1]
        padding = '=' * (-len(payload_b64) % 4)
        payload_json = base64.urlsafe_b64decode(payload_b64 + padding)
        return json.loads(payload_json)
    except Exception:
        return {}

def render_risk_card(risk):
    priority = risk.get('risk_priority') or '-'
    status = risk.get('risk_status') or '-'
    p_color = PRIORITY_COLORS.get(priority, '#6b7280')
    s_color = STATUS_COLORS.get(status, '#6b7280')

    with st.container(border=True):
        top_l, top_r = st.columns([4, 2])
        with top_l:
            title = risk.get('risk_title') or ('Risk #' + str(risk.get('risk_id')))
            st.markdown('#### ' + str(title))
            meta = str(risk.get('risk_id')) + ' | ' + str(risk.get('risk_type') or '-') + ' | ' + str(risk.get('risk_category') or '-')
            st.markdown(f'<div class="risk-meta">ID #{meta}</div>', unsafe_allow_html=True)
        with top_r:
            badges = badge_html(priority, p_color) + badge_html(status, s_color)
            st.markdown(f'<div style="text-align:right; margin-top:6px;">{badges}</div>', unsafe_allow_html=True)

        st.write(risk.get('risk_description') or '_No description provided._')

        st.markdown('---')
        c1, c2, c3, c4 = st.columns(4)
        creator_name, creator_role, _ = extract_person(risk.get('created_by'))
        alloc_name, alloc_role, _ = extract_person(risk.get('risk_allocation'))
        assign_name, assign_role, _ = extract_person(risk.get('assigned_to'))

        with c1:
            st.caption('Created By')
            st.markdown('**' + creator_name + '**')
            if creator_role:
                st.caption(creator_role)
        with c2:
            st.caption('Allocated To')
            st.markdown('**' + alloc_name + '**')
            if alloc_role:
                st.caption(alloc_role)
        with c3:
            st.caption('Assigned To')
            st.markdown('**' + assign_name + '**')
            if assign_role:
                st.caption(assign_role)
        with c4:
            st.caption('Due Date')
            st.markdown('**' + str(risk.get('due_date') or '-') + '**')

def render_user_card(user):
    role = user.get('user_role') or '-'
    r_color = ROLE_COLORS.get(role, '#6b7280')

    with st.container(border=True):
        top_l, top_r = st.columns([4, 2])
        with top_l:
            st.markdown('#### ' + str(user.get('user_name') or '-'))
            st.markdown(f'<div class="risk-meta">ID #{user.get("user_id")}</div>', unsafe_allow_html=True)
        with top_r:
            st.markdown(f'<div style="text-align:right; margin-top:6px;">{badge_html(role, r_color)}</div>', unsafe_allow_html=True)

        st.markdown('---')
        c1, c2 = st.columns(2)
        with c1:
            st.caption('Email')
            st.markdown('**' + str(user.get('user_email') or '-') + '**')
        with c2:
            st.caption('User ID')
            st.markdown('**' + str(user.get('user_id') or '-') + '**')

def parse_log_line(line):
    parts = line.split(' - ', 4)
    if len(parts) == 5:
        timestamp, level, name, func, message = parts
    elif len(parts) == 4:
        timestamp, level, name, message = parts
        func = ''
    else:
        timestamp, level, name, func, message = '-', 'OTHER', '-', '-', line
    return timestamp.strip(), level.strip(), name.strip(), func.strip(), message.strip()

def render_log_card(line):
    timestamp, level, name, func, message = parse_log_line(line)
    level_key = level.upper()
    color = LOG_LEVEL_COLORS.get(level_key, '#6b7280')

    with st.container(border=True):
        top_l, top_r = st.columns([4, 2])
        with top_l:
            st.markdown('#### ' + (func or name or 'Log Entry'))
            meta = name + (' | ' + func if func else '')
            st.markdown(f'<div class="risk-meta">{meta}</div>', unsafe_allow_html=True)
        with top_r:
            st.markdown(f'<div style="text-align:right; margin-top:6px;">{badge_html(level_key, color)}</div>', unsafe_allow_html=True)

        st.write(message or '_No message._')
        st.caption('🕒 ' + timestamp)

def render_login_page():
    top_l, top_r = st.columns([5, 1.4])
    with top_r:
        if st.button('➕ Add Default Values', key='login_add_defaults', use_container_width=True):
            resp = None
            try:
                with st.spinner('Please wait...'):
                    resp = requests.get(f'{BASE}/default')
            except requests.exceptions.ConnectionError:
                st.error('Cannot reach FastAPI server. Is it running on port 8000?')

            show_response(resp)

    st.markdown(
        '<div class="login-hero"><h1>Risk Management System</h1><p>Sign in to manage risks, users and more.</p></div>',
        unsafe_allow_html=True
    )

    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        with st.container(border=True):
            st.markdown('### Sign In')
            email = st.text_input('Email', placeholder='you@example.com', key='login_email')
            password = st.text_input('Password', type='password', placeholder='********', key='login_password')

            login_clicked = st.button('Login', use_container_width=True, type='primary')

            if login_clicked:
                if not email or not password:
                    st.warning('Please enter both email and password.')
                else:
                    resp = None
                    try:
                        with st.spinner('Signing in...'):
                            resp = requests.post(f'{BASE}/login', data={'username': email, 'password': password})
                    except requests.exceptions.ConnectionError:
                        st.error('Cannot reach FastAPI server. Is it running on port 8000?')

                    if resp is not None:
                        if resp.status_code == 200:
                            token = resp.json()['access_token']
                            st.session_state['token'] = token
                            st.session_state['logged_in'] = True

                            claims = decode_token(token)
                            st.session_state['user_email'] = claims.get('sub', email)
                            st.session_state['role'] = claims.get('role', 'Employee')
                            st.rerun()
                        else:
                            st.error('Invalid email or password. Please try again.')

        st.caption("Contact your administrator if you don't have an account.")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ Risk Management\nSystem")
    st.divider()

    # ── NOT LOGGED IN ────────────────────────
    if not st.session_state.get("logged_in"):
        st.info("🔒 Please sign in to continue.")

    # ── LOGGED IN ────────────────────────────
    else:
        role  = st.session_state.get("role", "")
        email = st.session_state.get("user_email", "")

        badge = {"Admin": "🔴 Admin", "Manager": "🟡 Manager", "Employee": "🟢 Employee"}.get(role, role)
        st.success(f"**{email}**\n\n{badge}")
        st.divider()

        # Role-based page list
        pages = ["🤖 RiskBot"]
        if is_manager_or_above():
            pages.append("📋 Risks")
        if is_admin():
            pages.append("👥 Users")
            pages.append("📄 Logs")
        pages.append("ℹ️ System")

        page = st.radio("Navigation", pages, label_visibility="collapsed")
        st.session_state["page"] = page

        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ─────────────────────────────────────────────
# GUARD
# ─────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    render_login_page()
    st.stop()

page = st.session_state.get("page", "🤖 RiskBot")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — RISKBOT
# ══════════════════════════════════════════════════════════════════════════════
if page == "🤖 RiskBot":
    st.title("🤖 RiskBot")
    st.caption("Your AI assistant for risk management. Ask anything in plain language.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Render history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask RiskBot anything...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("RiskBot is thinking..."):
            resp = api("post", "/chatbot/", params={"message": user_input})

        if resp and resp.status_code == 200:
            bot_reply = resp.json()
        elif resp and resp.status_code == 401:
            bot_reply = "⚠️ Session expired. Please logout and login again."
        elif resp:
            bot_reply = f"⚠️ Error {resp.status_code}: {resp.text}"
        else:
            bot_reply = "⚠️ Could not reach the server."

        st.session_state["messages"].append({"role": "assistant", "content": str(bot_reply)})
        with st.chat_message("assistant"):
            st.write(bot_reply)

    # Clear chat button
    if st.session_state.get("messages"):
        if st.button("🗑️ Clear Chat", use_container_width=False):
            st.session_state["messages"] = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — RISKS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Risks":
    st.title("📋 Risk Management")

    t_all, t_by_id, t_add, t_update, t_delete = st.tabs([
        "📂 View All", "🔍 View by ID", "➕ Add Risk", "✏️ Update Risk", "🗑️ Delete Risk"
    ])

    # ── View All ─────────────────────────────
    with t_all:
        st.subheader("All Risks")
        if st.button("🔄 Load Risks", use_container_width=True, key="load_risks"):
            resp = api("get", "/risk")
            if resp and resp.status_code == 200:
                st.session_state["all_risks"] = resp.json() or []
            elif resp:
                show_response(resp)
                st.session_state["all_risks"] = []

        risks_data = st.session_state.get("all_risks", [])
        if risks_data:
            fc1, fc2 = st.columns(2)
            with fc1:
                f_priority = st.selectbox("Filter by Priority", ["All"] + PRIORITIES, key="filter_priority")
            with fc2:
                f_status = st.selectbox("Filter by Status", ["All"] + STATUSES, key="filter_status")

            filtered = [
                r for r in risks_data
                if (f_priority == "All" or r.get("risk_priority") == f_priority)
                and (f_status == "All" or r.get("risk_status") == f_status)
            ]

            st.caption(f"Showing **{len(filtered)}** of **{len(risks_data)}** risk(s)")
            if filtered:
                for r in filtered:
                    render_risk_card(r)
            else:
                st.info("No risks match the selected filters.")
        elif "all_risks" in st.session_state:
            st.info("No risks found.")

    # ── View by ID ───────────────────────────
    with t_by_id:
        st.subheader("View Risk by ID")
        risk_id = st.number_input("Risk ID", min_value=1, step=1, key="view_risk_id")
        if st.button("🔍 Fetch", use_container_width=True, key="fetch_risk"):
            resp = api("get", "/risk/id", params={"risk_id": int(risk_id)})
            if resp and resp.status_code == 200:
                render_risk_card(resp.json())
            else:
                show_response(resp)

    # ── Add Risk ─────────────────────────────
    with t_add:
        st.subheader("Add New Risk")
        with st.form("form_add_risk"):
            col1, col2 = st.columns(2)
            with col1:
                a_title       = st.text_input("Title", placeholder="Optional short title")
                a_desc        = st.text_area("Description *")
                a_priority    = st.selectbox("Priority *", PRIORITIES)
                a_status      = st.selectbox("Status *", STATUSES)
                a_type        = st.selectbox("Type *", TYPES)
            with col2:
                a_category    = st.text_input("Category *", placeholder="e.g. Authentication, CI/CD")
                a_created_by  = st.number_input("Created By — User ID *", min_value=1, step=1)
                a_allocation  = st.number_input("Allocated To — Manager ID *", min_value=1, step=1)
                a_assigned    = st.number_input("Assigned To — Employee ID *", min_value=1, step=1)
                a_due         = st.date_input("Due Date *")

            if st.form_submit_button("➕ Add Risk", use_container_width=True, type="primary"):
                if not a_desc or not a_category:
                    st.error("Description and Category are required.")
                else:
                    payload = {
                        "risk_title":       a_title or None,
                        "risk_description": a_desc,
                        "risk_priority":    a_priority,
                        "risk_status":      a_status,
                        "risk_type":        a_type,
                        "risk_category":    a_category,
                        "created_by":       int(a_created_by),
                        "risk_allocation":  int(a_allocation),
                        "assigned_to":      int(a_assigned),
                        "due_date":         str(a_due),
                    }
                    resp = api("post", "/risk/add_risk", json=payload)
                    show_response(resp)

    # ── Update Risk ──────────────────────────
    with t_update:
        st.subheader("Update Risk")
        st.caption("Load a risk's current details, then edit whatever needs to change. Fields you leave as-is are saved unchanged.")

        lc1, lc2 = st.columns([3, 1])
        with lc1:
            u_risk_id = st.number_input("Risk ID to Update *", min_value=1, step=1, key="update_risk_id")
        with lc2:
            st.write("")
            st.write("")
            if st.button("🔍 Load Details", use_container_width=True, key="load_update_risk"):
                resp = api("get", "/risk/id", params={"risk_id": int(u_risk_id)})
                if resp and resp.status_code == 200:
                    st.session_state["update_risk_data"] = resp.json()
                    st.session_state["update_risk_data_id"] = int(u_risk_id)
                else:
                    st.session_state["update_risk_data"] = None
                    show_response(resp)

        risk_data  = st.session_state.get("update_risk_data")
        loaded_rid = st.session_state.get("update_risk_data_id")

        if risk_data and loaded_rid == int(u_risk_id):
            def _opt_index(options, value):
                return options.index(value) + 1 if value in options else 0

            def _person_id(value):
                return value.get("user_id") if isinstance(value, dict) else None

            try:
                due_default = pd.to_datetime(risk_data.get("due_date")).date()
            except Exception:
                due_default = pd.Timestamp.now().date()

            with st.form("form_update_risk"):
                col1, col2 = st.columns(2)
                with col1:
                    u_title    = st.text_input("Title",       value=risk_data.get("risk_title") or "")
                    u_desc     = st.text_area("Description",  value=risk_data.get("risk_description") or "")
                    u_priority = st.selectbox("Priority", ["— no change —"] + PRIORITIES,
                                               index=_opt_index(PRIORITIES, risk_data.get("risk_priority")))
                    u_status   = st.selectbox("Status", ["— no change —"] + STATUSES,
                                               index=_opt_index(STATUSES, risk_data.get("risk_status")))
                    u_type     = st.selectbox("Type", ["— no change —"] + TYPES,
                                               index=_opt_index(TYPES, risk_data.get("risk_type")))
                with col2:
                    u_category = st.text_input("Category", value=risk_data.get("risk_category") or "")
                    u_c_by     = st.number_input("Created By — User ID", min_value=1, step=1,
                                                  value=int(_person_id(risk_data.get("created_by")) or 1))
                    u_alloc    = st.number_input("Allocated To — Manager ID", min_value=1, step=1,
                                                  value=int(_person_id(risk_data.get("risk_allocation")) or 1))
                    u_assign   = st.number_input("Assigned To — Employee ID", min_value=1, step=1,
                                                  value=int(_person_id(risk_data.get("assigned_to")) or 1))
                    u_due      = st.date_input("Due Date", value=due_default)

                if st.form_submit_button("✏️ Update Risk", use_container_width=True, type="primary"):
                    payload = {
                        "risk_title":       u_title or None,
                        "risk_description": u_desc,
                        "risk_priority":    None if u_priority == "— no change —" else u_priority,
                        "risk_status":      None if u_status == "— no change —" else u_status,
                        "risk_type":        None if u_type == "— no change —" else u_type,
                        "risk_category":    u_category,
                        "created_by":       int(u_c_by),
                        "risk_allocation":  int(u_alloc),
                        "assigned_to":      int(u_assign),
                        "due_date":         str(u_due),
                    }
                    payload = {k: v for k, v in payload.items() if v is not None}
                    resp = api("post", "/risk/update_risk",
                               params={"risk_id": int(loaded_rid)}, json=payload)
                    show_response(resp)
                    st.session_state["update_risk_data"] = None
        else:
            st.info("Enter a Risk ID above and click **Load Details** to see and edit its current values.")

    # ── Delete Risk ──────────────────────────
    with t_delete:
        st.subheader("Delete Risk")
        st.warning("⚠️ This is permanent and cannot be undone.")
        with st.form("form_delete_risk"):
            d_risk_id = st.number_input("Risk ID to Delete *", min_value=1, step=1)
            confirm   = st.checkbox("Yes, I want to permanently delete this risk.")
            if st.form_submit_button("🗑️ Delete Risk", use_container_width=True):
                if not confirm:
                    st.error("Please check the confirmation box first.")
                else:
                    resp = api("post", "/risk/delete_risk", params={"risk_id": int(d_risk_id)})
                    show_response(resp)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — USERS  (Admin only)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Users":
    st.title("👥 User Management")

    t_all, t_by_id, t_add, t_update, t_delete = st.tabs([
        "📂 View All", "🔍 View by ID", "➕ Add User", "✏️ Update User", "🗑️ Delete User"
    ])

    # ── View All ─────────────────────────────
    with t_all:
        st.subheader("All Users")
        if st.button("🔄 Load Users", use_container_width=True, key="load_users"):
            resp = api("get", "/user/")
            if resp and resp.status_code == 200:
                st.session_state["all_users"] = resp.json() or []
            elif resp:
                show_response(resp)
                st.session_state["all_users"] = []

        users_data = st.session_state.get("all_users", [])
        if users_data:
            f_role = st.selectbox("Filter by Role", ["All"] + ROLES, key="filter_user_role")

            filtered_users = [
                u for u in users_data
                if f_role == "All" or u.get("user_role") == f_role
            ]

            st.caption(f"Showing **{len(filtered_users)}** of **{len(users_data)}** user(s)")
            if filtered_users:
                for u in filtered_users:
                    render_user_card(u)
            else:
                st.info("No users match the selected filter.")
        elif "all_users" in st.session_state:
            st.info("No users found.")

    # ── View by ID ───────────────────────────
    with t_by_id:
        st.subheader("View User by ID")
        user_id = st.number_input("User ID", min_value=1, step=1, key="view_user_id")
        if st.button("🔍 Fetch", use_container_width=True, key="fetch_user"):
            resp = api("get", "/user/show_by_id", params={"user_id": int(user_id)})
            if resp and resp.status_code == 200:
                render_user_card(resp.json())
            else:
                show_response(resp)

    # ── Add User ─────────────────────────────
    with t_add:
        st.subheader("Add New User")
        with st.form("form_add_user"):
            a_name     = st.text_input("Full Name *")
            a_email    = st.text_input("Email *")
            a_password = st.text_input("Password *", type="password")
            a_role     = st.selectbox("Role *", ROLES)
            if st.form_submit_button("➕ Add User", use_container_width=True, type="primary"):
                if not a_name or not a_email or not a_password:
                    st.error("Name, Email, and Password are required.")
                else:
                    payload = {
                        "user_name":     a_name,
                        "user_email":    a_email,
                        "user_password": a_password,
                        "user_role":     a_role,
                    }
                    resp = api("post", "/user/add_user", json=payload)
                    show_response(resp)

    # ── Update User ──────────────────────────
    with t_update:
        st.subheader("Update User")
        st.caption("Load a user's current details, then edit whatever needs to change.")

        lc1, lc2 = st.columns([3, 1])
        with lc1:
            u_user_id = st.number_input("User ID to Update *", min_value=1, step=1, key="update_user_id")
        with lc2:
            st.write("")
            st.write("")
            if st.button("🔍 Load Details", use_container_width=True, key="load_update_user"):
                resp = api("get", "/user/show_by_id", params={"user_id": int(u_user_id)})
                if resp and resp.status_code == 200:
                    st.session_state["update_user_data"] = resp.json()
                    st.session_state["update_user_data_id"] = int(u_user_id)
                else:
                    st.session_state["update_user_data"] = None
                    show_response(resp)

        user_data  = st.session_state.get("update_user_data")
        loaded_uid = st.session_state.get("update_user_data_id")

        if user_data and loaded_uid == int(u_user_id):
            role_options  = ["— no change —"] + ROLES
            current_role  = user_data.get("user_role")
            role_index    = role_options.index(current_role) if current_role in role_options else 0

            with st.form("form_update_user"):
                u_name     = st.text_input("Name",  value=user_data.get("user_name") or "")
                u_email    = st.text_input("Email", value=user_data.get("user_email") or "")
                u_password = st.text_input("New Password", placeholder="leave blank to keep the current password", type="password")
                u_role     = st.selectbox("Role", role_options, index=role_index)

                if st.form_submit_button("✏️ Update User", use_container_width=True, type="primary"):
                    payload = {
                        "user_name":  u_name,
                        "user_email": u_email,
                        "user_role":  None if u_role == "— no change —" else u_role,
                    }
                    if u_password:
                        payload["user_password"] = u_password
                    payload = {k: v for k, v in payload.items() if v is not None}

                    resp = api("put", "/user/update_user",
                               params={"user_id": int(loaded_uid)}, json=payload)
                    show_response(resp)
                    st.session_state["update_user_data"] = None
        else:
            st.info("Enter a User ID above and click **Load Details** to see and edit its current values.")

    # ── Delete User ──────────────────────────
    with t_delete:
        st.subheader("Delete User")
        st.warning("⚠️ This is permanent and cannot be undone.")
        with st.form("form_delete_user"):
            d_user_id = st.number_input("User ID to Delete *", min_value=1, step=1)
            confirm   = st.checkbox("Yes, I want to permanently delete this user.")
            if st.form_submit_button("🗑️ Delete User", use_container_width=True):
                if not confirm:
                    st.error("Please check the confirmation box first.")
                else:
                    resp = api("delete", "/user/delete_user", params={"user_id": int(d_user_id)})
                    show_response(resp)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — LOGS  (Admin only)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Logs":
    st.title("📄 Activity Logs")
    st.caption("Full system activity log. Admin eyes only.")

    col_btn, col_search, col_level = st.columns([1, 2, 1])
    with col_btn:
        load = st.button("🔄 Load Logs", use_container_width=True, type="primary")
    with col_search:
        search = st.text_input("Filter", placeholder="Type keyword to filter log lines...",
                               label_visibility="collapsed")
    with col_level:
        level_filter = st.selectbox("Level", ["All", "INFO", "WARNING", "ERROR"],
                                    label_visibility="collapsed")

    if load:
        st.session_state["raw_logs"] = None
        resp = api("get", "/logs")
        if resp and resp.status_code == 200:
            st.session_state["raw_logs"] = resp.json()
        elif resp:
            show_response(resp)

    if st.session_state.get("raw_logs"):
        raw   = st.session_state["raw_logs"]
        lines = [l for l in raw.strip().split("\n") if l.strip()]
        lines.reverse()  # newest first

        if search:
            lines = [l for l in lines if search.lower() in l.lower()]
        if level_filter != "All":
            lines = [l for l in lines if level_filter in l]

        st.caption(f"Showing **{len(lines)}** entries"
                   + (f' matching "{search}"' if search else ""))

        max_show = 200
        for line in lines[:max_show]:
            render_log_card(line)
        if len(lines) > max_show:
            st.info(f"Showing the most recent {max_show} of {len(lines)} matching entries. Refine your filter to narrow this down.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ System":
    st.title("ℹ️ System")

    t_intro, t_me, t_seed = st.tabs(["About", "Who Am I", "Seed Default Data"])

    with t_intro:
        st.subheader("About This System")
        if st.button("🔍 Load Info", use_container_width=True):
            resp = requests.get(f"{BASE}/")
            if resp and resp.status_code == 200:
                info = resp.json()
                with st.container(border=True):
                    st.markdown('#### ' + str(info.get('Message', 'Risk Management System')))
                    st.markdown('---')
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.caption('Created By')
                        st.markdown('**' + str(info.get('Created_By', '-')) + '**')
                    with c2:
                        st.caption('Created On')
                        st.markdown('**' + str(info.get('On', '-')) + '**')
                    with c3:
                        st.caption('Organization')
                        st.markdown('**' + str(info.get('At', '-')) + '**')
                    st.caption('During')
                    st.markdown('**' + str(info.get('During', '-')) + '**')
            else:
                show_response(resp)

    with t_me:
        st.subheader("Current Session")
        if st.button("👤 Who Am I?", use_container_width=True):
            claims = decode_token(st.session_state.get('token', ''))
            email = claims.get('sub', st.session_state.get('user_email', '-'))
            role  = claims.get('role', st.session_state.get('role', '-'))
            st.info(f"Logged in as **{email}** — role: **{role}**")

    with t_seed:
        st.subheader("Seed Default Data")
        st.warning("⚠️ Adds 8 default users and 8 sample risks. Use only on a fresh/empty database.")
        with st.form("form_seed"):
            confirm_seed = st.checkbox("I understand this will insert default records into the database.")
            if st.form_submit_button("🌱 Seed Database", use_container_width=True):
                if not confirm_seed:
                    st.error("Please check the confirmation box first.")
                else:
                    resp = requests.get(f"{BASE}/default")
                    show_response(resp)