import streamlit as st
import streamlit.components.v1 as components

def render_task_switching_game():
    st.title("🔄 Task Switching Challenge")
    st.subheader("Switch between rules and respond quickly!")

    if "game_scores" not in st.session_state:
        st.session_state["game_scores"] = {}

    st.markdown("""
    **How to play:**  
    1. You will see a **letter or number** in the center of the screen.  
    2. Background color **changes randomly**: Blue or Green.  
       - **Blue**: click if number is even OR letter is a vowel  
       - **Green**: click if number is odd OR letter is a consonant  
    3. Respond **as quickly and accurately** as possible.  
    4. Game lasts **30 seconds** per round.  
    5. Score = number of correct responses.
    """)

    if st.button("▶️ Start Game"):

        html_game = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Task Switching Game</title>
        <style>
            body { font-family:sans-serif; text-align:center; background-color:#f5f5f5; }
            #stimulus { font-size:72px; font-weight:bold; margin-top:50px; padding:50px; border-radius:20px; display:inline-block; cursor:pointer; user-select:none; }
            #score { font-size:24px; font-weight:bold; margin-top:20px; }
            #timer { font-size:20px; margin-top:10px; font-weight:bold; }
            #result h2 { color:#0a0; font-weight:bold; margin-top:20px; }
            button { font-size:20px; margin:5px; padding:5px 10px; }
        </style>
        </head>
        <body>
        <h1>🔄 Task Switching Challenge</h1>
        <div id="score">Score: 0</div>
        <div id="timer">Time Left: 30s</div>
        <div id="stimulus">?</div>
        <div id="result"></div>

        <script>
        const stimulusEl = document.getElementById("stimulus");
        const scoreEl = document.getElementById("score");
        const timerEl = document.getElementById("timer");
        const resultEl = document.getElementById("result");

        let score = 0;
        let timeLeft = 30;
        let gameEnded = false;

        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const vowels = ["A","E","I","O","U"];

        function getRandomStimulus(){
            const isLetter = Math.random() < 0.5;
            if(isLetter){
                const l = letters.charAt(Math.floor(Math.random()*letters.length));
                return {type:"letter", value:l};
            } else {
                const n = Math.floor(Math.random()*9)+1;
                return {type:"number", value:n};
            }
        }

        function getRandomColor(){
            return Math.random() < 0.5 ? "blue" : "green";
        }

        let currentStimulus = {};
        let currentColor = "";

        function showStimulus(){
            if(gameEnded) return;

            currentStimulus = getRandomStimulus();
            currentColor = getRandomColor();

            stimulusEl.innerText = currentStimulus.value;
            stimulusEl.style.backgroundColor = currentColor;
        }

        stimulusEl.addEventListener("click", ()=>{
            if(gameEnded) return;

            let correct = false;
            if(currentColor === "blue"){
                if(currentStimulus.type==="number" && currentStimulus.value%2===0) correct=true;
                if(currentStimulus.type==="letter" && vowels.includes(currentStimulus.value)) correct=true;
            } else if(currentColor==="green"){
                if(currentStimulus.type==="number" && currentStimulus.value%2===1) correct=true;
                if(currentStimulus.type==="letter" && !vowels.includes(currentStimulus.value)) correct=true;
            }

            if(correct) score++;
            scoreEl.innerText = "Score: "+score;
            showStimulus();
        });

        // Countdown timer
        const timerInterval = setInterval(()=>{
            timeLeft--;
            timerEl.innerText = "Time Left: " + timeLeft + "s";
            if(timeLeft<=0){
                clearInterval(timerInterval);
                endGame();
            }
        },1000);

        function endGame(){
            if(gameEnded) return;
            gameEnded = true;
            resultEl.innerHTML = "<h2>Game Over! Your Score: "+score+"</h2>";
            window.parent.postMessage({func:'setScore', value:score, game:'TaskSwitching'}, '*');

            const btnContainer = document.createElement("div");
            btnContainer.style.marginTop = "20px";

            const homeBtn = document.createElement("button");
            homeBtn.innerText = "🏠 Home";
            homeBtn.onclick = () => { window.location.href = "/" };

            const nextBtn = document.createElement("button");
            nextBtn.innerText = "➡️ Next Game";
            nextBtn.style.marginLeft = "10px";
            nextBtn.onclick = () => { window.location.href = "/pages/Game5.py" };

            btnContainer.appendChild(homeBtn);
            btnContainer.appendChild(nextBtn);
            document.body.appendChild(btnContainer);

            stimulusEl.style.pointerEvents = "none";
        }

        // Start first stimulus
        showStimulus();
        </script>
        </body>
        </html>
        """
        components.html(html_game, height=600, scrolling=False)
