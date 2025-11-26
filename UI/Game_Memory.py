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
    2. A negative countdown shows how long until cards hide.  
    3. Once cards are hidden, you have 30 seconds to match all pairs.  
    4. Click on two cards to reveal them. Matching pairs stay revealed, otherwise they hide again.  
    5. Try to match as many pairs as you can!
    """)

    if st.button("▶️ Start Game"):
        html_game = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Memory Game</title>
          <style>
            body { 
              font-family: sans-serif; 
              text-align:center; 
              background-color: #000; 
              color: #fff; 
            }
            #grid { 
              display: grid; 
              grid-template-columns: repeat(4, 100px); 
              grid-gap: 10px; 
              justify-content:center; 
              margin-top:20px; 
            }
            .card { 
              font-size: 60px; 
              width:100px; 
              height:100px; 
              display:flex; 
              align-items:center; 
              justify-content:center; 
              background:#444; 
              cursor:pointer; 
              border-radius:10px; 
              color: #fff; 
              font-weight: bold;
            }
            #timer { 
              font-size: 28px; 
              margin-top:10px; 
              font-weight: bold;
            }
            #result h2 {
              color: #0f0; 
              font-weight: bold;
            }
          </style>
        </head>
        <body>
          <h1>🧩 Memory Match Game</h1>
          <p>Memorize and match all pairs!</p>
          <div id="timer">-5</div>
          <div id="grid"></div>
          <div id="result"></div>

          <script>
            const symbols = ["🍎","🍌","🍇","🍓","🍒","🥝","🍍","🥭"];
            let cards = symbols.concat(symbols);
            cards.sort(() => 0.5 - Math.random());

            const grid = document.getElementById("grid");
            let firstCard = null;
            let secondCard = null;
            let matches = 0;
            let timer = 30;
            let memCountdown = -5;

            function createGrid() {
              grid.innerHTML = "";
              for (let i=0; i<cards.length; i++){
                const card = document.createElement("div");
                card.className = "card";
                card.dataset.symbol = cards[i];
                card.innerHTML = cards[i]; // memorization phase
                grid.appendChild(card);
              }
            }

            function startGame() {
              const cardDivs = document.querySelectorAll(".card");

              const memInterval = setInterval(() => {
                document.getElementById("timer").innerText = memCountdown;
                memCountdown++;
                if (memCountdown > 0) {
                  clearInterval(memInterval);
                  cardDivs.forEach(c => c.innerHTML = "❓");

                  const gameInterval = setInterval(() => {
                    timer--;
                    document.getElementById("timer").innerText = timer;
                    if (timer <= 0 || matches === 8){
                      clearInterval(gameInterval);
                      endGame();
                    }
                  }, 1000);
                }
              }, 1000);

              cardDivs.forEach(card => {
                card.addEventListener("click", () => {
                  if (memCountdown <= 0) return;
                  if (card.innerHTML !== "❓") return;
                  card.innerHTML = card.dataset.symbol;
                  if (!firstCard){
                    firstCard = card;
                  } else if (!secondCard){
                    secondCard = card;
                    if (firstCard.dataset.symbol === secondCard.dataset.symbol){
                      matches++;
                      firstCard = null;
                      secondCard = null;
                      if (matches === 8) endGame();
                    } else {
                      setTimeout(()=>{
                        firstCard.innerHTML = "❓";
                        secondCard.innerHTML = "❓";
                        firstCard = null;
                        secondCard = null;
                      }, 1000);
                    }
                  }
                });
              });
            }

            function endGame() {
              document.getElementById("result").innerHTML = "<h2>Game Over! You matched " + matches + " pairs.</h2>";
              // send score to Streamlit session_state
              const scoreDiv = document.createElement("div");
              scoreDiv.id = "scoreDiv";
              scoreDiv.innerText = matches;
              document.body.appendChild(scoreDiv);
              window.parent.postMessage({func: 'setScore', value: matches}, '*');

              // Add navigation buttons
              const btnContainer = document.createElement("div");
              btnContainer.style.marginTop = "20px";

              const homeBtn = document.createElement("button");
              homeBtn.innerText = "Home";
              homeBtn.style.fontSize = "20px";
              homeBtn.onclick = () => { window.location.href = "/" };

              const nextBtn = document.createElement("button");
              nextBtn.innerText = "Next Game";
              nextBtn.style.fontSize = "20px";
              nextBtn.style.marginLeft = "10px";
              nextBtn.onclick = () => { window.location.href = "/pages/Game2.py" }; // Adjust path

              btnContainer.appendChild(homeBtn);
              btnContainer.appendChild(nextBtn);
              document.body.appendChild(btnContainer);
            }

            createGrid();
            startGame();
          </script>
        </body>
        </html>
        """
        components.html(html_game, height=750, scrolling=False)
