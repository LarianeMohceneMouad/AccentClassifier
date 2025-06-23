# Accent Classifier & Summarizer

This project is a web application that allows users to input a YouTube video URL, automatically download the video, extract its audio, transcribe the speech, classify the speaker's accent, and generate a summary of the content using Azure OpenAI services.

## Features

- **YouTube Video Download:** Downloads the video from a provided URL.
- **Audio Extraction:** Extracts audio from the downloaded video.
- **Speech Transcription:** Transcribes the audio using Azure OpenAI Whisper.
- **Accent Classification:** Identifies the accent of the speaker using a pre-trained SpeechBrain model.
- **Content Summarization:** Summarizes the transcribed content and provides an explanation, including the detected accent and confidence score.
- **Web Interface:** Simple Flask-based web UI for user interaction.

## Project Structure

- `app.py`: Flask web application entry point.
- `main.py`: Core logic for downloading, extracting, transcribing, classifying, and summarizing.
- `audio_extract.py`: (Required) Contains the `extract_audio` function.
- `templates/index.html`: HTML template for the web interface.
- `config.json` & `.env`: Configuration and API keys.
- `requierements.txt`: Python dependencies.
- `Dockerfile`: For containerized deployment.

## How It Works

1. **User Input:**  
   The user enters a YouTube video URL in the web interface.

2. **Video Download:**  
   The backend downloads the video using `yt_dlp`.

3. **Audio Extraction:**  
   The audio is extracted from the video and saved as `audio.mp3`.

4. **Transcription:**  
   The audio file is transcribed to text using Azure OpenAI Whisper.

5. **Accent Classification:**  
   The transcribed audio is analyzed by a SpeechBrain model to determine the accent and confidence score.

6. **Summarization:**  
   The transcription, accent, and confidence score are sent to Azure OpenAI for summarization and explanation.

7. **Results Display:**  
   The transcription, accent, confidence score, and summary are displayed on the web page.

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd AccentClassifier
```

### 2. Install Dependencies

Make sure you have Python 3.12 installed.

```sh
pip install -r requierements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root with your Azure OpenAI API key and endpoints:

```
OPENAI_API_KEY=your_openai_api_key
WHISPER_API_VERSION=2024-02-01
WHISPER_API_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/openai/deployments/whisper/audio/translations?api-version=2024-06-01
OPENAI_API_ENDPOINT=https://<your-resource>.openai.azure.com/
```

### 4. Run the Application

```sh
python app.py
```

The app will be available at [http://localhost:5000](http://localhost:5000).

### 5. Docker (Optional)

To run the app in a Docker container:

```sh
docker build -t accent-classifier .
docker run -p 5000:5000 accent-classifier
```

## Notes

- Ensure you have valid Azure OpenAI credentials and the correct deployment names.
- The `audio_extract.py` file must be present and implement the `extract_audio` function.
- The SpeechBrain model requires internet access to download the pre-trained weights on first run.

## File Overview

- [`app.py`](app.py): Flask app and route handling.
- [`main.py`](main.py): Core processing functions.
- [`templates/index.html`](templates/index.html): Web UI template.
- [`requierements.txt`](requierements.txt): Python dependencies.
- [`Dockerfile`](Dockerfile): Containerization instructions.
- [`config.json`](config.json): Additional configuration.
- [`.env`](.env): API keys and endpoints.

## License

This project is for educational purposes.

---

**Author:**  
Mohcene Mouad Lariane
