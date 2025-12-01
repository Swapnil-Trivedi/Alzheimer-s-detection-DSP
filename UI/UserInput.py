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
    
    # Initialize manual cognitive input flag
    if "manual_cognitive_input" not in st.session_state:
        st.session_state.manual_cognitive_input = False

    # --------------------------------------
    # Cognitive Assessment Toggle (outside form for immediate response)
    # --------------------------------------
    st.markdown("### 🧠 Cognitive Assessment Options")
    st.info("🎮 **Option 1 (Recommended):** Play the cognitive games in the tabs above, and we'll calculate scores automatically based on your performance.")
    st.markdown("**Option 2:** If you have clinical cognitive test results, you can enter them manually:")
    
    use_manual_cognitive = st.checkbox("I have clinical cognitive test results to enter manually", 
                                        value=st.session_state.manual_cognitive_input,
                                        key="manual_cognitive_checkbox")
    
    # Update session state when checkbox changes
    st.session_state.manual_cognitive_input = use_manual_cognitive
    
    st.markdown("---")

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
            age = st.number_input("Age", min_value=18, max_value=90, step=1)

        with col2:
            gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

        col_eth, col_edu = st.columns(2)
        
        with col_eth:
            ethnicity = st.selectbox(
                "Ethnicity",
                ["Caucasian", "African American", "Asian", "Other"]
            )

        with col_edu:
            education = st.slider(
                "Education Level (years)",
                min_value=0, max_value=20, value=12, step=1,
                help="Years of formal education completed"
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
        # Clinical Measurements
        # -------------------------
        st.markdown("### 🩺 Clinical Measurements")
        st.info("💡 These are medical test results. If you don't have recent lab results, you can use typical healthy ranges.")

        col8, col9, col10 = st.columns(3)

        with col8:
            systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=90, max_value=180, value=120)
            diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=60, max_value=120, value=80)

        with col9:
            cholesterol_total = st.number_input("Total Cholesterol (mg/dL)", min_value=150, max_value=300, value=200)
            cholesterol_ldl = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=200, value=100)

        with col10:
            cholesterol_hdl = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
            cholesterol_triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=400, value=150)

        st.markdown("---")

        # -------------------------
        # Cognitive Assessment - Manual Entry (if toggled)
        # -------------------------
        if st.session_state.manual_cognitive_input:
            col11, col12 = st.columns(2)

            with col11:
                mmse = st.slider("MMSE Score", min_value=0, max_value=30, value=28, 
                               help="Mini-Mental State Examination (0-30, higher is better)")
                functional_assessment = st.slider("Functional Assessment", min_value=0, max_value=10, value=8,
                                                help="Overall functional ability (0-10)")
                adl = st.slider("Activities of Daily Living (ADL)", min_value=0, max_value=10, value=8,
                              help="Ability to perform daily tasks (0-10)")

            with col12:
                memory_complaints = st.radio("Memory Complaints?", ["No", "Yes"], horizontal=True)
                behavioral_problems = st.radio("Behavioral Problems?", ["No", "Yes"], horizontal=True)
                confusion = st.radio("Confusion?", ["No", "Yes"], horizontal=True)

            col13, col14 = st.columns(2)

            with col13:
                disorientation = st.radio("Disorientation?", ["No", "Yes"], horizontal=True)
                personality_changes = st.radio("Personality Changes?", ["No", "Yes"], horizontal=True)

            with col14:
                difficulty_tasks = st.radio("Difficulty Completing Tasks?", ["No", "Yes"], horizontal=True)
                forgetfulness = st.radio("Forgetfulness?", ["No", "Yes"], horizontal=True)
            
            st.markdown("---")
        else:
            # Set defaults - these will be overridden by game scores
            mmse = None
            functional_assessment = None
            adl = None
            memory_complaints = "No"
            behavioral_problems = "No"
            confusion = "No"
            disorientation = "No"
            personality_changes = "No"
            difficulty_tasks = "No"
            forgetfulness = "No"

        # -------------------------
        # Submit Button
        # -------------------------
        submitted = st.form_submit_button("Save Information")

        if submitted:
            # Store base user data (demographics, lifestyle, medical, clinical)
            user_data = {
                "Age": age,
                "Gender": 0 if gender == "Male" else 1,
                "Ethnicity": ["Caucasian", "African American", "Asian", "Other"].index(ethnicity),
                "EducationLevel": int(education),

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
                "Hypertension": 0 if hypertension == "No" else 1,

                "SystolicBP": int(systolic_bp),
                "DiastolicBP": int(diastolic_bp),
                "CholesterolTotal": int(cholesterol_total),
                "CholesterolLDL": int(cholesterol_ldl),
                "CholesterolHDL": int(cholesterol_hdl),
                "CholesterolTriglycerides": int(cholesterol_triglycerides),
            }
            
            # Add manual cognitive scores if provided
            if st.session_state.manual_cognitive_input:
                user_data.update({
                    "MMSE": int(mmse),
                    "FunctionalAssessment": int(functional_assessment),
                    "MemoryComplaints": 0 if memory_complaints == "No" else 1,
                    "BehavioralProblems": 0 if behavioral_problems == "No" else 1,
                    "ADL": int(adl),
                    "Confusion": 0 if confusion == "No" else 1,
                    "Disorientation": 0 if disorientation == "No" else 1,
                    "PersonalityChanges": 0 if personality_changes == "No" else 1,
                    "DifficultyCompletingTasks": 0 if difficulty_tasks == "No" else 1,
                    "Forgetfulness": 0 if forgetfulness == "No" else 1
                })
            
            st.session_state.user_data = user_data

            if st.session_state.manual_cognitive_input:
                st.success("✅ Your information has been saved with manual cognitive scores. You may now proceed to the Results tab.")
            else:
                st.success("✅ Your information has been saved. Please play the cognitive games in the tabs above to complete your assessment!")
            
            print(st.session_state.user_data)