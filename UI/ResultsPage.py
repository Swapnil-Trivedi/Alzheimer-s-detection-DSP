import streamlit as st
import joblib  # Assuming your model is saved in a `.pkl` file
import numpy as np

# Load your trained ML model (replace with actual path)
# For example, if you have a trained model saved as 'alzheimers_model.pkl':
model = joblib.load('alzheimers_model.pkl')

def get_risk_prediction(game_scores):
    # Example of how to prepare input for the model
    # Let's assume the model takes a 1D array of features for prediction
    input_features = []

    # Add game scores to the features (you can also add other clinical inputs here)
    input_features.append(game_scores.get("MemoryGame", 0))  # Memory game score
    input_features.append(game_scores.get("TaskSwitching", 0))  # Task Switching score

    # Example: Add clinical features like age, gender, etc. (this can come from `UserInput.py`)
    input_features.append(st.session_state.get('age', 0))  # Example: age
    input_features.append(st.session_state.get('gender', 0))  # Example: gender (0 = male, 1 = female)
    
    # Convert features to a numpy array (or format required by your model)
    input_array = np.array(input_features).reshape(1, -1)

    # Get prediction from the model
    prediction = model.predict(input_array)

    return prediction[0]

def render_results_page():
    st.title("🏆 Game Results")

    st.markdown("""
    Here are your results across all games:
    """)

    # Check if session state has any game scores stored
    if "game_scores" in st.session_state and len(st.session_state["game_scores"]) > 0:
        # Display the scores
        for game, score in st.session_state["game_scores"].items():
            st.subheader(f"{game}: {score} points")
    else:
        st.warning("You haven't completed any games yet!")

    # Display the prediction after the "Predict" button is clicked
    if "game_scores" in st.session_state and len(st.session_state["game_scores"]) > 0:
        # Add a button to predict Alzheimer's risk
        if st.button("🔮 Predict Alzheimer's Risk"):
            # Get the risk prediction
            prediction = get_risk_prediction(st.session_state["game_scores"])

            # Display the prediction result
            if prediction == 1:
                st.write("**Alzheimer's Risk Prediction:** High Risk")
            else:
                st.write("**Alzheimer's Risk Prediction:** Low Risk")

    else:
        st.warning("Please complete the games to see the result.")

    # Buttons to go back to home or start new games
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Go Home"):
            st.session_state["game_scores"] = {}  # Reset scores if needed
            st.experimental_rerun()  # Redirect to home
    with col2:
        if st.button("➡️ Next Game"):
            # Redirect to the next game (e.g., a Task Switching game or another)
            st.session_state["game_scores"] = {}  # Reset scores for a new session
            st.experimental_rerun()  # Optionally, you can change the redirection logic
