import streamlit as st
import speech_recognition as sr
import pyttsx3
from utils import generate_recipe

# Initialize the speech engine once
def init_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # You can change the voice index
    engine.setProperty("rate", 175)
    return engine

tts_engine = init_tts()

def speak_text(text):
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        st.error(f"Speech output error: {e}")

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak your ingredients clearly.")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        st.session_state.ingredients = text  # Store persistently
    except sr.UnknownValueError:
        st.error("❌ Could not understand your speech.")
    except sr.RequestError:
        st.error("⚠️ Could not connect to Speech Recognition service.")

# ---------------------- STREAMLIT UI ----------------------
st.set_page_config(page_title="AI Recipe Generator 🍳", layout="centered")

st.title("🍲 AI Recipe Generator (Voice + Text)")
st.write("Speak or type your ingredients, and get a delicious recipe — with voice output!")

# Initialize session state
if "ingredients" not in st.session_state:
    st.session_state.ingredients = ""

# Input mode
input_mode = st.radio("Choose Input Method:", ("✍️ Text", "🎙️ Voice"))

if input_mode == "✍️ Text":
    st.session_state.ingredients = st.text_area(
        "Enter ingredients (comma-separated):",
        value=st.session_state.ingredients,
        placeholder="e.g., chicken, rice, onion, tomato",
    )
elif input_mode == "🎙️ Voice":
    if st.button("🎧 Start Listening"):
        get_voice_input()

if st.session_state.ingredients:
    st.write(f"✅ Ingredients: {st.session_state.ingredients}")

# Generate Recipe
if st.button("🍳 Generate Recipe"):
    if st.session_state.ingredients:
        with st.spinner("Cooking up your AI recipe... 🍽️"):
            recipe = generate_recipe(st.session_state.ingredients)
        st.subheader("👩‍🍳 Your AI-Generated Recipe:")
        st.write(recipe)

        if st.checkbox("🔊 Speak Recipe"):
            speak_text(recipe)
    else:
        st.warning("Please provide ingredients first.")
