import streamlit as st

# -------------------------
# Import all page render functions
# -------------------------
from UI.Landing import render_landing_page
from UI.UserInput import render_user_input_page
from UI.AboutGames import render_about_games_page
from UI.Game_Memory import render_memory_game
from UI.ReactionGame import render_reaction_game
from UI.TaskSwitchingGame import  render_task_switching_game
from UI.PatternGame import render_pattern_game
# from UI.Results import render_results_page

# -------------------------
# Initialize Session State
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"  # default landing page

# Optional: store user data and game scores in session state
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "game_scores" not in st.session_state:
    st.session_state.game_scores = {
        "Memory": 0,
        "Reaction": 0,
        "TaskSwitch": 0,
        "Pattern": 0
    }

# -------------------------
# Router Logic
# -------------------------
page = st.session_state.page

if page == "Home":
    render_landing_page()

elif page == "User Input":
    render_user_input_page()

elif page == "About the Games":
    render_about_games_page()

# -------------------------
# Uncomment and implement these as you create the games
# -------------------------
elif page == "Memory Game":
    render_memory_game()

elif page == "Reaction Game":
    render_reaction_game()

elif page == "Task Switching Game":
    render_task_switching_game()

elif page == "Pattern Game":
    render_pattern_game()

# elif page == "Results":
#     render_results_page()

# -------------------------
# Optional: Footer for all pages
# -------------------------
st.markdown("---")
st.caption("Alzheimer’s Risk Assessment Tool – Educational & Demonstration Purposes Only")
