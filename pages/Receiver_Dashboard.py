import streamlit as st
from database import get_connection

st.set_page_config(page_title="Receiver Dashboard", page_icon="🤝", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "receiver":
    st.error("Only receivers can access this page.")
    st.stop()

st.title("🤝 Receiver Dashboard")
st.write(f"Welcome, **{st.session_state['name']}**!")
st.divider()

st.header("🍱 Available Food")
connection = get_connection()
donations = connection.execute("""
    SELECT donations.*, users.name AS donor_name, users.phone AS donor_phone
    FROM donations JOIN users ON donations.donor_id = users.id
    WHERE donations.status = 'Available'
    ORDER BY donations.created_at DESC
""").fetchall()
connection.close()

if not donations:
    st.info("No food donations are currently available.")

for donation in donations:
    with st.container(border=True):
        st.subheader(f"🍱 {donation['food_name']}")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Quantity:** {donation['quantity']} {donation['unit']}")
            st.write(f"**Description:** {donation['description'] or 'Not provided'}")
            st.write(f"**Expiry:** {donation['expiry_time']}")
        with col2:
            st.write(f"**Donor:** {donation['donor_name']}")
            st.write(f"**Pickup:** {donation['pickup_address']}")
            if donation['donor_phone']:
                st.write(f"**Contact:** {donation['donor_phone']}")

        if st.button("Request Food", key=f"request_{donation['id']}"):
            connection = get_connection()
            existing = connection.execute(
                "SELECT id FROM requests WHERE donation_id=? AND receiver_id=?",
                (donation['id'], st.session_state['user_id'])
            ).fetchone()
            if existing:
                st.warning("You already requested this donation.")
            else:
                connection.execute(
                    "INSERT INTO requests (donation_id, receiver_id) VALUES (?, ?)",
                    (donation['id'], st.session_state['user_id'])
                )
                connection.commit()
                st.success("Food request submitted! 🎉")
            connection.close()

st.divider()
st.header("📋 My Requests")
connection = get_connection()
requests = connection.execute("""
    SELECT requests.id, requests.status, requests.requested_at,
           donations.food_name, donations.quantity, donations.unit,
           users.name AS donor_name
    FROM requests
    JOIN donations ON requests.donation_id = donations.id
    JOIN users ON donations.donor_id = users.id
    WHERE requests.receiver_id = ?
    ORDER BY requests.requested_at DESC
""", (st.session_state['user_id'],)).fetchall()
connection.close()

if requests:
    for request in requests:
        st.write(
            f"**{request['food_name']}** — {request['quantity']} {request['unit']} "
            f"| Donor: {request['donor_name']} | Status: **{request['status']}**"
        )
else:
    st.info("You have not submitted any food requests yet.")
