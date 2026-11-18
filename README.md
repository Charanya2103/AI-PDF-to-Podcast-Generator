# AI-Driven PDF to Podcast Generator

A Streamlit application that transforms text-based PDF documents into conversational, two-host podcast scripts and MP3 audio.

## Features

- Extracts text from PDF files with page markers using `pypdf`.
- Generates a conversational, multi-speaker script using the Gemini API.
- Optionally summarizes long documents locally using Hugging Face Transformers.
- Converts the generated dialogue into MP3 audio using ElevenLabs Text-to-Speech.
- Lets users review/edit and download the script and audio.

## Technology stack

- **Language:** Python
- **UI:** Streamlit
- **PDF processing:** pypdf
- **Generative AI:** Google Gemini API
- **NLP / Transformers:** Hugging Face Transformers (optional local summarization)
- **Text-to-Speech:** ElevenLabs API

## Project structure

```text
ai-pdf-to-podcast-generator/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── src/
    ├── __init__.py
    ├── pdf_utils.py
    ├── podcast_generator.py
    ├── audio_generator.py
    └── hf_summarizer.py
```

## Prerequisites

- Python 3.10 or newer
- A Gemini API key
- An ElevenLabs API key for audio generation
- Internet connection for API calls

The Hugging Face summarization option downloads its model the first time it is used and runs locally. It is optional and can require substantial RAM/disk space.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-pdf-to-podcast-generator.git
   cd ai-pdf-to-podcast-generator
   ```

2. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create a `.env` file by copying `.env.example`, then add your API keys:

   ```env
   GEMINI_API_KEY=your_real_gemini_api_key
   GEMINI_MODEL=gemini-2.5-flash
   ELEVENLABS_API_KEY=your_real_elevenlabs_api_key
   ```

   Never commit `.env` or publish API keys.

5. Run the app:

   ```bash
   streamlit run app.py
   ```

## How to use

1. Open the local Streamlit URL shown in the terminal.
2. Enter your Gemini API key in the sidebar.
3. Upload a text-based PDF.
4. Extract the document text.
5. Generate the podcast script.
6. Review or edit the script and download it.
7. Add your ElevenLabs API key and generate/download the MP3.

## Important notes

- Scanned/image-only PDFs are not OCR-processed. Apply OCR before uploading those files.
- The app sends extracted document text to the Gemini API. Do not upload confidential, personal, or copyrighted material unless you have permission and understand the provider's data policies.
- API providers may charge for usage. Check their current pricing and quotas.
- The audio feature currently uses one voice for the complete dialogue. Speaker labels are removed before text-to-speech; true multi-voice diarized output would require mapping each host to a separate voice.
- Hugging Face summarization is optional. The default workflow uses Gemini for script generation.
- Always verify AI-generated summaries and scripts against the original PDF.

## Future improvements

- Separate voice assignment for each podcast host.
- OCR support for scanned PDFs.
- Podcast length and language controls.
- Background music and audio mixing.
- User accounts and podcast history.
- Deployment with Streamlit Community Cloud.

## Responsible use

Use documents you are authorized to process. Review generated content for factual accuracy and avoid treating the output as a substitute for the original source.
