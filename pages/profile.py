import streamlit as st


st.title("👤 Profile")

st.write(
    "Manage your account and fitness preferences."
)

st.divider()


st.subheader("Account")

col1, col2 = st.columns(2)

with col1:
    st.text_input(
        "Name",
        value="Demo User"
    )

with col2:
    st.text_input(
        "Email",
        value="demo@example.com",
        disabled=True
    )


st.divider()


st.subheader("Fitness Preferences")

goal = st.selectbox(
    "Primary Fitness Goal",
    [
        "General Fitness",
        "Strength",
        "Endurance",
        "Weight Loss"
    ]
)

experience = st.selectbox(
    "Experience Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


if st.button("Save Preferences"):
    st.success(
        "Preferences saved locally for now. "
        "They will be stored in SQLite after "
        "authentication is implemented."
    )


st.divider()


st.subheader("⚠️ Safety")

st.warning(
    "This application provides fitness assistance "
    "and is not a substitute for professional "
    "medical or fitness advice."
)