import streamlit as st
import pandas as pd
import plotly.express as px

def render_results_page():
    st.title("📊 Cognitive Assessment Results")

    # -------------------------------
    # User Profile Overview
    # -------------------------------
    st.subheader("👤 User Profile Overview")
    if "user_data" in st.session_state and st.session_state.user_data:
        user_data = st.session_state.user_data

        # Convert user_data dict into a DataFrame with 2 columns
        df_profile = pd.DataFrame(list(user_data.items()), columns=["Field", "Value"])

        # Display as a table
        st.table(df_profile)
    else:
        st.info("No user data found. Please fill out your information first.")

    st.markdown("---")

    # -------------------------------
    # Capture score from query params
    # -------------------------------
    query_params = st.query_params  # Correct API
    for game in ["Memory", "Reaction", "TaskSwitching", "MemoryPattern"]:
        key = game + "_score"
        if key in query_params:
            value = float(query_params[key][0])
            if "game_scores" not in st.session_state:
                st.session_state.game_scores = {}
            st.session_state.game_scores[game] = value

    # -------------------------------
    # Game Scores
    # -------------------------------
    st.subheader("🎮 Game Scores")
    if "game_scores" in st.session_state and st.session_state.game_scores:
        game_scores = st.session_state.game_scores
        display_scores = {}
        for game_name, score in game_scores.items():
            if score is None:
                display_scores[game_name] = 0
            else:
                # Convert normalized score to points for some games
                if game_name in ["Memory", "Reaction"]:
                    display_scores[game_name] = score
                else:
                    display_scores[game_name] = score

        # Display metrics in columns
        cols = st.columns(len(display_scores))
        for i, (game, score) in enumerate(display_scores.items()):
            cols[i].metric(label=game, value=score)

        # Optional: Bar chart
        df = pd.DataFrame({"Game": list(display_scores.keys()), "Score": list(display_scores.values())})
        fig = px.bar(df, x="Game", y="Score", text="Score", color="Score", color_continuous_scale="viridis")
        fig.update_layout(showlegend=False, yaxis_title="Score", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No game scores found. Play the games to see results.")

    st.markdown("---")

    # -------------------------------
    # Model Prediction Section
    # -------------------------------
    st.subheader("🧠 Predict Alzheimer’s Risk (Mock)")
    model_choice = st.radio(
        "Select a model:",
        ["Decision Tree", "XGBoost", "Neural Network"]
    )

    if st.button("Predict"):
        import random
        prediction = random.choice(["Positive", "Negative"])
        prob = random.uniform(0.6, 0.99) if prediction=="Positive" else random.uniform(0.01,0.4)

        if prediction == "Positive":
            st.error(f"Alzheimer’s Risk: {prediction}")
        else:
            st.success(f"Alzheimer’s Risk: {prediction}")
        st.write(f"Confidence: {prob*100:.1f}%")
