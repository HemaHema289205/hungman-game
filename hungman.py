import streamlit as st
import random
import nltk
import os
from nltk.corpus import words

# Ensure NLTK data is available
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
nltk.download('words', quiet=True)

# Initialize session state
if "chosen_word" not in st.session_state:
    st.session_state.word_list = [w.lower() for w in words.words() if w.isalpha() and len(w) >= 5]
    st.session_state.chosen_word = random.choice(st.session_state.word_list)
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.max_wrong = 6
    st.session_state.game_over = False

def display_word():
    return " ".join([letter if letter in st.session_state.guessed_letters else "_" for letter in st.session_state.chosen_word])

def guess_letter(letter):
    if st.session_state.game_over or letter in st.session_state.guessed_letters:
        return
    st.session_state.guessed_letters.append(letter)
    if letter not in st.session_state.chosen_word:
        st.session_state.wrong_guesses += 1
    check_game_status()

def check_game_status():
    if "_" not in display_word():
        st.session_state.game_over = True
        st.success(f"🎉 Congratulations! Word: {st.session_state.chosen_word}")
    elif st.session_state.wrong_guesses >= st.session_state.max_wrong:
        st.session_state.game_over = True
        st.error(f"💀 Game Over! Word was: {st.session_state.chosen_word}")

def reset_game():
    st.session_state.chosen_word = random.choice(st.session_state.word_list)
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.game_over = False

# UI Layout
st.markdown("<h1 style='text-align: center;'>🕹️ Hangman Game</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center;'>{display_word()}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Wrong guesses left: {st.session_state.max_wrong - st.session_state.wrong_guesses}</p>", unsafe_allow_html=True)

# Letter buttons
alphabet = "abcdefghijklmnopqrstuvwxyz"
cols = st.columns(13)
for i, letter in enumerate(alphabet):
    with cols[i % 13]:
        st.button(letter.upper(), key=letter, on_click=guess_letter, args=(letter,), disabled=letter in st.session_state.guessed_letters or st.session_state.game_over)

# End buttons
if st.session_state.game_over:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Play Again"):
            reset_game()
    with col2:
        st.markdown("Thanks for playing!")
