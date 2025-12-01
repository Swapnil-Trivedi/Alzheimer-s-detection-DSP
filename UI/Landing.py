import streamlit as st

def render_landing_page():
    st.markdown(
        """
        Welcome to the **Alzheimer’s Risk Assessment Tool** — an interactive system that blends:

        - 🧬 **Clinical and lifestyle data**
        - 🎮 **30-second cognitive mini-games**
        - 🤖 **Predictive machine learning models**

        This project demonstrates a modern, engaging approach to early cognitive decline detection by combining
        traditional clinical indicators with gamified digital biomarkers.
        """
    )

    st.markdown("---")

    # --------------------------------
    # Dataset Overview (Collapsible)
    # --------------------------------
    st.header("📊 Dataset Overview")
    st.write(
        "The model is trained on a dataset of adults aged **60–90**, "
        "including demographic, lifestyle, clinical, and cognitive information. "
        "Explore the key feature categories below:"
    )

    with st.expander("👤 Demographic Details"):
        st.markdown(
            """
            - **Age** (60–90)  
            - **Gender**: 0 = Male, 1 = Female  
            - **Ethnicity**:  
                - 0 = Caucasian  
                - 1 = African American  
                - 2 = Asian  
                - 3 = Other  
            - **Education Level**: 0 (None) → 3 (Higher)
            """
        )

    with st.expander("🏃 Lifestyle Factors"):
        st.markdown(
            """
            - **BMI**: 15–40  
            - **Smoking**: 0/1  
            - **Alcohol Consumption**: 0–20 units/week  
            - **Physical Activity**: 0–10 hours/week  
            - **Diet Quality**: 0–10  
            - **Sleep Quality**: 4–10  
            """
        )

    with st.expander("🩺 Medical History"):
        st.markdown(
            """
            - Family history of Alzheimer's  
            - Cardiovascular disease  
            - Hypertension  
            - Diabetes  
            - Depression  
            - Head injury  
            *(all encoded as 0/1)*
            """
        )

    with st.expander("📈 Clinical Measurements"):
        st.markdown(
            """
            **Blood Pressure**
            - Systolic: 90–180  
            - Diastolic: 60–120  

            **Cholesterol**
            - Total: 150–300  
            - LDL: 50–200  
            - HDL: 20–100  
            - Triglycerides: 50–400  
            """
        )

    with st.expander("🧩 Cognitive & Symptom Assessments"):
        st.markdown(
            """
            - **MMSE**: 0–30  
            - **Functional Assessment**: 0–10  
            - **Daily Living Score**: 0–10  
            - **Memory complaints**: 0/1  
            - **Behavioral issues**: 0/1  
            - Symptoms like confusion, forgetfulness, disorientation
            """
        )
