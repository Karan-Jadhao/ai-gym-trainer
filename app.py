import streamlit as st
from pathlib import Path

from database.database import initialize_database
from auth.auth import (
    initialize_session,
    show_auth_page,
    logout_user
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Load CSS
# --------------------------------------------------

def load_css():
    css_file = Path("assets/style.css")

    if css_file.exists():

        with open(
            css_file,
            "r",
            encoding="utf-8"
        ) as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# --------------------------------------------------
# Initialize application
# --------------------------------------------------

initialize_database()

initialize_session()


# --------------------------------------------------
# Authentication wall
# --------------------------------------------------

if not st.session_state.logged_in:

    show_auth_page()

    st.stop()


# --------------------------------------------------
# Logged-in user sidebar
# --------------------------------------------------

with st.sidebar:

    st.markdown("### 🏋️ AI Gym Trainer")

    st.write(
        f"Welcome, **{st.session_state.user_name}**!"
    )

    st.caption(
        st.session_state.user_email
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_user()


# --------------------------------------------------
# Application navigation
# --------------------------------------------------

pages = {
    "Main": [

        st.Page(
            "pages/dashboard.py",
            title="Dashboard",
            icon="🏠"
        ),

        st.Page(
            "pages/workout.py",
            title="Workout Trainer",
            icon="🏋️"
        ),

        st.Page(
            "pages/running.py",
            title="Running",
            icon="🏃"
        ),

        st.Page(
            "pages/history.py",
            title="History",
            icon="📊"
        ),

        st.Page(
            "pages/profile.py",
            title="Profile",
            icon="👤"
        ),
    ]
}


pg = st.navigation(pages)

pg.run()