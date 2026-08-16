import streamlit as st

st.title("AI Gym Trainer")

user_name = st.session_state.get(
    "user_name",
    "User"
)

st.subheader(f"Welcome to AI Gym Trainer, {user_name}!")

st.write(
    "Your personal AI-powered fitness assistant "
    "for strength training and running."
)

st.divider()
st.subheader("Today's Activity")
col1, col2, col3,col4 = st.columns(4)

with col1:
    st.metric("Workout Sets", "0")

with col2:
    st.metric("Total Reps", "0")

with col3:
    st.metric("Running Distance", "0 km")

with col4:
    st.metric(label="Average form",value="--")

st.divider()

st.subheader("Quick Actions")
col1,col2=st.columns(2)

with col1:
    st.markdown("### Strength Training")

    st.write(
        "Use your webcam to track squats, "
        "push-ups, and bicep curls."
    )

    if st.button(
        "Start Workout",
        use_container_width=True
    ):
        st.switch_page("pages/workout.py")


with col2:
    st.markdown("### Running")

    st.write(
        "Track your run using GPS without "
        "using camera-based pose detection."
    )

    if st.button(
        "Start Running",
        use_container_width=True
    ):
        st.switch_page("pages/running.py")


st.divider()

st.subheader("Recent Activity")

st.info(
    "Your recent workouts and runs will appear here "
    "after you complete your first session."
)

st.warning(
    "Safety Notice: AI Gym Trainer is a fitness "
    "assistance tool and is not medical advice. "
    "Stop exercising if you experience pain, dizziness, "
    "or discomfort."
)