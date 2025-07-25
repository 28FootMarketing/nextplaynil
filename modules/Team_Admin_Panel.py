import json
import streamlit as st
from datetime import datetime
import os

LOG_FILE = "./logs/role_change_log.jsonl"

def log_role_change(email, old_role, new_role):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "email": email,
        "old_role": old_role,
        "new_role": new_role,
        "event": "role_change"
    }
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

def role_editor():
    st.subheader("🔐 Role & Access Manager")

    # Load the existing roles
    with open("./data/user_roles.json", "r") as f:
        user_roles = json.load(f)

    editable_roles = {}

    for email, role_data in user_roles.items():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.text(email)
        with col2:
            role_options = ["admin", "coach", "athlete", "guest"]
            current_role = role_data.get("role", "guest")
            default_index = role_options.index(current_role) if current_role in role_options else role_options.index("guest")

            new_role = st.selectbox(
                "Role",
                role_options,
                index=default_index,
                key=email
            )
            editable_roles[email] = new_role

    # Save button
    if st.button("💾 Save Role Changes"):
        for email, new_role in editable_roles.items():
            old_role = user_roles[email].get("role", "guest")
            if old_role != new_role:
                user_roles[email]["role"] = new_role
                log_role_change(email, old_role, new_role)
        with open("./data/user_roles.json", "w") as f:
            json.dump(user_roles, f, indent=4)
        st.success("Roles updated successfully.")
