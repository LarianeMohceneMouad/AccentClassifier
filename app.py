from flask import Flask, request, render_template, redirect, url_for
import os
from main import download_video, extract_audio, transcribe_audio, classify_audio, forculate_summary, remove_temp_files

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        video_url = request.form["video_url"]
        download_video(video_url)
        extract_audio(input_path="temp_video.mp4", output_path="./audio.mp3", overwrite=True)
        transcription = transcribe_audio()
        score, origin = classify_audio("audio.mp3")
        final_answer = forculate_summary(transcription, origin, score)
        remove_temp_files()
        result = {
            "transcription": transcription,
            "accent": origin,
            "score": f'{round(score, 4)*100}%',
            "summary": final_answer
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)