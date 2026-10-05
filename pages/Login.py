import streamlit as st
from auth import register_user, login_user

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")
st.title("🔐 Login / Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", type="primary"):
        user = login_user(email.strip(), password)
        if user:
            st.session_state.update(logged_in=True, user_id=user['id'], name=user['name'], role=user['role'])
            st.success(f"Welcome {user['name']}!")
            st.rerun()
        else:
            st.error("Invalid email or password.")

with tab2:
    st.subheader("Create Account")
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm = st.text_input("Confirm Password", type="password", key="confirm_password")
    phone = st.text_input("Phone Number", key="reg_phone")
    address = st.text_area("Address", key="reg_address")
    role = st.selectbox("Account Type", ["Donor", "Receiver"], key="reg_role")
    if st.button("Register"):
        if not name.strip() or not email.strip() or not password:
            st.warning("Please fill all required fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            success, message = register_user(name.strip(), email.strip().lower(), password, phone.strip(), role.lower(), address.strip())
            (st.success if success else st.error)(message)
