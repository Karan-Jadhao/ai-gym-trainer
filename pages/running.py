import streamlit as st

st.title("🏃 Running")

st.write(
    "Track your running distance and pace using "
    "browser GPS."
)

st.divider()


col1, col2, col3,col4 = st.columns(4)

with col1:
    st.metric("Distance", "0.00 km")

with col2:
    st.metric("Duration", "00:00")

with col3:
    st.metric("Average Pace", "-- min/km")

with col4:
    st.metric("Gps Points", "0")

st.divider()

st.subheader("Run Tracking")
st.info(
    "Your GPS route will appear here after "
    "browser geolocation is implemented."
)


col1, col2 = st.columns(2)

with col1:
    if st.button(
        "▶️ Start Run",
        use_container_width=True
    ):
        st.success(
            "GPS tracking will start in the next phase."
        )

with col2:
    if st.button(
        "⏹️ Finish Run",
        use_container_width=True
    ):
        st.info(
            "Run data will be saved after GPS "
            "and database integration."
        )


st.divider()


st.subheader("🎙️ Voice Coaching")

st.write(
    "Periodic running feedback will be provided "
    "using browser speech synthesis."
)