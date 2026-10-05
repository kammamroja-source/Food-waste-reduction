import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About the System")
st.write("### Food Waste Reduction & Donation System")
st.write(
    "This application connects people and organizations with surplus food "
    "to receivers who can use it, helping reduce food waste."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.info("🍱 **Donors**\n\nAdd surplus food with quantity, expiry and pickup details.")
with col2:
    st.info("🤝 **Receivers**\n\nView available food and submit requests.")
with col3:
    st.info("📊 **Admins**\n\nMonitor users, donations and requests.")

st.divider()
st.subheader("Key Features")
for item in [
    "Secure user registration and login",
    "Food donation management",
    "Available-food browsing for receivers",
    "Donation request tracking",
    "Admin statistics and status charts",
]:
    st.write(f"✅ {item}")
