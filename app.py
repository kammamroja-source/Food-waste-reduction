import streamlit as st

from database import create_tables


# Create database tables
create_tables()


# Page configuration
st.set_page_config(
    page_title="Food Waste Reduction & Donation",
    page_icon="🍱",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #f7fff7;
}

.title {
    font-size: 45px;
    font-weight: bold;
    color: #2e7d32;
}

.subtitle {
    font-size: 20px;
    color: #555;
}

.card {
    padding: 25px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="title">🍱 Food Waste Reduction & Donation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Connecting surplus food with people who need it.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("""
    <div class="card">

    ### 🍽️ Donors

    Restaurants, hotels, events and individuals
    can donate surplus food.

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="card">

    ### 🤝 NGOs / Receivers

    Organizations can find available food
    and request donations.

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="card">

    ### 📊 Admin

    Administrators can monitor donations,
    requests and system statistics.

    </div>
    """, unsafe_allow_html=True)


st.divider()

st.info(
    "Use the pages in the sidebar to register, login "
    "and manage food donations."
)
