import streamlit as st
from UI.Landing import render_landing_page
from UI.UserInput import render_user_input_page
from UI.AboutGames import render_about_games_page
from UI.Game_Memory import render_memory_game
from UI.ReactionGame import render_reaction_game
from UI.TaskSwitchingGame import render_task_switching_game
from UI.PatternGame import render_pattern_game
from UI.ResultsPage import render_results_page
from UI.EdaProfileReport import render_eda_tab
import streamlit.components.v1 as components

# ---------------------------------------------
# Session State Initialization
# ---------------------------------------------
def init_session_state():
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    if "game_scores" not in st.session_state:
        st.session_state.game_scores = {
            "Memory": 0,
            "Reaction": 0,
            "TaskSwitch": 0,
            "Pattern": 0
        }

    if "model_output" not in st.session_state:
        st.session_state.model_output = None

init_session_state()

# ---------------------------------------------
# Page Layout
# ---------------------------------------------
st.set_page_config(
    page_title="Alzheimer's Cognitive Assessment",
    layout="wide",
)

# st.title("🧠 Alzheimer’s Cognitive Assessment Dashboard")
# st.write(
#     "Welcome! Navigate through each step to complete the assessment, "
#     "play cognitive games, and view your AI-powered results."
# )
 # --------------------------------
    # Header
    # --------------------------------
st.markdown(
        """
        <h1 style="text-align:center;">🧠 Alzheimer’s Risk Assessment</h1>
        <h3 style="text-align:center; color:#666;">
            Interactive Cognitive Games + Clinical Risk Factors
        </h3>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------
# Main Navigation Tabs
# ---------------------------------------------
tabs = st.tabs([
    "🏠 Home",
    "📊 Exploratory Data Analysis",
    "👤 User Information",
    "🎮 About the Games",
    "🧩 Memory",
    "⚡ Reaction",
    "🔄 Task Switching",
    "🔢 Pattern Game",
    "📊 Results"
])

with tabs[0]:
    render_landing_page()
with tabs[1]:
    render_eda_tab()
with tabs[2]:
    render_user_input_page()
with tabs[3]:
    render_about_games_page()
with tabs[4]:
    render_memory_game()
with tabs[5]:
    render_reaction_game()
with tabs[6]:
    render_task_switching_game()
with tabs[7]:
    render_pattern_game()
with tabs[8]:
    render_results_page()

# ---------------------------------------------
# Global Footer
# ---------------------------------------------
st.markdown("---")
st.caption("Alzheimer’s Risk Assessment Tool – Educational Use Only")
