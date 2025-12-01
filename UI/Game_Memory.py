import streamlit as st
import streamlit.components.v1 as components

def render_memory_game():
    st.title("🧩 Memory Match Game")
    st.subheader("Memorize and match as many pairs as you can in 30 seconds!")

    if "game_scores" not in st.session_state:
        st.session_state["game_scores"] = {}

    # Instructions
    st.markdown("""
    **How to play:**  
    1. All cards will be shown for 5 seconds to memorize.  
    2. Once cards are hidden, you have 30 seconds to match all pairs.  
    3. Click on two cards to reveal them. Matching pairs stay revealed, otherwise they hide again.  
    4. Try to match as many pairs as possible!  
    """)

    # Start button
    if st.button("▶️ Start Game", key="start_memory"):
        html_game = """
        <div id="game-container" style="text-align:center; background-color:#fff; padding:20px; border-radius:10px;">
            <h2>🧩 Memory Match</h2>
            <div id="timer" style="font-size:28px; font-weight:bold;">Get Ready!</div>
            <div id="grid" style="display:grid; grid-template-columns:repeat(4,100px); gap:10px; justify-content:center; margin-top:20px;"></div>
            <div id="result" style="margin-top:20px;"></div>
        </div>

        <script>
        const symbols = ["🍎","🍌","🍇","🍓","🍒","🥝","🍍","🥭"];
        let cards = symbols.concat(symbols).sort(() => 0.5 - Math.random());

        const grid = document.getElementById("grid");
        let firstCard = null;
        let secondCard = null;
        let matches = 0;
        let memTime = 5;
        let gameTime = 30;

        function createGrid() {
            grid.innerHTML = "";
            cards.forEach(symbol => {
                const card = document.createElement("div");
                card.className = "card";
                card.dataset.symbol = symbol;
                card.style.width = "100px";
                card.style.height = "100px";
                card.style.display = "flex";
                card.style.alignItems = "center";
                card.style.justifyContent = "center";
                card.style.fontSize = "50px";
                card.style.background = "#ddd";
                card.style.color = "#000";
                card.style.borderRadius = "10px";
                card.style.cursor = "pointer";
                card.innerHTML = symbol;
                grid.appendChild(card);
            });
        }

        createGrid();

        let memInterval = setInterval(() => {
            document.getElementById("timer").innerText = "Memorize: " + memTime + "s";
            memTime--;
            if(memTime < 0){
                clearInterval(memInterval);
                document.querySelectorAll(".card").forEach(c => c.innerHTML = "❓");
                startGame();
            }
        }, 1000);

        function startGame(){
            const cardDivs = document.querySelectorAll(".card");
            const gameInterval = setInterval(() => {
                document.getElementById("timer").innerText = "Time Left: " + gameTime + "s";
                gameTime--;
                if(gameTime < 0 || matches === 8){
                    clearInterval(gameInterval);
                    endGame();
                }
            }, 1000);

            cardDivs.forEach(card => {
                card.addEventListener("click", () => {
                    if(card.innerHTML !== "❓") return;
                    card.innerHTML = card.dataset.symbol;

                    if(!firstCard){
                        firstCard = card;
                    } else if(!secondCard){
                        secondCard = card;
                        if(firstCard.dataset.symbol === secondCard.dataset.symbol){
                            matches++;
                            firstCard = null;
                            secondCard = null;
                            if(matches === 8) endGame();
                        } else {
                            setTimeout(() => {
                                firstCard.innerHTML = "❓";
                                secondCard.innerHTML = "❓";
                                firstCard = null;
                                secondCard = null;
                            }, 200);
                        }
                    }
                });
            });
        }

        function endGame(){
            document.getElementById("result").innerHTML = "<h3>Game Over! You matched " + matches + " pairs.</h3>";
            const normScore = matches / 8;
            const url = new URL(window.location.href);
            url.searchParams.set("memory_score", normScore);
            window.history.replaceState({}, '', url);
        }
        </script>
        """
        components.html(html_game, height=750, scrolling=False)

    # Capture score from query params and store in session state
    st.subheader("Enter Your Score Manually")

    memory_input = st.number_input(
        "How many pairs did you match? (0–8)",
        min_value=0, max_value=8, step=1
    )

    if st.button("Save Memory Score"):
        st.session_state["game_scores"]["Memory"] = int(memory_input)
        st.success(f"Memory Game score saved: {memory_input} pairs!")