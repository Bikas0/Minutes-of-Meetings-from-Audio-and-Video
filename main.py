import os
import torch
import warnings
from speech_recording import SpeechRecord
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
warnings.filterwarnings("ignore")


# Create the folder to store the audio file
FOLDER = "AudioFile"
os.makedirs(FOLDER, exist_ok=True)

SpeechRecord(FOLDER)

def get_speech_transcription(audio_path):
    
    runnning_device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        "model", torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(runnning_device)

    processor = AutoProcessor.from_pretrained("model")

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


# text = get_speech_transcription("/home/bikas/LLM-Minutes-of-Meeting/videoplayback.m4a")
text = get_speech_transcription(os.path.join(FOLDER, "output.wav"))
# text = get_speech_transcription("videoplayback (4).m4a")
os.remove(os.path.join(FOLDER, "output.wav"))
print(text)
