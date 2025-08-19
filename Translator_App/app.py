import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

# Translator
translator = Translator()

# Language codes supported by both googletrans and gTTS
# Note: Not all languages supported by googletrans are supported by gTTS.
# This list includes a subset that should work with both for common use cases.
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl"
}

# Streamlit UI
st.set_page_config(page_title="AI Translator App", page_icon="🗣️", layout="centered")
st.title("AI Translator App")
st.markdown("**Created by: Samikshya Sanskruti Swain**")

# Input text
text = st.text_area("Enter text to translate:", height=150)

# Language selection
col1, col2 = st.columns(2)
with col1:
    src_lang_name = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
    src_lang_code = LANGUAGES[src_lang_name]
with col2:
    dest_lang_name = st.selectbox("Destination Language", list(LANGUAGES.keys()), index=1)
    dest_lang_code = LANGUAGES[dest_lang_name]

# Translate
if st.button("Translate"):
    if text.strip() != "":
        try:
            translated = translator.translate(text, src=src_lang_code, dest=dest_lang_code)

            if translated and translated.text:
                st.subheader("Translated Text:")
                st.success(translated.text)

                # Text-to-Speech Option
                try:
                    tts = gTTS(text=translated.text, lang=dest_lang_code)
                    tts_file = "output.mp3"
                    tts.save(tts_file)

                    st.subheader("Listen:")
                    audio_file = open(tts_file, "rb")
                    st.audio(audio_file.read(), format="audio/mp3")

                    # Clean up the temporary audio file
                    os.remove(tts_file)

                except Exception as e:
                    st.warning(f"Could not generate speech for the translated text. Error: {e}")

            else:
                 st.warning("Translation failed. Please check your input and language selections.")

        except Exception as e:
            st.error(f"An error occurred during translation: {e}")

    else:
        st.warning("Please enter some text to translate.")
