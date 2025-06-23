import yt_dlp
from audio_extract import extract_audio
import os
from openai import AzureOpenAI
from speechbrain.pretrained.interfaces import foreign_class
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  
api_key = os.getenv("OPENAI_API_KEY")



# Function to download video from url input
def download_video(url, save_path="."):
    ydl_opts = {
        'outtmpl': f'temp_video.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'nooverwrites': True,
        'overwrite': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")
    

# Function to extract audio from the downloaded video audio file
def transcribe_audio():     
    """transcribe audio from the downloaded video audio file."""
    client = AzureOpenAI(
        api_key=api_key,  
        api_version="2024-02-01",
        azure_endpoint = "https://mohcenemouadlariane-174-resource.cognitiveservices.azure.com/openai/deployments/whisper/audio/translations?api-version=2024-06-01"
    )
        
    deployment_id = "whisper" 
    audio_test_file = "./audio.mp3"
        
    result = client.audio.transcriptions.create(
        file=open(audio_test_file, "rb"),            
        model=deployment_id
    )
    return result.text
    

def classify_audio(audio_file):
    """Classify the accent of the audio file using a pre-trained model."""
    classifier = foreign_class(source="Jzuluaga/accent-id-commonaccent_xlsr-en-english", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
    _, score, _, text_lab = classifier.classify_file(audio_file)
    return score[0].item(), text_lab[0]


def remove_temp_files():
    """Remove temporary files created during the process."""
    temp_file_paths = ["audio.mp3", "temp_video.mp4"]
    for file_path in temp_file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")


def forculate_summary(audio_transcription, accent, score):
    """ Generate a summary and explanation of the audio transcription using Azure OpenAI. """
    # Set up Azure OpenAI client    
    endpoint = os.getenv("ENDPOINT_URL", "https://mohcenemouadlariane-174-resource.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "o4-mini")
    subscription_key = api_key

    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2025-01-01-preview",
    )

    #Prepare the chat prompt
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant that helps summarize the and explain the provided content and also mention the accent of the language spoken alsong with the confidence score. The content is in the form of a text file. You will be provided with a text file that contains the content to summarize and explain."
                }
            ],
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Here is the content of the text file: {audio_transcription} and the origin {accent} and the confidence score is {int(score)*100}%. Please summarize the content in a concise manner."
                }
            ]

        }
    ]
    messages = chat_prompt

    # Generate the completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_completion_tokens=100000,
        stop=None,
        stream=False
    )

    # Access the content directly from the response object
    return completion.choices[0].message.content


if __name__ == "__main__":
    # Download the video from the provided URL
    video_url = input("Enter the video URL: ")
    download_video(video_url)
    # Extract audio from the downloaded video
    extract_audio(input_path="temp_video.mp4", output_path="./audio.mp3", overwrite=True)
    # Transcribe the audio using Azure
    print("Transcribing audio...")
    transcription = transcribe_audio()
    print("Transcription complete!")
    print("Processing...")
    score, origin = classify_audio("audio.mp3")
    final_answer = forculate_summary(transcription, origin, score)
    print(final_answer)
    # Clean up temporary files
    remove_temp_files()





