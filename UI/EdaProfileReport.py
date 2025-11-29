import streamlit as st
import pandas as pd
import ydata_profiling 
from streamlit_pandas_profiling import st_profile_report

# Function to render EDA (Exploratory Data Analysis) tab
def render_eda_tab():
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.markdown("""
       This section provides an exploratory data analysis (EDA) report of the raw dataset
       used for training the Alzheimer's risk prediction model. The report includes statistical
       summaries, distributions, correlations, and other insights about the dataset features.  
    """)

    # Define the file path (make sure to place your file in the root directory of your project)
    file_path = "./data/alzheimers_disease_data.csv"  # Update with your actual file path (e.g., "data/my_data.csv")

    # Read the dataset
    try:
        df = pd.read_csv(file_path)
        pr=df.profile_report()
        st_profile_report(pr)
        st.success("EDA Report generated successfully!")

    except Exception as e:
        st.error(f"Error reading file: {e}")
