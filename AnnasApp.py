import streamlit as st
import pandas as pd
from datetime import datetime
import string

st.set_page_config(page_title="Daily Word", layout="centered")

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 480px;
    }
    h2 { font-size: 1.8rem !important; letter-spacing: 0.25rem; }
    h3 { font-size: 1.1rem !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Word database
# -----------------------------

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

# -----------------------------
# Get today's word (first one only)
# -----------------------------

todays_date = datetime.today().strftime('%Y-%m-%d')
todays_rows = word_df[word_df["Date"] == todays_date]

if todays_rows.empty:
    st.error("No word set for today.")
    st.stop()

word = todays_rows["Word"].iloc[0].upper()
desc = todays_rows["Description"].iloc[0]

# -----------------------------
# Session state
# -----------------------------

key = "w1"

if f"clicked_{key}" not in st.session_state:
    st.session_state[f"clicked_{key}"] = set()
if f"wrong_{key}" not in st.session_state:
    st.session_state[f"wrong_{key}"] = 1
if f"game_over_{key}" not in st.session_state:
    st.session_state[f"game_over_{key}"] = False
if f"popup_done_{key}" not in st.session_state:
    st.session_state[f"popup_done_{key}"] = False

# -----------------------------
# Handle letter click via query param
# -----------------------------

params = st.query_params
if "letter" in params and not st.session_state[f"game_over_{key}"]:
    letter = params["letter"].upper()
    if letter in string.ascii_uppercase and letter not in st.session_state[f"clicked_{key}"]:
        st.session_state[f"clicked_{key}"].add(letter)
        if letter not in word:
            st.session_state[f"wrong_{key}"] += 1
    st.query_params.clear()
    st.rerun()

# =========================================================
# POPUPS
# =========================================================

@st.dialog("🎉 You Win!")
def win_popup(w):
    st.image("win.jpg", use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>The word was {w}</h2>", unsafe_allow_html=True)

@st.dialog("💀 Game Over")
def lose_popup(w):
    st.image("lose.jpg", use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>The word was {w}</h2>", unsafe_allow_html=True)

# =========================================================
# UI
# =========================================================

st.markdown("<h2 style='text-align:center;'>Daily Word Learner 💛</h2>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center;'>{desc}</h3>", unsafe_allow_html=True)

# Hangman image
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(f"step{st.session_state[f'wrong_{key}']}.PNG", width=140)

# Word display
display_word = [l if l in st.session_state[f"clicked_{key}"] else "_" for l in word]
st.markdown(
    f"<h2 style='text-align:center;'>{' '.join(display_word)}</h2>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Keyboard — HTML grid, works on all screen sizes
# -----------------------------

if not st.session_state[f"game_over_{key}"]:
    clicked = st.session_state[f"clicked_{key}"]

    buttons_html = ""
    for letter in string.ascii_uppercase:
        used = letter in clicked
        correct = letter in word and letter in clicked

        if used:
            if correct:
                style = "background:#4caf50;color:white;opacity:0.5;cursor:default;"
            else:
                style = "background:#e0e0e0;color:#aaa;opacity:0.5;cursor:default;"
            btn = f'<button style="{style}" disabled>{letter}</button>'
        else:
            btn = f'<a href="?letter={letter}" style="text-decoration:none;"><button>{letter}</button></a>'

        buttons_html += btn

    st.markdown(f"""
    <style>
    .keyboard {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        justify-content: center;
        margin: 0 auto;
        max-width: 400px;
    }}
    .keyboard button {{
        width: 44px;
        height: 44px;
        font-size: 1rem;
        font-weight: bold;
        border: 2px solid #555;
        border-radius: 8px;
        background: white;
        color: #333;
        cursor: pointer;
        touch-action: manipulation;
    }}
    .keyboard button:active {{
        background: #ddd;
    }}
    </style>
    <div class="keyboard">{buttons_html}</div>
    """, unsafe_allow_html=True)

# -----------------------------
# Win / Lose checks
# -----------------------------

if st.session_state[f"wrong_{key}"] >= 8 and not st.session_state[f"game_over_{key}"]:
    st.session_state[f"game_over_{key}"] = True
    if not st.session_state[f"popup_done_{key}"]:
        st.session_state[f"popup_done_{key}"] = True
        lose_popup(word)

if "_" not in display_word and not st.session_state[f"game_over_{key}"]:
    st.session_state[f"game_over_{key}"] = True
    if not st.session_state[f"popup_done_{key}"]:
        st.session_state[f"popup_done_{key}"] = True
        win_popup(word)