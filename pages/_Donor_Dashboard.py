import streamlit as st
import sqlite3
from datetime import datetime

from database import get_connection


st.set_page_config(
    page_title="Donor Dashboard",
    page_icon="🍽️",
    layout="wide"
)


# Check login
if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.stop()


if st.session_state.get("role") != "donor":

    st.error(
        "Only donors can access this page."
    )

    st.stop()


st.title("🍽️ Donor Dashboard")

st.write(
    f"Welcome, **{st.session_state['name']}**!"
)


st.divider()


# ==========================
# ADD FOOD DONATION
# ==========================

st.header("➕ Add Food Donation")


with st.form("donation_form"):

    food_name = st.text_input(
        "Food Name"
    )

    description = st.text_area(
        "Description"
    )

    col1, col2 = st.columns(2)

    with col1:

        quantity = st.number_input(
            "Quantity",
            min_value=0.1,
            step=0.5
        )

    with col2:

        unit = st.selectbox(
            "Unit",
            [
                "kg",
                "liters",
                "packets",
                "plates"
            ]
        )

    expiry_time = st.datetime_input(
        "Expiry Date & Time",
        value=datetime.now()
    )

    pickup_address = st.text_area(
        "Pickup Address"
    )

    submit = st.form_submit_button(
        "Donate Food 🍱"
    )


if submit:

    if not food_name or not pickup_address:

        st.error(
            "Please enter food name and pickup address."
        )

    else:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO donations
            (
                donor_id,
                food_name,
                description,
                quantity,
                unit,
                expiry_time,
                pickup_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            st.session_state["user_id"],
            food_name,
            description,
            quantity,
            unit,
            expiry_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            pickup_address
        ))

        connection.commit()
        connection.close()

        st.success(
            "Food donation added successfully! 🎉"
        )


# ==========================
# MY DONATIONS
# ==========================

st.divider()

st.header("📦 My Donations")


connection = get_connection()

donations = connection.execute("""
    SELECT *
    FROM donations
    WHERE donor_id = ?
    ORDER BY created_at DESC
""", (
    st.session_state["user_id"],
)).fetchall()

connection.close()


if donations:

    for donation in donations:

        with st.container(border=True):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.subheader(
                    f"🍱 {donation['food_name']}"
                )

                st.write(
                    donation["description"]
                )

            with col2:

                st.write(
                    f"**Quantity:** "
                    f"{donation['quantity']} "
                    f"{donation['unit']}"
                )

                st.write(
                    f"**Expiry:** "
                    f"{donation['expiry_time']}"
                )

            with col3:

                st.write(
                    f"**Status:** "
                    f"{donation['status']}"
                )

else:

    st.info(
        "You haven't added any donations yet."
    )
