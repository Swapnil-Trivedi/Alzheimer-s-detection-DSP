import streamlit as st

def render_landing_page():
    # -------------------------
    # Page Configuration
    # -------------------------
    st.set_page_config(
        page_title="Alzheimer’s Risk Assessment",
        page_icon="🧠",
        layout="wide"
    )

    # -------------------------
    # Main Landing Page
    # -------------------------
    st.title("Alzheimer’s Risk Assessment")
    st.subheader("Interactive Cognitive Games + Clinical Risk Factors")

    st.markdown("""
    Welcome to the **Alzheimer’s Risk Assessment Tool** — an interactive system that combines **user-provided health and lifestyle information** 
    with **30-second cognitive mini-games** to estimate potential cognitive decline risk.

    This project demonstrates a modern approach to early detection by blending **machine learning**, **clinical features**, 
    and **gamified cognitive testing**.
    """)

    st.markdown("---")

    # -------------------------
    # Dataset Overview Section
    # -------------------------
    st.header("Dataset Overview")

    st.markdown("""
    The model is trained on a dataset of patients aged **60–90**, containing demographic, lifestyle, medical, and cognitive information.
    Below is a breakdown of the key data categories used in the assessment.
    """)

    # --- Category 1: Demographic Details ---
    with st.expander("Demographic Details"):
        st.markdown("""
        - **Age (60–90)**  
        - **Gender**: 0 = Male, 1 = Female  
        - **Ethnicity**: 0 = Caucasian, 1 = African American, 2 = Asian, 3 = Other  
        - **Education Level**:  
            - 0 = None  
            - 1 = High School  
            - 2 = Bachelor's  
            - 3 = Higher  
        """)

    # --- Category 2: Lifestyle Factors ---
    with st.expander("Lifestyle Factors"):
        st.markdown("""
        - **BMI**: 15–40  
        - **Smoking**: 0 = No, 1 = Yes  
        - **Alcohol Consumption**: 0–20 units/week  
        - **Physical Activity**: 0–10 hours/week  
        - **Diet Quality**: 0–10  
        - **Sleep Quality**: 4–10  
        """)

    # --- Category 3: Medical History ---
    with st.expander("Medical History"):
        st.markdown("""
        - **Family History of Alzheimer's**: 0 = No, 1 = Yes  
        - **Cardiovascular Disease**: 0 = No, 1 = Yes  
        - **Diabetes**: 0 = No, 1 = Yes  
        - **Depression**: 0 = No, 1 = Yes  
        - **Head Injury**: 0 = No, 1 = Yes  
        - **Hypertension**: 0 = No, 1 = Yes  
        """)

    # --- Category 4: Clinical Measurements ---
    with st.expander("Clinical Measurements"):
        st.markdown("""
        - **Blood Pressure**  
            - Systolic: 90–180  
            - Diastolic: 60–120  
        - **Cholesterol Levels**  
            - Total: 150–300 mg/dL  
            - LDL: 50–200 mg/dL  
            - HDL: 20–100 mg/dL  
            - Triglycerides: 50–400 mg/dL  
        """)

    # --- Category 5: Cognitive & Symptom Assessments ---
    with st.expander("Cognitive & Functional Indicators"):
        st.markdown("""
        - **MMSE**: 0–30 (lower = impairment)  
        - **Functional Assessment**: 0–10  
        - **ADL (Daily Living Score)**: 0–10  
        - **Memory Complaints**: 0/1  
        - **Behavioral Problems**: 0/1  
        - **Symptoms**: Confusion, Disorientation, Forgetfulness, etc.  
        """)

    st.markdown("---")

    # -------------------------
    # Navigation Buttons (Session-State Routing)
    # -------------------------
    col1, col2 = st.columns(2)

    # Initialize page state if not exists
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    with col1:
        st.success("Begin the interactive assessment including 30-second cognitive games.")
        if st.button("Start Assessment"):
            st.session_state.page = "User Input"

    with col2:
        st.info("Learn more about the cognitive mini-games and how they contribute to risk scoring.")
        if st.button("Learn About the Games"):
            st.session_state.page = "About the Games"

    # -------------------------
    # Footer
    # -------------------------
    st.markdown("---")
    st.caption("This tool is for demonstration and educational purposes only and is not a medical diagnostic system.")
