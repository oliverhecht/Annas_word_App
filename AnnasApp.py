import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Daily Word", layout="centered")

word_df = pd.DataFrame({
    "Word": [
        "Ubiquitous", "Ephemeral",
        "Obfuscate", "Recalcitrant",
        "Perspicacious", "Laconic",
        "Ineffable", "Sycophant",
        "Ameliorate", "Bellicose",
        "Cacophony", "Capitulate",
        "Fastidious", "Grandiloquent",
        "Intransigent", "Magnanimous",
        "Pernicious", "Quixotic",
        "Reticent", "Sagacious",
        "Vociferous", "Zenith",
        "Acrimonious", "Benevolent",
        "Circumspect", "Diaphanous",
        "Enervate", "Fortuitous",
        "Garrulous", "Hegemony"
    ],
    "Description": [
        "Present, appearing, or found everywhere",
        "Lasting for a very short time",
        "To deliberately make something unclear or confusing",
        "Stubbornly refusing to obey authority or compromise",
        "Having keen insight and understanding",
        "Using very few words; brief and to the point",
        "Too great or extreme to be expressed in words",
        "A person who flatters others for personal gain",
        "To make something better or improve it",
        "Aggressively hostile or combative",
        "A harsh, discordant mixture of sounds",
        "To give in or surrender",
        "Very attentive to detail; perfectionist",
        "Using elaborate or pompous language",
        "Unwilling to change one's views or agree",
        "Generous or forgiving, especially toward a rival",
        "Harmful in a subtle or gradual way",
        "Extremely idealistic and unrealistic",
        "Reserved or not revealing feelings",
        "Having or showing great wisdom",
        "Expressing something loudly and forcefully",
        "The highest point or peak",
        "Angry and bitter in tone or manner",
        "Kind and generous",
        "Careful and cautious before making decisions",
        "Light, delicate, and translucent",
        "To weaken or drain of energy",
        "Happening by chance, often in a positive way",
        "Excessively talkative",
        "Leadership or dominance over others"
    ],
    "Date": pd.date_range(start="2026-05-14", periods=15).repeat(2).strftime("%Y-%m-%d")
})

todays_date = datetime.today().strftime('%Y-%m-%d')
todays_rows = word_df[word_df["Date"] == todays_date]

if todays_rows.empty:
    st.error("No word set for today.")
    st.stop()

target_word = todays_rows["Word"].iloc[0].upper()
desc = todays_rows["Description"].iloc[0]

# Base64-encode all 8 step images
def img_to_b64(path):
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/{ext};base64,{data}"

images_b64 = []
for i in range(1, 9):
    images_b64.append(img_to_b64(f"step{i}.PNG"))

# Build JS array of base64 image strings
images_js = "[" + ",".join(f'"{src}"' for src in images_b64) + "]"

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: sans-serif; background: white; padding: 12px; max-width: 480px; margin: 0 auto; }}
  h1 {{ text-align: center; font-size: 1.4rem; margin-bottom: 6px; }}
  #desc {{ text-align: center; font-size: 0.95rem; color: #555; margin-bottom: 14px; }}
  #hangman-container {{ text-align: center; margin-bottom: 12px; }}
  #hangman-container img {{ width: 120px; height: auto; }}
  #word {{ text-align: center; font-size: 1.8rem; letter-spacing: 0.4rem; margin-bottom: 6px; font-weight: bold; }}
  #mistakes {{ text-align: center; font-size: 0.85rem; color: #888; margin-bottom: 14px; }}
  .kb-row {{ display: flex; justify-content: center; gap: 5px; margin-bottom: 6px; }}
  .kb-btn {{
    width: 34px; height: 44px;
    background: #818384; color: white;
    border: none; border-radius: 6px;
    font-weight: bold; font-size: 0.9rem;
    cursor: pointer; touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
  }}
  .kb-btn:disabled {{ cursor: default; }}
  .kb-btn.correct {{ background: #4caf50; }}
  .kb-btn.wrong {{ background: #ccc; color: #999; }}
  #message {{ text-align: center; font-size: 1.2rem; font-weight: bold; margin-top: 16px; }}
</style>
</head>
<body>
<h1>Daily Word Learner 💛</h1>
<div id="desc">{desc}</div>
<div id="hangman-container"><img id="hangman-img" src="" /></div>
<div id="word"></div>
<div id="mistakes"></div>
<div id="keyboard"></div>
<div id="message"></div>

<script>
const TARGET = "{target_word}";
const ROWS = ["QWERTYUIOP","ASDFGHJKL","ZXCVBNM"];
const IMAGES = {images_js};

let clicked = new Set();
let wrong = 0;
let gameOver = false;

function render() {{
  document.getElementById("hangman-img").src = IMAGES[Math.min(wrong, IMAGES.length-1)];

  const display = TARGET.split("").map(l => clicked.has(l) ? l : "_").join(" ");
  document.getElementById("word").textContent = display;
  document.getElementById("mistakes").textContent = `Wrong guesses: ${{wrong}} / 7`;

  const kb = document.getElementById("keyboard");
  kb.innerHTML = "";
  ROWS.forEach(row => {{
    const div = document.createElement("div");
    div.className = "kb-row";
    for (const l of row) {{
      const btn = document.createElement("button");
      btn.className = "kb-btn";
      btn.textContent = l;
      if (clicked.has(l)) {{
        btn.disabled = true;
        btn.classList.add(TARGET.includes(l) ? "correct" : "wrong");
      }} else {{
        btn.addEventListener("click", () => guess(l));
      }}
      div.appendChild(btn);
    }}
    kb.appendChild(div);
  }});

  if (!gameOver) {{
    if (!display.includes("_")) {{
      gameOver = true;
      document.getElementById("message").textContent = "🎉 You got it!";
      kb.innerHTML = "";
    }} else if (wrong >= 7) {{
      gameOver = true;
      document.getElementById("message").textContent = `💀 Game over! The word was ${{TARGET}}`;
      kb.innerHTML = "";
    }}
  }}
}}

function guess(l) {{
  if (gameOver || clicked.has(l)) return;
  clicked.add(l);
  if (!TARGET.includes(l)) wrong++;
  render();
}}

render();
</script>
</body>
</html>
"""

st.components.v1.html(game_html, height=560, scrolling=False)