import subprocess
import os
import sys
# from fastapi import FastAPI, File, UploadFile 
import aiofiles
import torch
import warnings
from speech_recording import SpeechRecord
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
warnings.filterwarnings("ignore")

# Create the folder to store the audio file
FOLDER = "AudioFile"
os.makedirs(FOLDER, exist_ok=True)

# SpeechRecord(FOLDER)

def audio_to_transcript(audio_path):
    # whisper_model = "Large_model"
    # whisper_model = "Base_model"
    whisper_model = "Turbo_model"
    runnning_device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(runnning_device)

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
        device=runnning_device,
    )
    
    print(f"Wait few a Minute...")
    result = speech_pipeline(audio_path, return_timestamps=False)
    print(f"Complete the Task...")
    # print(f"{result}")
    del speech_pipeline, model, processor
    torch.cuda.empty_cache()
    
    return result['text']


def video_to_audio(video_file):
    audio_file = os.path.join(FOLDER, "input_audio.mp3")
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return audio_file

# audio_file = video_to_audio('interview.mp4')
audio_file = os.path.join(FOLDER, "input_audio.mp3")
transcript = audio_to_transcript(audio_file)
# os.remove(os.path.join(FOLDER, "input_audio.mp3"))
print(transcript)

