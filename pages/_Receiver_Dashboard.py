import streamlit as st

from database import get_connection


st.set_page_config(
    page_title="Receiver Dashboard",
    page_icon="🤝",
    layout="wide"
)


if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.stop()


if st.session_state.get("role") != "receiver":

    st.error(
        "Only receivers can access this page."
    )

    st.stop()


st.title("🤝 Receiver Dashboard")

st.write(
    f"Welcome, **{st.session_state['name']}**!"
)


st.divider()


st.header("🍱 Available Food")


connection = get_connection()

donations = connection.execute("""
    SELECT
        donations.*,
        users.name AS donor_name,
        users.phone AS donor_phone
    FROM donations

    JOIN users
    ON donations.donor_id = users.id

    WHERE donations.status = 'Available'

    ORDER BY donations.created_at DESC
""").fetchall()

connection.close()


if not donations:

    st.info(
        "No food donations are currently available."
    )


for donation in donations:

    with st.container(border=True):

        st.subheader(
            f"🍱 {donation['food_name']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Quantity:** "
                f"{donation['quantity']} "
                f"{donation['unit']}"
            )

            st.write(
                f"**Description:** "
                f"{donation['description']}"
            )

            st.write(
                f"**Expiry:** "
                f"{donation['expiry_time']}"
            )

        with col2:

            st.write(
                f"**Donor:** "
                f"{donation['donor_name']}"
            )

            st.write(
                f"**Pickup Location:** "
                f"{donation['pickup_address']}"
            )


        if st.button(
            "Request Food",
            key=f"request_{donation['id']}"
        ):

            connection = get_connection()

            existing = connection.execute("""
                SELECT *
                FROM requests
                WHERE donation_id = ?
                AND receiver_id = ?
            """, (
                donation["id"],
                st.session_state["user_id"]
            )).fetchone()


            if existing:

                st.warning(
                    "You already requested this donation."
                )

            else:

                connection.execute("""
                    INSERT INTO requests
                    (
                        donation_id,
                        receiver_id
                    )
                    VALUES (?, ?)
                """, (
                    donation["id"],
                    st.session_state["user_id"]
                ))

                connection.commit()

                st.success(
                    "Food request submitted! 🎉"
                )

            connection.close()
