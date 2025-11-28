import streamlit as st

def render_user_input_page():
    st.markdown("## 👤 User Information")
    st.write(
        "Please provide the following information. "
        "**Your data is used only locally for generating your risk assessment** and is not stored externally."
    )

    # Ensure session state exists
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    # --------------------------------------
    # Use a structured form to avoid clutter
    # --------------------------------------
    with st.form("user_info_form"):

        # -------------------------
        # Demographics
        # -------------------------
        st.markdown("### 📌 Demographic Details")
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=60, max_value=90, step=1)

        with col2:
            gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

        ethnicity = st.selectbox(
            "Ethnicity",
            ["Caucasian", "African American", "Asian", "Other"]
        )

        education = st.selectbox(
            "Highest Education Level",
            ["None", "High School", "Bachelor's", "Higher"]
        )

        st.markdown("---")

        # -------------------------
        # Lifestyle Factors
        # -------------------------
        st.markdown("### 🏃 Lifestyle Factors")

        col3, col4 = st.columns(2)

        with col3:
            bmi = st.number_input("BMI", min_value=15.0, max_value=40.0, format="%.1f")
            alcohol = st.number_input("Weekly Alcohol Consumption (units)", min_value=0, max_value=20)
            physical_activity = st.number_input("Physical Activity (hours/week)", min_value=0, max_value=10)

        with col4:
            smoking = st.radio("Do you smoke?", ["No", "Yes"], horizontal=True)
            diet_quality = st.number_input("Diet Quality (0–10)", min_value=0, max_value=10)
            sleep_quality = st.number_input("Sleep Quality (0–10)", min_value=4, max_value=10)

        st.markdown("---")

        # -------------------------
        # Medical History
        # -------------------------
        st.markdown("### 🩺 Medical History")

        col5, col6, col7 = st.columns(3)

        with col5:
            family_history = st.radio("Family History of Alzheimer's?", ["No", "Yes"])
            cardiovascular = st.radio("Cardiovascular Disease?", ["No", "Yes"])

        with col6:
            diabetes = st.radio("Diabetes?", ["No", "Yes"])
            depression = st.radio("Depression?", ["No", "Yes"])

        with col7:
            head_injury = st.radio("History of Head Injury?", ["No", "Yes"])
            hypertension = st.radio("Hypertension?", ["No", "Yes"])

        st.markdown("---")

        # -------------------------
        # Submit Button
        # -------------------------
        submitted = st.form_submit_button("Save Information")

        if submitted:
            st.session_state.user_data = {
                "Age": age,
                "Gender": 0 if gender == "Male" else 1,
                "Ethnicity": ["Caucasian", "African American", "Asian", "Other"].index(ethnicity),
                "Education": ["None", "High School", "Bachelor's", "Higher"].index(education),

                "BMI": float(bmi),
                "Smoking": 0 if smoking == "No" else 1,
                "AlcoholConsumption": int(alcohol),
                "PhysicalActivity": int(physical_activity),
                "DietQuality": int(diet_quality),
                "SleepQuality": int(sleep_quality),

                "FamilyHistoryAlzheimers": 0 if family_history == "No" else 1,
                "CardiovascularDisease": 0 if cardiovascular == "No" else 1,
                "Diabetes": 0 if diabetes == "No" else 1,
                "Depression": 0 if depression == "No" else 1,
                "HeadInjury": 0 if head_injury == "No" else 1,
                "Hypertension": 0 if hypertension == "No" else 1
            }

            st.success("Your information has been saved. You may now proceed to the cognitive games using the tabs above.")
