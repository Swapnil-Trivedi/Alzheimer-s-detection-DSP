import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import os

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
    report_path = "./data/eda_report.html"  # Path to save the EDA report

    # Check if the HTML report exists
    if os.path.exists(report_path):
        # If the report already exists, load it directly
        with open(report_path, "r") as file:
            report_html = file.read()
        # Create a scrollable container for the EDA report with larger height
        st.components.v1.html(
            report_html, 
            height=1200, 
            scrolling=True  # Enable scrolling
        )
        st.success("EDA Report loaded successfully from saved file!")
    else:
        # If the report doesn't exist, try to generate it
        st.warning("⚠️ Pre-generated EDA report not found.")
        st.info("To generate a new EDA report, install ydata-profiling: `pip install ydata-profiling`")
        
        if st.button("Try to Generate Report"):
            try:
                import ydata_profiling
                # Read the dataset
                df = pd.read_csv(file_path)
                pr = df.profile_report(title="Alzheimer's Disease Data EDA")
                
                # Save the report to an HTML file
                with open(report_path, "w") as f:
                    f.write(pr.to_html())

                # Render the saved HTML report
                st.components.v1.html(
                    pr.to_html(), 
                    height=1200, 
                    scrolling=True  # Enable scrolling
                )
                st.success("EDA Report generated and saved successfully!")
                st.info("💡 Tip: Use the tabs (Overview, Variables, Interactions, etc.) at the top of the report to navigate between sections.")
            
            except ImportError:
                st.error("ydata_profiling is not installed. Install it with: `pip install ydata-profiling`")
            except Exception as e:
                st.error(f"Error generating report: {e}")
