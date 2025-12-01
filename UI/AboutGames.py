import streamlit as st

def render_about_games_page():
    st.markdown(
        """
        # 🧩 Cognitive Games Overview
        Short, 30-second interactive games designed to assess cognitive abilities
        related to Alzheimer's risk.

        Completing all games provides a **comprehensive evaluation of memory,
        attention, and executive function**, which are key cognitive domains
        affected in early stages.
        """
    )

    st.markdown("---")

    # ---------------------------
    # Arrange games in 2 columns
    # ---------------------------
    col1, col2 = st.columns(2)

    # ---------------------------
    # Column 1: Game 1 & Game 2
    # ---------------------------
    with col1:
        st.header("1️⃣ Memory Match Game")
        st.markdown(
            """
            **Cognitive Skill:** Short-term memory & pattern recall

            **Instructions:**
            - Memorize pairs in a grid of cards or symbols.  
            - Match them as quickly as possible.  
            - Duration: **30 seconds**

            **Tips:**
            - Accuracy over speed initially.
            """
        )

        st.markdown("---")

        st.header("3️⃣ Reaction Speed Test")
        st.markdown(
            """
            **Cognitive Skill:** Alertness & processing speed

            **Instructions:**
            - Click as soon as a signal appears (color change or symbol).  
            - Duration: **30 seconds**

            **Tips:**
            - Keep your eyes on the screen.  
            - Stay relaxed for faster reactions.
            """
        )

    # ---------------------------
    # Column 2: Game 3 & Game 4
    # ---------------------------
    with col2:
        st.header("2️⃣ Task Switching Challenge")
        st.markdown(
            """
            **Cognitive Skill:** Executive function & mental flexibility

            **Instructions:**
            - Switch rapidly between different rules (color vs shape).  
            - Duration: **30 seconds**

            **Tips:**
            - Read each rule carefully.  
            - Balance speed and accuracy.
            """
        )

        st.markdown("---")

        st.header("4️⃣ Pattern Recall Game")
        st.markdown(
            """
            **Cognitive Skill:** Working memory & sequential reasoning

            **Instructions:**
            - Observe a pattern or sequence and reproduce it.  
            - Difficulty increases with each round.  
            - Duration: **30 seconds**

            **Tips:**
            - Visualize the pattern carefully.  
            - Focus on one sequence at a time.
            """
        )

    st.markdown("---")
    st.success(
        "✅ Complete all four games to generate your **final cognitive score**. "
        "Follow instructions carefully and enjoy the interactive assessment!"
    )
