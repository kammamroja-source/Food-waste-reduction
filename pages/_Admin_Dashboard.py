import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Admin Dashboard - Food Donation System",
    page_icon="🍱",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🍱 Food Waste Reduction & Donation System")
st.subheader("👨‍💼 Admin Dashboard")

st.markdown("---")

# ---------------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------------
# You can replace this with your database data later.

donations = [
    {
        "Donation ID": 1,
        "Donor": "Rahul",
        "Food": "Rice and Curry",
        "Quantity": 20,
        "Location": "Hyderabad",
        "Status": "Collected",
        "Date": "2026-10-01"
    },
    {
        "Donation ID": 2,
        "Donor": "Priya",
        "Food": "Vegetable Biryani",
        "Quantity": 15,
        "Location": "Warangal",
        "Status": "Pending",
        "Date": "2026-10-02"
    },
    {
        "Donation ID": 3,
        "Donor": "Anil",
        "Food": "Chapati and Dal",
        "Quantity": 25,
        "Location": "Karimnagar",
        "Status": "Delivered",
        "Date": "2026-10-03"
    },
    {
        "Donation ID": 4,
        "Donor": "Sneha",
        "Food": "Fruits",
        "Quantity": 10,
        "Location": "Hyderabad",
        "Status": "Collected",
        "Date": "2026-10-04"
    }
]

donation_df = pd.DataFrame(donations)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🔐 Admin Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "All Donations",
        "Pending Donations",
        "Collected Donations",
        "Delivered Donations"
    ]
)

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":

    st.header("📊 Dashboard Overview")

    total_donations = len(donation_df)

    total_food = donation_df["Quantity"].sum()

    pending_food = donation_df[
        donation_df["Status"] == "Pending"
    ]["Quantity"].sum()

    collected_food = donation_df[
        donation_df["Status"] == "Collected"
    ]["Quantity"].sum()

    delivered_food = donation_df[
        donation_df["Status"] == "Delivered"
    ]["Quantity"].sum()

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🍱 Total Donations",
            total_donations
        )

    with col2:
        st.metric(
            "🥗 Total Food",
            f"{total_food} kg"
        )

    with col3:
        st.metric(
            "⏳ Pending Food",
            f"{pending_food} kg"
        )

    with col4:
        st.metric(
            "🚚 Collected Food",
            f"{collected_food} kg"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # ADDITIONAL STATISTICS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"📦 **Total Donations:** {total_donations}"
        )

    with col2:
        st.success(
            f"🚚 **Collected Food:** {collected_food} kg"
        )

    with col3:
        st.success(
            f"🏠 **Delivered Food:** {delivered_food} kg"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # DONATION STATUS CHART
    # -----------------------------------------------------

    st.subheader("📈 Donation Status")

    status_count = donation_df["Status"].value_counts()

    st.bar_chart(status_count)

    st.markdown("---")

    # -----------------------------------------------------
    # RECENT DONATIONS
    # -----------------------------------------------------

    st.subheader("🕒 Recent Donations")

    st.dataframe(
        donation_df.tail(5),
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# ALL DONATIONS
# ---------------------------------------------------------
elif menu == "All Donations":

    st.header("🍱 All Food Donations")

    st.dataframe(
        donation_df,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"**Total Donations:** {len(donation_df)}"
    )

    st.write(
        f"**Total Food Quantity:** {donation_df['Quantity'].sum()} kg"
    )


# ---------------------------------------------------------
# PENDING DONATIONS
# ---------------------------------------------------------
elif menu == "Pending Donations":

    st.header("⏳ Pending Donations")

    pending_df = donation_df[
        donation_df["Status"] == "Pending"
    ]

    if pending_df.empty:
        st.success("No pending donations 🎉")
    else:
        st.dataframe(
            pending_df,
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            f"Pending Food: {pending_df['Quantity'].sum()} kg"
        )


# ---------------------------------------------------------
# COLLECTED DONATIONS
# ---------------------------------------------------------
elif menu == "Collected Donations":

    st.header("🚚 Collected Donations")

    collected_df = donation_df[
        donation_df["Status"] == "Collected"
    ]

    if collected_df.empty:
        st.info("No collected donations available.")
    else:
        st.dataframe(
            collected_df,
            use_container_width=True,
            hide_index=True
        )

        collected_food = collected_df["Quantity"].sum()

        st.success(
            f"Total Collected Food: {collected_food} kg"
        )


# ---------------------------------------------------------
# DELIVERED DONATIONS
# ---------------------------------------------------------
elif menu == "Delivered Donations":

    st.header("🏠 Delivered Donations")

    delivered_df = donation_df[
        donation_df["Status"] == "Delivered"
    ]

    if delivered_df.empty:
        st.info("No delivered donations available.")
    else:
        st.dataframe(
            delivered_df,
            use_container_width=True,
            hide_index=True
        )

        delivered_food = delivered_df["Quantity"].sum()

        st.success(
            f"Total Delivered Food: {delivered_food} kg"
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")

st.caption(
    "Food Waste Reduction & Donation System | Admin Panel"
)