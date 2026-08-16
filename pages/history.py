import streamlit as st
import pandas as pd

from database.database import (
    get_user_workouts,
    get_workout_statistics
)


# --------------------------------------------------
# Authentication
# --------------------------------------------------

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()


user_id = st.session_state.user_id


# --------------------------------------------------
# Page title
# --------------------------------------------------

st.title("📊 Workout & Running History")

st.write(
    "Track your fitness progress over time."
)

st.divider()


# --------------------------------------------------
# Statistics
# --------------------------------------------------

statistics = get_workout_statistics(
    user_id
)

total_workouts = statistics["total_workouts"]
total_reps = statistics["total_reps"]
average_form = statistics["average_form"]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Workouts",
        total_workouts
    )

with col2:
    st.metric(
        "Total Reps",
        total_reps
    )

with col3:
    st.metric(
        "Average Form",
        f"{average_form:.1f}"
    )

with col4:
    st.metric(
        "Total Runs",
        "0"
    )


st.divider()


# --------------------------------------------------
# Workout history
# --------------------------------------------------

st.subheader("🏋️ Workout History")

workouts = get_user_workouts(
    user_id
)


if workouts:

    workout_data = []

    for workout in workouts:

        workout_data.append(
            {
                "Date": workout["created_at"],
                "Exercise": workout["exercise"],
                "Repetitions": workout["repetitions"],
                "Form Score": workout["form_score"],
                "Duration (sec)": workout["duration"],
                "AI Feedback": workout["feedback"]
            }
        )

    dataframe = pd.DataFrame(
        workout_data
    )

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No workouts recorded yet. "
        "Complete your first workout!"
    )


st.divider()


# --------------------------------------------------
# Progress chart
# --------------------------------------------------

st.subheader("📈 Repetition Progress")


if workouts:

    chart_data = pd.DataFrame(
        {
            "Date": [
                workout["created_at"]
                for workout in workouts
            ],
            "Repetitions": [
                workout["repetitions"]
                for workout in workouts
            ]
        }
    )

    chart_data["Date"] = pd.to_datetime(
        chart_data["Date"]
    )

    chart_data = chart_data.sort_values(
        "Date"
    )

    st.line_chart(
        chart_data.set_index("Date")
    )

else:

    st.info(
        "Complete some workouts to see "
        "your progress chart."
    )


st.divider()


# --------------------------------------------------
# Running history placeholder
# --------------------------------------------------

st.subheader("🏃 Running History")

st.info(
    "Running history will be connected to SQLite "
    "when we implement GPS tracking."
)