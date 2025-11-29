import streamlit as st
import streamlit.components.v1 as components

def render_pattern_game():
    st.title("🎨 Memory Pattern Challenge")
    st.subheader("Remember the numbers and click tiles in ascending order!")

    if "game_scores" not in st.session_state:
        st.session_state["game_scores"] = {}

    st.markdown("""
    **How to play:**  
    1. Four horizontal colored tiles are shown, each with a number 1–4 randomly assigned.  
    2. Numbers are visible for **5 seconds**, then disappear.  
    3. Click the tiles in **ascending order** from memory.  
    4. Game ends if you click the wrong tile.  
    5. Score = number of rounds successfully completed.
    """)

    if st.button("▶️ Start Game", key="start_pattern"):
        html_game = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Memory Pattern Challenge</title>
        <style>
            body { font-family: sans-serif; text-align:center; background-color:#f5f5f5; color:#000; }
            #game-area { display:flex; justify-content:center; margin-top:30px; }
            .tab { width:120px; height:120px; margin:10px; border-radius:15px; font-size:36px; font-weight:bold; color:#fff; display:flex; align-items:center; justify-content:center; cursor:pointer; user-select:none; }
            #tab0 { background-color:#ff4444; } 
            #tab1 { background-color:#44ff44; } 
            #tab2 { background-color:#4444ff; } 
            #tab3 { background-color:#ffbb33; } 
            #score { font-size:24px; font-weight:bold; margin-top:20px; }
            #timer { font-size:20px; margin-top:10px; font-weight:bold; }
            #result h2 { color:#0a0; font-weight:bold; }
            button { font-size:20px; margin:5px; padding:5px 10px; }
        </style>
        </head>
        <body>
        <h1>🎨 Memory Pattern Challenge</h1>
        <div id="score">Round: 0</div>
        <div id="timer"></div>
        <div id="game-area">
            <div class="tab" id="tab0">1</div>
            <div class="tab" id="tab1">2</div>
            <div class="tab" id="tab2">3</div>
            <div class="tab" id="tab3">4</div>
        </div>
        <div id="result"></div>

        <script>
        const tabs = [0,1,2,3];
        let round = 0;
        let expectedOrder = [];
        let gameEnded = false;

        const scoreDiv = document.getElementById("score");
        const timerDiv = document.getElementById("timer");

        function shuffleNumbers(){
            const numbers = [1,2,3,4];
            for(let i=numbers.length-1;i>0;i--){
                const j = Math.floor(Math.random()*(i+1));
                [numbers[i],numbers[j]] = [numbers[j], numbers[i]];
            }
            return numbers;
        }

        function startRound(){
            if(gameEnded) return;

            round++;
            scoreDiv.innerText = "Round: " + round;
            const nums = shuffleNumbers();
            expectedOrder = nums.slice().sort((a,b)=>a-b);

            tabs.forEach((id,i)=>{
                const tab = document.getElementById("tab"+id);
                tab.innerText = nums[i];
                tab.style.pointerEvents = "none"; // disable clicks during timer
                tab.setAttribute("data-num", nums[i]);
            });

            let countdown = 5;
            timerDiv.innerText = "Memorize numbers: " + countdown + "s";

            const timerInterval = setInterval(()=>{
                countdown--;
                if(countdown>0){
                    timerDiv.innerText = "Memorize numbers: " + countdown + "s";
                } else {
                    clearInterval(timerInterval);
                    timerDiv.innerText = "Now click in ascending order!";
                    tabs.forEach((id)=>{
                        document.getElementById("tab"+id).innerText = "";
                        document.getElementById("tab"+id).style.pointerEvents = "auto";
                    });
                }
            },1000);
        }

        function endGame(){
            if(gameEnded) return;
            gameEnded = true;

            const roundsCompleted = round-1;
            document.getElementById("result").innerHTML = "<h2>Game Over! Rounds completed: "+roundsCompleted+"</h2>";
            
            // Send score to Streamlit
            window.parent.postMessage({func:'setScore', value:roundsCompleted, game:'MemoryPattern'}, '*');

            tabs.forEach((id)=>{
                document.getElementById("tab"+id).style.pointerEvents = "none";
            });
        }

        tabs.forEach((id)=>{
            document.getElementById("tab"+id).addEventListener("click", ()=>{
                if(gameEnded) return;
                const tabEl = document.getElementById("tab"+id);
                const clickedNumber = parseInt(tabEl.getAttribute("data-num"));
                if(clickedNumber !== expectedOrder.shift()){
                    endGame();
                } else if(expectedOrder.length===0){
                    setTimeout(startRound, 500);
                }
            });
        });

        startRound();
        </script>
        </body>
        </html>
        """
        components.html(html_game, height=600, scrolling=False)

    # Capture score from JS via query params and store in session_state
    st.subheader("Enter Your Score Manually")

    score_input = st.number_input(
        "How many rounds did you complete?",
        min_value=0,
        max_value=20,
        step=1
    )

    if st.button("Save Pattern Game Score"):
        st.session_state["game_scores"]["Pattern"] = int(score_input)
        st.success(f"Pattern Switching score saved: {score_input} rounds completed!")
