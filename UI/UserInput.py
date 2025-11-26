import streamlit as st

def render_user_input_page():
    st.title("Enter Your Basic Information")
    st.subheader("This data will help personalize your Alzheimer's risk assessment.")

    # Initialize user_data dict if not exists
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    # -------------------------
    # Demographics
    # -------------------------
    st.header("Demographic Details")
    age = st.number_input("Age", min_value=60, max_value=90, value=65)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ethnicity = st.selectbox("Ethnicity", ["Caucasian", "African American", "Asian", "Other"])
    education = st.selectbox("Education Level", ["None", "High School", "Bachelor's", "Higher"])

    # -------------------------
    # Lifestyle Factors
    # -------------------------
    st.header("Lifestyle Factors")
    bmi = st.slider("BMI", min_value=15.0, max_value=40.0, value=25.0)
    smoking = st.selectbox("Do you smoke?", ["No", "Yes"])
    alcohol = st.slider("Weekly Alcohol Consumption (units)", 0, 20, 0)
    physical_activity = st.slider("Physical Activity (hours/week)", 0, 10, 3)
    diet_quality = st.slider("Diet Quality (0–10)", 0, 10, 5)
    sleep_quality = st.slider("Sleep Quality (0–10)", 4, 10, 7)

    # -------------------------
    # Medical History
    # -------------------------
    st.header("Medical History")
    family_history = st.selectbox("Family History of Alzheimer's?", ["No", "Yes"])
    cardiovascular = st.selectbox("Cardiovascular Disease?", ["No", "Yes"])
    diabetes = st.selectbox("Diabetes?", ["No", "Yes"])
    depression = st.selectbox("Depression?", ["No", "Yes"])
    head_injury = st.selectbox("History of Head Injury?", ["No", "Yes"])
    hypertension = st.selectbox("Hypertension?", ["No", "Yes"])

    # -------------------------
    # Save Inputs to Session State
    # -------------------------
    if st.button("Proceed to Cognitive Games"):
        st.session_state.user_data = {
            "Age": age,
            "Gender": 0 if gender == "Male" else 1,
            "Ethnicity": ["Caucasian", "African American", "Asian", "Other"].index(ethnicity),
            "Education": ["None", "High School", "Bachelor's", "Higher"].index(education),
            "BMI": bmi,
            "Smoking": 0 if smoking == "No" else 1,
            "AlcoholConsumption": alcohol,
            "PhysicalActivity": physical_activity,
            "DietQuality": diet_quality,
            "SleepQuality": sleep_quality,
            "FamilyHistoryAlzheimers": 0 if family_history == "No" else 1,
            "CardiovascularDisease": 0 if cardiovascular == "No" else 1,
            "Diabetes": 0 if diabetes == "No" else 1,
            "Depression": 0 if depression == "No" else 1,
            "HeadInjury": 0 if head_injury == "No" else 1,
            "Hypertension": 0 if hypertension == "No" else 1
        }
        st.session_state.page = "About the Games"
