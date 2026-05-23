import streamlit as st
import pandas as pd
from datetime import datetime
import string

st.set_page_config(page_title="Daily Word", layout="centered")

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 480px;
    }

    /* Make all letter buttons small and square */
    div.stButton > button {
        padding: 0 !important;
        width: 36px !important;
        height: 36px !important;
        min-height: 36px !important;
        font-size: 0.85rem !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        margin: 1px auto !important;
        display: block !important;
    }

    /* Remove extra column padding so buttons pack tightly */
    div[data-testid="column"] {
        padding: 0 2px !important;
    }
</style>
""", unsafe_allow_html=True)

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

word = todays_rows["Word"].iloc[0].upper()
desc = todays_rows["Description"].iloc[0]

key = "w1"

if f"clicked_{key}" not in st.session_state:
    st.session_state[f"clicked_{key}"] = set()
if f"wrong_{key}" not in st.session_state:
    st.session_state[f"wrong_{key}"] = 1
if f"game_over_{key}" not in st.session_state:
    st.session_state[f"game_over_{key}"] = False
if f"popup_done_{key}" not in st.session_state:
    st.session_state[f"popup_done_{key}"] = False

@st.dialog("🎉 You Win!")
def win_popup(w):
    st.image("win.jpg", use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>The word was {w}</h2>", unsafe_allow_html=True)

@st.dialog("💀 Game Over")
def lose_popup(w):
    st.image("lose.jpg", use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>The word was {w}</h2>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>Daily Word Learner 💛</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:1.1rem;'>{desc}</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(f"step{st.session_state[f'wrong_{key}']}.PNG", width=120)

display_word = [l if l in st.session_state[f"clicked_{key}"] else "_" for l in word]
st.markdown(
    f"<h2 style='text-align:center; letter-spacing:0.3rem;'>{' '.join(display_word)}</h2>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state[f"game_over_{key}"]:
    letters = list(string.ascii_uppercase)
    rows = [letters[:13], letters[13:]]

    for row in rows:
        cols = st.columns(len(row))
        for i, letter in enumerate(row):
            with cols[i]:
                used = letter in st.session_state[f"clicked_{key}"]
                if st.button(letter, key=f"{key}_{letter}", disabled=used):
                    st.session_state[f"clicked_{key}"].add(letter)
                    if letter not in word:
                        st.session_state[f"wrong_{key}"] += 1
                    st.rerun()

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