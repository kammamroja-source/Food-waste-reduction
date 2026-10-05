import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_connection


st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)


if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.stop()


if st.session_state.get("role") != "admin":

    st.error(
        "Only administrators can access this page."
    )

    st.stop()


st.title("📊 Admin Dashboard")


connection = get_connection()


# Total users
total_users = connection.execute("""
    SELECT COUNT(*) AS count
    FROM users
""").fetchone()["count"]


# Total donations
total_donations = connection.execute("""
    SELECT COUNT(*) AS count
    FROM donations
""").fetchone()["count"]


# Total food
total_food = connection.execute("""
    SELECT COALESCE(SUM(quantity), 0) AS total
    FROM donations
""").fetchone()["total"]


# Total requests
total_requests = connection.execute("""
    SELECT COUNT(*) AS count
    FROM requests
""").fetchone()["count"]


connection.close()


# Statistics

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Users",
        total_users
    )


with col2:

    st.metric(
        "🍱 Donations",
        total_donations
    )


with col3:

    st.metric(
        "🥘 Food Rescued",
        total_food
    )


with col4:

    st.metric(
        "🤝 Requests",
        total_requests
    )


st.divider()


# Donation status chart

connection = get_connection()

data = pd.read_sql_query("""
    SELECT status, COUNT(*) AS count
    FROM donations
    GROUP BY status
""", connection)

connection.close()


if not data.empty:

    fig = px.pie(
        data,
        names="status",
        values="count",
        title="Donation Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
