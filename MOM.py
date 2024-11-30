import os
import subprocess
import torch
import warnings
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore")

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Directory to store audio files
AUDIO_FOLDER = "AudioFile"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Function to generate Minutes of Meeting (MoM)
def generate_mom(text):
    prompt = f"""
    Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text. 
    For each relevant topic, create a single title and list the key points discussed under that title. 
    When the topic changes, create a new title and include the discussion points related to the new topic under it. 
    If there are irrelevant topics mentioned, list them separately under an "Irrelevant Topics" title. 
    Each title should be followed by a bullet-point list of the main discussion points related to that specific topic.
    Text: {text}
    """
    model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 0})
    response = model.generate_content([prompt])
    return response.text


# Convert video to audio
def extract_audio_from_video(video_path):
    audio_path = os.path.join(AUDIO_FOLDER, "input_audio.mp3")
    subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path], 
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return audio_path

# Convert audio to transcript
def audio_to_transcript(audio_path):
    whisper_model = "Base_model"  # Replace with actual model name
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(whisper_model)

    speech_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=256,
        chunk_length_s=20,
        batch_size=8,
        torch_dtype=torch_dtype,
        device=device,
    )

    print("Processing audio... Please wait.")
    result = speech_pipeline(audio_path, return_timestamps=False)
    print("Transcription completed.")

    # Clean up resources
    del speech_pipeline, model, processor
    torch.cuda.empty_cache()

    return result['text']


file = 'AudioFile/input_audio.mp3'  # Replace with your video file path
extension = file.split(".")[-1]
if extension == "mp4":
    file = extract_audio_from_video(file)
transcript = audio_to_transcript(file)
mom_result = generate_mom(transcript)
# os.remove(os.path.join(AUDIO_FOLDER, "input_audio.mp3"))
print(mom_result)
