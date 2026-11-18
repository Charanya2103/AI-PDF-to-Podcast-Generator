import os
import streamlit as st
from dotenv import load_dotenv

from src.pdf_utils import extract_text_from_pdf
from src.podcast_generator import generate_podcast_script
from src.audio_generator import generate_audio

load_dotenv()

st.set_page_config(page_title="AI PDF to Podcast", page_icon="🎙️", layout="wide")
st.title("🎙️ AI-Driven PDF to Podcast Generator")
st.caption("Turn long PDF documents into conversational, multi-speaker podcast episodes.")

with st.sidebar:
    st.header("Configuration")
    st.write("Add API keys to a `.env` file or enter them below.")
    gemini_key = st.text_input("Gemini API key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    eleven_key = st.text_input("ElevenLabs API key (optional)", value=os.getenv("ELEVENLABS_API_KEY", ""), type="password")
    model = st.text_input("Gemini model", value=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    st.divider()
    use_hf = st.checkbox("Use Hugging Face summarization (optional)", value=False)
    hf_model = st.text_input("Hugging Face model", value="sshleifer/distilbart-cnn-12-6", disabled=not use_hf)

uploaded = st.file_uploader("Upload a PDF document", type=["pdf"])
col1, col2 = st.columns(2)
with col1:
    host_a = st.text_input("Host 1 name", "Alex")
with col2:
    host_b = st.text_input("Host 2 name", "Sam")

if uploaded:
    if st.button("Extract PDF text"):
        with st.spinner("Reading your PDF..."):
            try:
                text = extract_text_from_pdf(uploaded.getvalue())
                st.session_state["pdf_text"] = text
                st.success(f"Extracted {len(text):,} characters.")
            except Exception as exc:
                st.error(str(exc))

if "pdf_text" in st.session_state:
    with st.expander("Preview extracted text"):
        st.text_area("PDF content", st.session_state["pdf_text"][:12000], height=220)

    if st.button("Generate podcast script", type="primary"):
        if not gemini_key:
            st.error("Enter your Gemini API key in the sidebar.")
        else:
            with st.spinner("Generating a conversational podcast script..."):
                try:
                    summary = None
                    if use_hf:
                        from src.hf_summarizer import summarize_text
                        summary = summarize_text(st.session_state["pdf_text"], hf_model)
                    script = generate_podcast_script(
                        st.session_state["pdf_text"], gemini_key, model, host_a, host_b, summary
                    )
                    st.session_state["podcast_script"] = script
                    st.success("Podcast script generated.")
                except Exception as exc:
                    st.error(f"Script generation failed: {exc}")

if "podcast_script" in st.session_state:
    st.subheader("Generated podcast script")
    st.text_area("Edit or review the script", st.session_state["podcast_script"], height=360, key="script_editor")
    st.download_button(
        "Download script (.txt)",
        st.session_state["script_editor"],
        file_name="podcast_script.txt",
        mime="text/plain",
    )

    if st.button("Generate podcast audio"):
        if not eleven_key:
            st.error("Enter your ElevenLabs API key in the sidebar.")
        else:
            with st.spinner("Converting dialogue into audio..."):
                try:
                    audio_bytes = generate_audio(st.session_state["script_editor"], eleven_key)
                    st.session_state["audio_bytes"] = audio_bytes
                    st.success("Audio generated.")
                except Exception as exc:
                    st.error(f"Audio generation failed: {exc}")

if "audio_bytes" in st.session_state:
    st.subheader("Podcast audio")
    st.audio(st.session_state["audio_bytes"], format="audio/mpeg")
    st.download_button(
        "Download podcast (.mp3)",
        st.session_state["audio_bytes"],
        file_name="generated_podcast.mp3",
        mime="audio/mpeg",
    )

st.markdown("---")
st.caption("Note: Review AI-generated content for accuracy before relying on it. API usage may incur charges.")
