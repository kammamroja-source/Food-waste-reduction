import streamlit as st
from datetime import datetime
from database import get_connection

st.set_page_config(page_title="Donor Dashboard", page_icon="🍽️", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "donor":
    st.error("Only donors can access this page.")
    st.stop()

st.title("🍽️ Donor Dashboard")
st.write(f"Welcome, **{st.session_state['name']}**!")
st.divider()

st.header("➕ Add Food Donation")
with st.form("donation_form"):
    food_name = st.text_input("Food Name")
    description = st.text_area("Description")
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity", min_value=0.1, step=0.5)
    with col2:
        unit = st.selectbox("Unit", ["kg", "liters", "packets", "plates"])
    expiry_date = st.date_input("Expiry Date", value=datetime.now().date())
    pickup_address = st.text_area("Pickup Address")
    submit = st.form_submit_button("Donate Food 🍱", type="primary")

if submit:
    if not food_name.strip() or not pickup_address.strip():
        st.error("Please enter food name and pickup address.")
    else:
        connection = get_connection()
        connection.execute("""
            INSERT INTO donations
            (donor_id, food_name, description, quantity, unit, expiry_time, pickup_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (st.session_state['user_id'], food_name.strip(), description.strip(), quantity,
              unit, expiry_date.strftime('%Y-%m-%d'), pickup_address.strip()))
        connection.commit()
        connection.close()
        st.success("Food donation added successfully! 🎉")

st.divider()
st.header("📦 My Donations")
connection = get_connection()
donations = connection.execute("""
    SELECT * FROM donations WHERE donor_id=? ORDER BY created_at DESC
""", (st.session_state['user_id'],)).fetchall()
connection.close()

if donations:
    for donation in donations:
        with st.container(border=True):
            c1,c2,c3 = st.columns(3)
            c1.subheader(f"🍱 {donation['food_name']}")
            c1.write(donation['description'] or 'No description')
            c2.write(f"**Quantity:** {donation['quantity']} {donation['unit']}")
            c2.write(f"**Expiry:** {donation['expiry_time']}")
            c3.write(f"**Status:** {donation['status']}")
else:
    st.info("You haven't added any donations yet.")
