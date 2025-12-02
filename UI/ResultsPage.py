import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np
from pathlib import Path
from .cognitive_scorer import calculate_cognitive_scores, get_cognitive_assessment_status
import shap
import matplotlib.pyplot as plt

# Global cache for neural network model
_NN_MODEL_CACHE = {}

def load_pytorch_model(model_path, scaler_path):
    """
    Load PyTorch neural network model - no threading issues!
    """
    cache_key = f"{model_path}_{scaler_path}"
    
    if cache_key in _NN_MODEL_CACHE:
        return _NN_MODEL_CACHE[cache_key]
    
    import torch
    import torch.nn as nn
    
    # Define the model architecture (same as training)
    class AlzheimerNet(nn.Module):
        def __init__(self, input_dim):
            super(AlzheimerNet, self).__init__()
            self.network = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(32, 32),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(32, 1),
                nn.Sigmoid()
            )
        
        def forward(self, x):
            return self.network(x)
    
    # Load checkpoint
    checkpoint = torch.load(str(model_path), map_location='cpu')
    
    # Initialize model
    model = AlzheimerNet(checkpoint['input_dim'])
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # Load scaler
    scaler = joblib.load(str(scaler_path))
    
    # Cache it
    _NN_MODEL_CACHE[cache_key] = (model, scaler, torch)
    
    return model, scaler, torch

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
    st.subheader("🧠 Alzheimer's Disease Risk Prediction")
    
    # Feature columns (32 features used in training)
    FEATURE_COLUMNS = [
        'Age', 'Gender', 'Ethnicity', 'EducationLevel', 'BMI', 'Smoking',
        'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
        'FamilyHistoryAlzheimers', 'CardiovascularDisease', 'Diabetes',
        'Depression', 'HeadInjury', 'Hypertension', 'SystolicBP', 'DiastolicBP',
        'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides',
        'MMSE', 'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems',
        'ADL', 'Confusion', 'Disorientation', 'PersonalityChanges',
        'DifficultyCompletingTasks', 'Forgetfulness'
    ]
    
    model_choice = st.radio(
        "Select a model:",
        ["Decision Tree", "Random Forest", "XGBoost", "Neural Network"]
    )

    if st.button("🔬 Predict Risk", type="primary"):
        # Check if user data exists
        if "user_data" not in st.session_state or not st.session_state.user_data:
            st.error("⚠️ Please fill out your information in the 'User Information' tab first!")
        else:
            try:
                with st.spinner("Loading model and making prediction..."):
                    # Get base path for models
                    base_path = Path(__file__).parent.parent / "models"
                    
                    # Prepare user data
                    user_data = st.session_state.user_data.copy()
                    
                    # Check if cognitive scores need to be calculated from games
                    if not st.session_state.get("manual_cognitive_input", False):
                        # Get game scores
                        game_scores = st.session_state.get("game_scores", {})
                        
                        # Calculate cognitive scores from game performance
                        cognitive_scores = calculate_cognitive_scores(game_scores)
                        
                        # Merge with user data
                        user_data.update(cognitive_scores)
                        
                        # Get status for display
                        status = get_cognitive_assessment_status(game_scores)
                        
                        if status["games_completed"] == 0:
                            st.warning("⚠️ No games played! Using default cognitive scores. For better predictions, play the cognitive games.")
                        elif status["games_completed"] < 4:
                            st.info(f"ℹ️ {status['games_completed']}/4 games completed. Playing all games improves prediction accuracy.")
                        else:
                            st.success(f"✅ All {status['games_completed']}/4 games completed! Using game-derived cognitive scores.")
                    else:
                        st.info("📝 Using manually entered cognitive assessment scores.")
                    
                    # Create input dataframe with proper feature order
                    input_data = pd.DataFrame([user_data])[FEATURE_COLUMNS]
                    
                    # Load and predict based on selected model
                    if model_choice == "Decision Tree":
                        model_path = base_path / "decision_tree" / "decision_tree_model.pkl"
                        model = joblib.load(model_path)
                        prediction = model.predict(input_data)[0]
                        probability = model.predict_proba(input_data)[0]
                        
                    elif model_choice == "Random Forest":
                        model_path = base_path / "random_forest" / "random_forest_model.pkl"
                        model = joblib.load(model_path)
                        prediction = model.predict(input_data)[0]
                        probability = model.predict_proba(input_data)[0]
                        
                    elif model_choice == "XGBoost":
                        model_path = base_path / "xgboost" / "xgboost_model.pkl"
                        model = joblib.load(model_path)
                        prediction = model.predict(input_data)[0]
                        probability = model.predict_proba(input_data)[0]
                        
                    elif model_choice == "Neural Network":
                        try:
                            model_path = base_path / "neural_network" / "pytorch_nn_model.pth"
                            scaler_path = base_path / "neural_network" / "scaler.pkl"
                            
                            # Load PyTorch model (no mutex issues!)
                            model, scaler, torch = load_pytorch_model(model_path, scaler_path)
                            
                            # Scale the input
                            input_scaled = scaler.transform(input_data)
                            
                            # Convert to tensor and predict
                            input_tensor = torch.FloatTensor(input_scaled)
                            
                            with torch.no_grad():
                                prob_diagnosis = model(input_tensor).squeeze().item()
                            
                            prediction = 1 if prob_diagnosis > 0.5 else 0
                            probability = np.array([1 - prob_diagnosis, prob_diagnosis])
                        except Exception as e:
                            st.error(f"Error loading Neural Network model: {e}")
                            st.info("Make sure PyTorch is installed: `pip install torch`")
                            raise
                    
                    # Display results
                    st.markdown("---")
                    st.markdown(f"### Prediction Results - {model_choice}")
                    
                    # Show data source transparency
                    if not st.session_state.get("manual_cognitive_input", False):
                        with st.expander("📊 Cognitive Assessment Data Source"):
                            game_scores = st.session_state.get("game_scores", {})
                            
                            st.markdown("**Game Performance → Cognitive Scores:**")
                            
                            col_game1, col_game2 = st.columns(2)
                            
                            with col_game1:
                                st.metric("Memory Game", f"{game_scores.get('Memory', 0)}/8 pairs")
                                st.metric("Reaction Game", f"{game_scores.get('Reaction', 0)} clicks")
                            
                            with col_game2:
                                st.metric("Task Switching", f"{game_scores.get('TaskSwitch', 0)} correct")
                                st.metric("Pattern Game", f"{game_scores.get('Pattern', 0)} rounds")
                            
                            st.markdown("**Derived Cognitive Scores:**")
                            cognitive_scores = calculate_cognitive_scores(game_scores)
                            
                            col_cog1, col_cog2, col_cog3 = st.columns(3)
                            
                            with col_cog1:
                                st.metric("MMSE Score", f"{cognitive_scores['MMSE']}/30")
                                st.metric("Functional", f"{cognitive_scores['FunctionalAssessment']}/10")
                            
                            with col_cog2:
                                st.metric("ADL", f"{cognitive_scores['ADL']}/10")
                                symptoms = sum([
                                    cognitive_scores['MemoryComplaints'],
                                    cognitive_scores['Forgetfulness'],
                                    cognitive_scores['Confusion']
                                ])
                                st.metric("Symptoms", f"{symptoms}/9 flags")
                            
                            with col_cog3:
                                st.caption("**Symptom Flags:**")
                                flags = []
                                if cognitive_scores['MemoryComplaints']: flags.append("Memory")
                                if cognitive_scores['Forgetfulness']: flags.append("Forgetful")
                                if cognitive_scores['Confusion']: flags.append("Confused")
                                if cognitive_scores['Disorientation']: flags.append("Disoriented")
                                if cognitive_scores['DifficultyCompletingTasks']: flags.append("Task Difficulty")
                                
                                st.write(", ".join(flags) if flags else "None detected")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if prediction == 1:
                            st.error("### 🔴 Positive Diagnosis Risk")
                            st.markdown("**The model indicates elevated risk for Alzheimer's disease.**")
                        else:
                            st.success("### 🟢 Negative Diagnosis Risk")
                            st.markdown("**The model indicates low risk for Alzheimer's disease.**")
                    
                    with col2:
                        st.metric(
                            label="Confidence Score",
                            value=f"{max(probability)*100:.1f}%"
                        )
                        st.metric(
                            label="Risk of Diagnosis",
                            value=f"{probability[1]*100:.1f}%"
                        )
                    
                    # Detailed probabilities
                    st.markdown("---")
                    st.markdown("#### Probability Breakdown")
                    prob_df = pd.DataFrame({
                        'Outcome': ['No Diagnosis', 'Diagnosis'],
                        'Probability': [probability[0]*100, probability[1]*100]
                    })
                    
                    fig = px.bar(
                        prob_df, 
                        x='Outcome', 
                        y='Probability',
                        text=prob_df['Probability'].apply(lambda x: f'{x:.1f}%'),
                        color='Outcome',
                        color_discrete_map={'No Diagnosis': 'green', 'Diagnosis': 'red'}
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(
                        showlegend=False,
                        yaxis_title="Probability (%)",
                        yaxis_range=[0, 105]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # SHAP Explanation - Simple Waterfall Plot
                    st.markdown("---")
                    st.subheader("🔍 What Contributed to This Prediction?")
                    
                    with st.expander("📖 How to Read This Plot", expanded=False):
                        st.markdown("""
                        **Waterfall Plot Explanation:**
                        
                        - **E[f(X)]** (bottom) = Average prediction across all patients (baseline)
                        - **f(x)** (top) = This specific patient's prediction
                        - **Red bars (→)** = Features that INCREASED the risk (pushed toward diagnosis)
                        - **Blue bars (←)** = Features that DECREASED the risk (pushed away from diagnosis)
                        - **Bar length** = How much that feature changed the prediction
                        
                        The plot starts at the baseline and shows how each feature contributes to reach the final prediction.
                        Only the most impactful features are shown for clarity.
                        """)
                    
                    try:
                        with st.spinner("Generating explanation..."):
                            # Generate SHAP values based on model type
                            if model_choice == "Neural Network":
                                # For neural network, use DeepExplainer
                                import torch
                                
                                # Load background data (sample from training data)
                                background_path = base_path.parent / "data" / "alzheimers_disease_data.csv"
                                if background_path.exists():
                                    background_df = pd.read_csv(background_path)[FEATURE_COLUMNS].sample(100, random_state=42)
                                    background_scaled = scaler.transform(background_df)
                                    background_tensor = torch.FloatTensor(background_scaled)
                                    
                                    # Create DeepExplainer
                                    explainer = shap.DeepExplainer(model, background_tensor)
                                    input_tensor = torch.FloatTensor(input_scaled)
                                    shap_values = explainer.shap_values(input_tensor)
                                    
                                    # Get SHAP values - flatten to 1D array
                                    if isinstance(shap_values, list):
                                        shap_values_diagnosis = np.array(shap_values[0]).flatten()
                                    else:
                                        shap_values_diagnosis = np.array(shap_values).flatten()
                                    
                                    # Ensure it's exactly 1D with 32 features
                                    if shap_values_diagnosis.shape[0] != len(FEATURE_COLUMNS):
                                        shap_values_diagnosis = shap_values_diagnosis[:len(FEATURE_COLUMNS)]
                                    
                                    # Create waterfall plot
                                    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                                    shap.plots.waterfall(
                                        shap.Explanation(
                                            values=shap_values_diagnosis,
                                            base_values=float(explainer.expected_value),
                                            data=input_data.iloc[0].values,
                                            feature_names=FEATURE_COLUMNS
                                        ),
                                        max_display=10,
                                        show=False
                                    )
                                    plt.tight_layout()
                                    col1, col2, col3 = st.columns([1, 2, 1])
                                    with col2:
                                        st.pyplot(fig, width='content')
                                    plt.close()
                                else:
                                    st.info("📊 Feature importance visualization (training data needed for Neural Network SHAP)")
                            else:
                                # Tree-based models: fast and exact
                                explainer = shap.TreeExplainer(model)
                                shap_values = explainer.shap_values(input_data)
                                
                                # Handle different SHAP value formats
                                if isinstance(shap_values, list) and len(shap_values) == 2:
                                    # List of arrays for binary classification [class 0, class 1]
                                    shap_values_diagnosis = shap_values[1][0]  # Class 1, first sample
                                    base_value = explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
                                elif isinstance(shap_values, np.ndarray):
                                    if len(shap_values.shape) == 3:
                                        # 3D array: (samples, features, classes)
                                        shap_values_diagnosis = shap_values[0, :, 1]  # First sample, all features, diagnosis class
                                        base_value = explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value
                                    elif len(shap_values.shape) == 2:
                                        # 2D array: (samples, features) - already for one class
                                        shap_values_diagnosis = shap_values[0]  # First sample
                                        base_value = explainer.expected_value
                                    else:
                                        # 1D array
                                        shap_values_diagnosis = shap_values
                                        base_value = explainer.expected_value
                                else:
                                    shap_values_diagnosis = shap_values
                                    base_value = explainer.expected_value
                                
                                # Ensure base_value is scalar
                                if isinstance(base_value, (list, np.ndarray)):
                                    base_value = float(base_value[0]) if len(base_value) > 0 else 0.0
                                else:
                                    base_value = float(base_value)
                                
                                # Create waterfall plot
                                fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                                shap.plots.waterfall(
                                    shap.Explanation(
                                        values=shap_values_diagnosis,
                                        base_values=base_value,
                                        data=input_data.iloc[0].values,
                                        feature_names=FEATURE_COLUMNS
                                    ),
                                    max_display=10,
                                    show=False
                                )
                                plt.tight_layout()
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    st.pyplot(fig, width='content')
                                plt.close()
                    
                    except Exception as e:
                        st.warning(f"Could not generate feature explanation: {str(e)}")
                    
                    # Disclaimer
                    st.info("⚠️ **Disclaimer:** This prediction is for educational purposes only and should not be used as a medical diagnosis. Please consult with healthcare professionals for proper medical advice.")
                    
            except FileNotFoundError as e:
                st.error(f"❌ Model file not found: {e}")
                st.info("Please ensure all model files are in the 'models' directory.")
            except Exception as e:
                st.error(f"❌ Error during prediction: {str(e)}")
                st.info("Please check that all required fields are filled in the User Information tab.")
