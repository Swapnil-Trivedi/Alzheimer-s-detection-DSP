import streamlit as st

def render_about_games_page():
    st.title("Cognitive Games Overview")
    st.subheader("Short 30-second games to assess cognitive abilities related to Alzheimer’s risk.")

    st.markdown("""
    Each game targets a specific cognitive domain often affected early in Alzheimer's disease.  
    Completing all games ensures a more accurate risk evaluation.
    """)

    st.markdown("---")

    # ---------------------------
    # Game 1: Memory Game
    # ---------------------------
    st.header("1. Memory Match Game")
    st.write("""
    **Cognitive Skill:** Short-term memory & pattern recall  
    You will see a sequence of items or a grid of symbols.  
    Your task is to remember and match pairs as quickly as possible.
    Duration: **30 seconds**
    """)

    if st.button("Start Memory Game"):
        st.session_state.page = "Memory Game"

    st.markdown("---")

    # ---------------------------
    # Game 2: Reaction Time
    # ---------------------------
    st.header("2. Reaction Speed Test")
    st.write("""
    **Cognitive Skill:** Alertness & processing speed  
    Click the screen as soon as the color changes or a signal appears.  
    The faster your reaction, the better your score.
    Duration: **30 seconds**
    """)

    if st.button("Start Reaction Game"):
        st.session_state.page = "Reaction Game"

    st.markdown("---")

    # ---------------------------
    # Game 3: Task Switching
    # ---------------------------
    st.header("3. Task Switching Challenge")
    st.write("""
    **Cognitive Skill:** Executive function & mental flexibility  
    You will rapidly switch between different rules (e.g., color vs shape).  
    The game measures your ability to adapt quickly.
    Duration: **30 seconds**
    """)

    if st.button("Start Task Switching Game"):
        st.session_state.page = "Task Switching Game"

    st.markdown("---")

    # ---------------------------
    # Game 4: Pattern Memory
    # ---------------------------
    st.header("4. Pattern Recall Game")
    st.write("""
    **Cognitive Skill:** Working memory & sequential reasoning  
    You will see a pattern or sequence, and must reproduce it.  
    Higher difficulty patterns give higher scores.
    Duration: **30 seconds**
    """)

    if st.button("Start Pattern Game"):
        st.session_state.page = "Pattern Game"

    st.markdown("---")

    st.success("Complete all four games to generate your final cognitive score.")
