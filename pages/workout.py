import streamlit as st
from database.database import save_workout


# --------------------------------------------------
# Check authentication
# --------------------------------------------------

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()


user_id = st.session_state.user_id


# --------------------------------------------------
# Page title
# --------------------------------------------------

st.title("🏋️ Live Workout Trainer")

st.write(
    "Choose an exercise and start your "
    "camera-based training session."
)

st.divider()


# --------------------------------------------------
# Exercise selection
# --------------------------------------------------

exercise = st.selectbox(
    "Select Exercise",
    [
        "Squat",
        "Push-up",
        "Bicep Curl"
    ]
)


# --------------------------------------------------
# Current workout metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Repetitions",
        "0"
    )

with col2:
    st.metric(
        "Form Score",
        "0 / 100"
    )

with col3:
    st.metric(
        "Phase",
        "Ready"
    )

with col4:
    st.metric(
        "Duration",
        "00:00"
    )


st.divider()


# --------------------------------------------------
# Camera placeholder
# --------------------------------------------------

st.subheader("📷 Camera")

st.info(
    "Camera-based pose detection will be added "
    "in the next stage."
)


# --------------------------------------------------
# AI coaching placeholder
# --------------------------------------------------

st.subheader("🤖 AI Coaching")

st.success(
    "AI coaching feedback will appear here "
    "after the workout."
)


st.divider()


# --------------------------------------------------
# Demo workout controls
# --------------------------------------------------

st.subheader("Workout Controls")

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "▶️ Start Workout",
        use_container_width=True
    ):

        st.session_state.workout_started = True

        st.info(
            f"{exercise} workout started!"
        )


with col2:

    if st.button(
        "⏹️ Finish Workout",
        use_container_width=True
    ):

        # ------------------------------------------
        # Temporary demo values
        # ------------------------------------------

        demo_reps = 10
        demo_form_score = 85.0
        demo_duration = 60.0

        demo_feedback = (
            "Good session. Keep your movement "
            "controlled and maintain proper form."
        )

        # ------------------------------------------
        # Save to database
        # ------------------------------------------

        workout_id = save_workout(
            user_id=user_id,
            exercise=exercise,
            repetitions=demo_reps,
            form_score=demo_form_score,
            duration=demo_duration,
            feedback=demo_feedback
        )

        st.success(
            f"Workout saved successfully! "
            f"Workout ID: {workout_id}"
        )

        st.info(
            f"{exercise}: {demo_reps} reps | "
            f"Form: {demo_form_score}/100"
        )