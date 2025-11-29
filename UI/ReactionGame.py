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

    # Start button
    if st.button("▶️ Start Game", key="start_reaction"):
        html_game = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Quick Tap Challenge</title>
          <style>
            body { font-family: sans-serif; text-align:center; background-color: #fff; color: #000; }
            #game-area { width: 400px; height: 400px; margin: 20px auto; position: relative; background-color: #f0f0f0; border-radius: 20px; }
            .square { width: 80px; height: 80px; position: absolute; cursor: pointer; border-radius: 10px; background-color: #ff4444; }
            #timer, #score { font-size: 36px; font-weight: bold; margin-top: 10px; }
            #result h2 { color: #0f0; font-weight: bold; }
            button { font-size: 20px; margin: 5px; padding: 5px 10px; }
          </style>
        </head>
        <body>
          <h1>⚡ Quick Tap Challenge</h1>
          <div id="timer">30</div>
          <div id="score">Score: 0</div>
          <div id="game-area"></div>
          <div id="result"></div>

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
              square.style.left = randomPosition().x + "px";
              square.style.top = randomPosition().y + "px";

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

              // Store score in query params so Streamlit can read it
              const normScore = score / 50; // adjust max clicks
              const url = new URL(window.location.href);
              url.searchParams.set("reaction_score", normScore);
              window.history.replaceState({}, '', url);
            }
          </script>
        </body>
        </html>
        """
        components.html(html_game, height=700, scrolling=False)

    st.divider()

    st.subheader("📝 Enter Your Score")

    score = st.number_input(
        "Enter your reaction game score (number of taps):",
        min_value=0,
        max_value=200,
        step=1,
        key="manual_reaction_score"
    )

    if st.button("Save Score"):
        st.session_state["game_scores"]["Reaction"] = score
        st.success(f"✅ Reaction Game score saved: **{score}** points!")

    st.divider()

    # Display saved score if exists
    if "Reaction" in st.session_state["game_scores"]:
        saved = st.session_state["game_scores"]["Reaction"]
        st.info(f"📌 Current saved Reaction score: **{saved}**")