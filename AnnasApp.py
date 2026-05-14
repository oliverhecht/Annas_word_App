import streamlit as st
import pandas as pd
from datetime import datetime
import string

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
# Get today's words
# -----------------------------

todays_date = datetime.today().strftime('%Y-%m-%d')
todays_rows = word_df[word_df["Date"] == todays_date]

if todays_rows.empty:
    st.error("No word set for today.")
    st.stop()

word_list = todays_rows["Word"].tolist()
desc_list = todays_rows["Description"].tolist()

# -----------------------------
# Title
# -----------------------------

st.markdown(
    "<h2 style='text-align: center;'>Welcome to your daily word learner &lt;3</h2>",
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Word 1", "Word 2"])

# =========================================================
# POPUPS
# =========================================================

@st.dialog("🎉 You Win!")
def win_popup(word):
    st.image("win.jpg", use_container_width=True)
    st.markdown(
        f"<h2 style='text-align:center;'>The word was {word}</h2>",
        unsafe_allow_html=True
    )

@st.dialog("💀 Game Over")
def lose_popup(word):
    st.image("lose.jpg", use_container_width=True)
    st.markdown(
        f"<h2 style='text-align:center;'>The word was {word}</h2>",
        unsafe_allow_html=True
    )

# =========================================================
# WORD GAME FUNCTION (clean logic reused)
# =========================================================

def run_game(key, word, desc):

    word = word.upper()

    # ---------------- state ----------------
    if f"clicked_{key}" not in st.session_state:
        st.session_state[f"clicked_{key}"] = set()

    if f"wrong_{key}" not in st.session_state:
        st.session_state[f"wrong_{key}"] = 1

    if f"game_over_{key}" not in st.session_state:
        st.session_state[f"game_over_{key}"] = False

    if f"popup_done_{key}" not in st.session_state:
        st.session_state[f"popup_done_{key}"] = False

    # ---------------- UI ----------------
    st.markdown(
        f"<h3 style='text-align:center;'>{desc}</h3>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(f"step{st.session_state[f'wrong_{key}']}.PNG", width=300)

    display_word = [
        l if l in st.session_state[f"clicked_{key}"] else "_"
        for l in word
    ]

    st.markdown(
        f"<h2 style='text-align:center;'>{' '.join(display_word)}</h2>",
        unsafe_allow_html=True
    )

    # ---------------- buttons ----------------
    if not st.session_state[f"game_over_{key}"]:
        cols = st.columns(8)

        for i, letter in enumerate(string.ascii_uppercase):
            with cols[i % 8]:

                used = letter in st.session_state[f"clicked_{key}"]

                if st.button(
                    letter,
                    key=f"{key}_{letter}",
                    disabled=used
                ):

                    st.session_state[f"clicked_{key}"].add(letter)

                    if letter not in word:
                        st.session_state[f"wrong_{key}"] += 1

    # ---------------- lose ----------------
    if (
        st.session_state[f"wrong_{key}"] >= 8
        and not st.session_state[f"game_over_{key}"]
    ):
        st.session_state[f"game_over_{key}"] = True

        if not st.session_state[f"popup_done_{key}"]:
            st.session_state[f"popup_done_{key}"] = True
            lose_popup(word)

    # ---------------- win ----------------
    if (
        "_" not in display_word
        and not st.session_state[f"game_over_{key}"]
    ):
        st.session_state[f"game_over_{key}"] = True

        if not st.session_state[f"popup_done_{key}"]:
            st.session_state[f"popup_done_{key}"] = True
            win_popup(word)

# =========================================================
# RUN TABS
# =========================================================

with tab1:
    run_game("w1", word_list[0], desc_list[0])

with tab2:
    run_game("w2", word_list[1], desc_list[1])