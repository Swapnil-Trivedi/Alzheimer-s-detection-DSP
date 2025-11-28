import streamlit as st
import streamlit.components.v1 as components

def render_reaction_game():
    st.title("⚡ Quick Tap Challenge")
    st.subheader("Click the red square as fast as you can in 30 seconds!")

    if "game_scores" not in st.session_state:
        st.session_state["game_scores"] = {}

    st.markdown("""
    **How to play:**  
    1. A red square will appear randomly inside the arena.  
    2. Click it as quickly as possible. Each click gives 1 point.  
    3. The game lasts 30 seconds. Try to get as many points as possible!  
    """)

    if st.button("▶️ Start Game",key="reaction_start"):
        html_game = """
        <div id="game-container" style="text-align:center; background-color:#fff; padding:20px; border-radius:10px;">
            <h2>⚡ Quick Tap Challenge</h2>
            <div id="timer">30</div>
            <div id="score">Score: 0</div>
            <div id="game-area" style="width:400px;height:400px;margin:20px auto;position:relative;background:#f0f0f0;border-radius:20px;"></div>
            <div id="result" style="margin-top:20px;"></div>
        </div>

        <script>
            const gameArea = document.getElementById("game-area");
            let score = 0;
            let time = 30;

            function randomPosition() {
                const x = Math.random() * (gameArea.clientWidth - 80);
                const y = Math.random() * (gameArea.clientHeight - 80);
                return {x, y};
            }

            function spawnSquare() {
                const square = document.createElement("div");
                square.className = "square";
                square.style.width = "80px";
                square.style.height = "80px";
                square.style.position = "absolute";
                square.style.borderRadius = "10px";
                square.style.backgroundColor = "#ff4444";
                square.style.cursor = "pointer";
                const pos = randomPosition();
                square.style.left = pos.x + "px";
                square.style.top = pos.y + "px";

                square.onclick = () => {
                    score++;
                    document.getElementById("score").innerText = "Score: " + score;
                    gameArea.removeChild(square);
                    spawnSquare();
                };

                gameArea.appendChild(square);
            }

            spawnSquare();

            const timerInterval = setInterval(() => {
                time--;
                document.getElementById("timer").innerText = time;
                if (time <= 0) {
                    clearInterval(timerInterval);
                    endGame();
                }
            }, 1000);

            function endGame() {
                gameArea.innerHTML = "";
                document.getElementById("result").innerHTML = "<h2>Game Over! Score: " + score + "</h2>";

                // Normalize score (max possible clicks can vary, let's assume 50 clicks as a reference)
                const normScore = Math.min(score / 50, 1.0);
                window.parent.postMessage({func:'setScore', value:normScore, game:'Reaction'}, '*');
            }
        </script>
        """
        components.html(html_game, height=700, scrolling=False)
