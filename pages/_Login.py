import streamlit as st

from auth import register_user, login_user


st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)


st.title("🔐 Login / Register")


tab1, tab2 = st.tabs([
    "Login",
    "Register"
])


# ==========================
# LOGIN
# ==========================

with tab1:

    st.subheader("Login")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", type="primary"):

        user = login_user(
            email,
            password
        )

        if user:

            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user["id"]
            st.session_state["name"] = user["name"]
            st.session_state["role"] = user["role"]

            st.success(
                f"Welcome {user['name']}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid email or password."
            )


# ==========================
# REGISTER
# ==========================

with tab2:

    st.subheader("Create Account")

    name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    phone = st.text_input(
        "Phone Number"
    )

    address = st.text_area(
        "Address"
    )

    role = st.selectbox(
        "Account Type",
        [
            "Donor",
            "Receiver"
        ]
    )

    if st.button("Register"):

        if not name or not email or not password:

            st.warning(
                "Please fill all required fields."
            )

        else:

            success, message = register_user(
                name,
                email,
                password,
                phone,
                role.lower(),
                address
            )

            if success:

                st.success(message)

            else:

                st.error(message)
