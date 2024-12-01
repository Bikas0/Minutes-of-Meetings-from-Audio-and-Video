# # import os
# # import subprocess
# # import torch
# # import magic
# # import warnings
# # from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# # from dotenv import load_dotenv
# # import google.generativeai as genai

# # # Load environment variables
# # load_dotenv()
# # warnings.filterwarnings("ignore")

# # # Configure GenAI Key
# # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # # Directory to store audio files
# # AUDIO_FOLDER = "AudioFile"
# # os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # # Function to generate Minutes of Meeting (MoM)
# # def generate_mom(transcription_result):
# #     segments = transcription_result['segments']
# #     formatted_text = "\n".join(
# #         [f"{seg['start']:0.2f}s - {seg['end']:0.2f}s: {seg['text']}" for seg in segments]
# #     )
# #     prompt = f"""
# #     Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text, including timestamps.
# #     For each relevant topic, create a single title and list the key points discussed under that title. 
# #     Include timestamps for when the discussion occurred. 
# #     If there are irrelevant topics mentioned, list them separately under an "Irrelevant Topics" title. 
# #     Each title should be followed by a bullet-point list of the main discussion points with corresponding timestamps.
# #     Text: {formatted_text}
# #     """
# #     model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 0})
# #     response = model.generate_content([prompt])
# #     return response.text


# # # Convert video to audio
# # def extract_audio_from_video(video_path):
# #     audio_path = os.path.join(AUDIO_FOLDER, "input_audio.mp3")
# #     subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path], 
# #                     stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
# #     return audio_path

# # # Convert audio to transcript
# # def audio_to_transcript(audio_path):
# #     whisper_model = "openai/whisper-base"
# #     device = "cuda:0" if torch.cuda.is_available() else "cpu"
# #     torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# #     model = AutoModelForSpeechSeq2Seq.from_pretrained(
# #         whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True
# #     ).to(device)

# #     processor = AutoProcessor.from_pretrained(whisper_model)

# #     speech_pipeline = pipeline(
# #         "automatic-speech-recognition",
# #         model=model,
# #         tokenizer=processor.tokenizer,
# #         feature_extractor=processor.feature_extractor,
# #         return_timestamps=True,
# #         chunk_length_s=30,
# #         batch_size=8,
# #         torch_dtype=torch_dtype,
# #         device=device,
# #     )

# #     print("Processing audio... Please wait.")
# #     try:
# #         result = speech_pipeline(audio_path)
# #     except Exception as e:
# #         raise RuntimeError(f"Error during transcription: {e}")
# #     print("Transcription completed.\n")

# #     # Inspect the result structure
# #     print("Raw Transcription Result:", result)

# #     # Process result based on format
# #     if "chunks" in result:
# #         transcript_data = {
# #             "segments": [
# #                 {
# #                     "start": chunk["timestamp"][0],
# #                     "end": chunk["timestamp"][1],
# #                     "text": chunk.get("text", ""),
# #                 }
# #                 for chunk in result["chunks"]
# #             ]
# #         }
# #     elif isinstance(result, dict) and "text" in result:
# #         # Fallback case: Treat the entire result as one segment
# #         transcript_data = {
# #             "segments": [{"start": 0, "end": 0, "text": result["text"]}]
# #         }
# #     else:
# #         raise ValueError("The transcription output format is invalid or unsupported.")

# #     # Clean up resources
# #     del speech_pipeline, model, processor
# #     torch.cuda.empty_cache()

# #     return transcript_data



# # def get_file_type(file_path):
# #     # Create a magic object to identify file type
# #     file_magic = magic.Magic(mime=True)
# #     file_type = file_magic.from_file(file_path)
    
# #     # Check if the file type indicates audio or video
# #     if 'audio' in file_type:
# #         return "Audio"
# #     elif 'video' in file_type:
# #         return "Video"
# #     else:
# #         return "Unknown file type"

# # # Main script
# # file = 'interview.mp4'  # Replace with your audio or video file path
# # file_type = get_file_type(file)
# # if file_type == "Video":
# #     file = extract_audio_from_video(file)
# # transcription_result = audio_to_transcript(file)

# # # Print raw transcription with timestamps
# # segments = transcription_result['segments']
# # for segment in segments:
# #     print(f"{segment['start']:0.2f}s - {segment['end']:0.2f}s: {segment['text']}")

# # mom_result = generate_mom(transcription_result)

# # # Print the generated meeting minutes
# # print("\n\nMinutes of Meeting (MoM):\n")
# # print(mom_result)



# import os
# import subprocess
# import torch
# import magic
# import warnings
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()
# warnings.filterwarnings("ignore")

# # Configure GenAI Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Directory to store audio files
# AUDIO_FOLDER = "AudioFile"
# os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # Function to convert seconds to hours, minutes, and seconds
# def format_time(seconds):
#     """
#     Format time from seconds to HH:MM:SS.
#     If seconds is None, default to 0.
#     """
#     if seconds is None:
#         seconds = 0
#     hours = seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = seconds % 60
#     return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# # Function to generate Minutes of Meeting (MoM) with formatted time
# def generate_mom(transcription_result):
#     segments = transcription_result['segments']
#     formatted_text = "\n".join(
#         [f"{format_time(seg['start'])} - {format_time(seg['end'])}: {seg['text']}" for seg in segments]
#     )
#     prompt = f"""
#     Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text, including timestamps.
#     For each relevant topic, create a single title and list the key points discussed under that title. 
#     Include timestamps for when the discussion occurred. 
#     If there are irrelevant topics mentioned, list them separately under an "Irrelevant Topics" title. 
#     Each title should be followed by a bullet-point list of the main discussion points with corresponding timestamps.
#     Text: {formatted_text}
#     """
#     model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 0})
#     response = model.generate_content([prompt])
#     return response.text

# # Convert video to audio
# def extract_audio_from_video(video_path):
#     audio_path = os.path.join(AUDIO_FOLDER, "input_audio.mp3")
#     subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path], 
#                     stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#     return audio_path

# # Convert audio to transcript
# def audio_to_transcript(audio_path):
#     whisper_model = "openai/whisper-base"
#     device = "cuda:0" if torch.cuda.is_available() else "cpu"
#     torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

#     model = AutoModelForSpeechSeq2Seq.from_pretrained(
#         whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True
#     ).to(device)

#     processor = AutoProcessor.from_pretrained(whisper_model)

#     speech_pipeline = pipeline(
#         "automatic-speech-recognition",
#         model=model,
#         tokenizer=processor.tokenizer,
#         feature_extractor=processor.feature_extractor,
#         return_timestamps=True,
#         chunk_length_s=30,
#         batch_size=8,
#         torch_dtype=torch_dtype,
#         device=device,
#     )

#     print("Processing audio... Please wait.")
#     try:
#         result = speech_pipeline(audio_path)
#     except Exception as e:
#         raise RuntimeError(f"Error during transcription: {e}")
#     print("Transcription completed.\n")

#     # Inspect the result structure
#     # print("Raw Transcription Result:", result)

#     # Process result based on format
  
#     # Handle transcription result
#     if isinstance(result, dict) and "chunks" in result:
#         transcript_data = {
#             "segments": [
#                 {
#                     "start": chunk["timestamp"][0],
#                     "end": chunk["timestamp"][1],
#                     "text": chunk["text"],
#                 }
#                 for chunk in result["chunks"]
#             ]
#         }
#     elif isinstance(result, dict) and "text" in result:
#         transcript_data = {
#             "segments": [{"start": 0, "end": 0, "text": result["text"]}]
#         }
#     else:
#         raise ValueError("Invalid transcription output format.")

#     # Clean up resources
#     del speech_pipeline, model, processor
#     torch.cuda.empty_cache()

#     return transcript_data

# # Function to determine the file type (audio or video)
# def get_file_type(file_path):
#     # Create a magic object to identify file type
#     file_magic = magic.Magic(mime=True)
#     file_type = file_magic.from_file(file_path)
    
#     # Check if the file type indicates audio or video
#     if 'audio' in file_type:
#         return "Audio"
#     elif 'video' in file_type:
#         return "Video"
#     else:
#         return "Unknown file type"

# # Main script
# file = 'interview.mp4'  # Replace with your audio or video file path
# file_type = get_file_type(file)
# if file_type == "Video":
#     file = extract_audio_from_video(file)
# transcription_result = audio_to_transcript(file)

# # Print raw transcription with timestamps
# segments = transcription_result['segments']
# # for segment in segments:
# #     print(f"{format_time(segment['start'])} - {format_time(segment['end'])}: {segment['text']}")

# mom_result = generate_mom(transcription_result)

# # Print the generated meeting minutes
# print("\n\nMinutes of Meeting (MoM):\n")
# print(mom_result)


# import os
# import subprocess
# import torch
# import magic
# import warnings
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()
# warnings.filterwarnings("ignore")

# # Configure GenAI Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Directory to store audio files
# AUDIO_FOLDER = "AudioFile"
# os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # Function to generate Minutes of Meeting (MoM)
# def generate_mom(transcription_result):
#     segments = transcription_result['segments']
#     formatted_text = "\n".join(
#         [f"{seg['start']:0.2f}s - {seg['end']:0.2f}s: {seg['text']}" for seg in segments]
#     )
#     prompt = f"""
#     Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text, including timestamps.
#     For each relevant topic, create a single title and list the key points discussed under that title. 
#     Include timestamps for when the discussion occurred. 
#     If there are irrelevant topics mentioned, list them separately under an "Irrelevant Topics" title. 
#     Each title should be followed by a bullet-point list of the main discussion points with corresponding timestamps.
#     Text: {formatted_text}
#     """
#     model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 0})
#     response = model.generate_content([prompt])
#     return response.text


# # Convert video to audio
# def extract_audio_from_video(video_path):
#     audio_path = os.path.join(AUDIO_FOLDER, "input_audio.mp3")
#     subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path], 
#                     stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#     return audio_path

# # Convert audio to transcript
# def audio_to_transcript(audio_path):
#     whisper_model = "openai/whisper-base"
#     device = "cuda:0" if torch.cuda.is_available() else "cpu"
#     torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

#     model = AutoModelForSpeechSeq2Seq.from_pretrained(
#         whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True
#     ).to(device)

#     processor = AutoProcessor.from_pretrained(whisper_model)

#     speech_pipeline = pipeline(
#         "automatic-speech-recognition",
#         model=model,
#         tokenizer=processor.tokenizer,
#         feature_extractor=processor.feature_extractor,
#         return_timestamps=True,
#         chunk_length_s=30,
#         batch_size=8,
#         torch_dtype=torch_dtype,
#         device=device,
#     )

#     print("Processing audio... Please wait.")
#     try:
#         result = speech_pipeline(audio_path)
#     except Exception as e:
#         raise RuntimeError(f"Error during transcription: {e}")
#     print("Transcription completed.\n")

#     # Inspect the result structure
#     print("Raw Transcription Result:", result)

#     # Process result based on format
#     if "chunks" in result:
#         transcript_data = {
#             "segments": [
#                 {
#                     "start": chunk["timestamp"][0],
#                     "end": chunk["timestamp"][1],
#                     "text": chunk.get("text", ""),
#                 }
#                 for chunk in result["chunks"]
#             ]
#         }
#     elif isinstance(result, dict) and "text" in result:
#         # Fallback case: Treat the entire result as one segment
#         transcript_data = {
#             "segments": [{"start": 0, "end": 0, "text": result["text"]}]
#         }
#     else:
#         raise ValueError("The transcription output format is invalid or unsupported.")

#     # Clean up resources
#     del speech_pipeline, model, processor
#     torch.cuda.empty_cache()

#     return transcript_data



# def get_file_type(file_path):
#     # Create a magic object to identify file type
#     file_magic = magic.Magic(mime=True)
#     file_type = file_magic.from_file(file_path)
    
#     # Check if the file type indicates audio or video
#     if 'audio' in file_type:
#         return "Audio"
#     elif 'video' in file_type:
#         return "Video"
#     else:
#         return "Unknown file type"

# # Main script
# file = 'interview.mp4'  # Replace with your audio or video file path
# file_type = get_file_type(file)
# if file_type == "Video":
#     file = extract_audio_from_video(file)
# transcription_result = audio_to_transcript(file)

# # Print raw transcription with timestamps
# segments = transcription_result['segments']
# for segment in segments:
#     print(f"{segment['start']:0.2f}s - {segment['end']:0.2f}s: {segment['text']}")

# mom_result = generate_mom(transcription_result)

# # Print the generated meeting minutes
# print("\n\nMinutes of Meeting (MoM):\n")
# print(mom_result)

# import os
# import subprocess
# import torch
# import magic
# import warnings
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()
# warnings.filterwarnings("ignore")

# # Configure GenAI Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Directory to store audio files
# AUDIO_FOLDER = "AudioFile"
# os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # Function to generate Minutes of Meeting (MoM)
# def generate_mom(transcription_result):
#     segments = transcription_result['segments']
#     formatted_text = "\n".join(
#         [f"{seg['start']:0.2f}s - {seg['end']:0.2f}s: {seg['text']}" for seg in segments]
#     )
#     prompt = f"""
#     Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text, including timestamps.
#     For each relevant topic, create a single title and list the key points discussed under that title. 
#     Include timestamps for when the discussion occurred. 
#     If there are irrelevant topics mentioned, list them separately under an "Irrelevant Topics" title. 
#     Each title should be followed by a bullet-point list of the main discussion points with corresponding timestamps.
#     Text: {formatted_text}
#     """
#     model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 0})
#     response = model.generate_content([prompt])
#     return response.text


# # Convert video to audio
# def extract_audio_from_video(video_path):
#     audio_path = os.path.join(AUDIO_FOLDER, "input_audio.mp3")
#     subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path], 
#                     stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#     return audio_path

# # Convert audio to transcript
# def audio_to_transcript(audio_path):
#     whisper_model = "openai/whisper-base"
#     device = "cuda:0" if torch.cuda.is_available() else "cpu"
#     torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

#     model = AutoModelForSpeechSeq2Seq.from_pretrained(
#         whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True
#     ).to(device)

#     processor = AutoProcessor.from_pretrained(whisper_model)

#     speech_pipeline = pipeline(
#         "automatic-speech-recognition",
#         model=model,
#         tokenizer=processor.tokenizer,
#         feature_extractor=processor.feature_extractor,
#         return_timestamps=True,
#         chunk_length_s=30,
#         batch_size=8,
#         torch_dtype=torch_dtype,
#         device=device,
#     )

#     print("Processing audio... Please wait.")
#     try:
#         result = speech_pipeline(audio_path)
#     except Exception as e:
#         raise RuntimeError(f"Error during transcription: {e}")
#     print("Transcription completed.\n")

#     # Inspect the result structure
#     print("Raw Transcription Result:", result)

#     # Process result based on format
#     if "chunks" in result:
#         transcript_data = {
#             "segments": [
#                 {
#                     "start": chunk["timestamp"][0],
#                     "end": chunk["timestamp"][1],
#                     "text": chunk.get("text", ""),
#                 }
#                 for chunk in result["chunks"]
#             ]
#         }
#     elif isinstance(result, dict) and "text" in result:
#         # Fallback case: Treat the entire result as one segment
#         transcript_data = {
#             "segments": [{"start": 0, "end": 0, "text": result["text"]}]
#         }
#     else:
#         raise ValueError("The transcription output format is invalid or unsupported.")

#     # Clean up resources
#     del speech_pipeline, model, processor
#     torch.cuda.empty_cache()

#     return transcript_data



# def get_file_type(file_path):
#     # Create a magic object to identify file type
#     file_magic = magic.Magic(mime=True)
#     file_type = file_magic.from_file(file_path)
    
#     # Check if the file type indicates audio or video
#     if 'audio' in file_type:
#         return "Audio"
#     elif 'video' in file_type:
#         return "Video"
#     else:
#         return "Unknown file type"

# # Main script
# file = 'interview.mp4'  # Replace with your audio or video file path
# file_type = get_file_type(file)
# if file_type == "Video":
#     file = extract_audio_from_video(file)
# transcription_result = audio_to_transcript(file)

# # Print raw transcription with timestamps
# segments = transcription_result['segments']
# for segment in segments:
#     print(f"{segment['start']:0.2f}s - {segment['end']:0.2f}s: {segment['text']}")

# mom_result = generate_mom(transcription_result)

# # Print the generated meeting minutes
# print("\n\nMinutes of Meeting (MoM):\n")
# print(mom_result)



import os
import subprocess
import torch
import magic
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

# Function to convert seconds to hours, minutes, and seconds
def format_time(seconds):
    """
    Format time from seconds to HH:MM:SS.
    If seconds is None, default to 0.
    """
    if seconds is None:
        seconds = 0
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Function to generate Minutes of Meeting (MoM) with formatted time
def generate_mom(transcription_result):
    segments = transcription_result['segments']
    formatted_text = "\n".join(
        [f"{format_time(seg['start'])} - {format_time(seg['end'])}: {seg['text']}" for seg in segments]
    )
    prompt = f"""
    Please generate a concise and well-structured Minutes of Meeting (MoM) from the provided text, including timestamps.
    For each relevant topic, create a single title and list the key points discussed under that title. 
    Include timestamps for when the discussion occurred.  
    Each title should be followed by a bullet-point list of the main discussion points with corresponding timestamps.
    Text: {formatted_text}
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
    whisper_model = "Base_model"
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        whisper_model, torch_dtype=torch_dtype, low_cpu_mem_usage=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(whisper_model)

    speech_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        return_timestamps=True,
        chunk_length_s=30,
        batch_size=8,
        torch_dtype=torch_dtype,
        device=device,
    )

    print("Processing audio... Please wait.")
    try:
        result = speech_pipeline(audio_path)
    except Exception as e:
        raise RuntimeError(f"Error during transcription: {e}")
    # Developer Md Bikasuzzaman
    print("Transcription completed.\n")

    # Inspect the result structure
    # print("Raw Transcription Result:", result)

    # Process result based on format
  
    # Handle transcription result
    if isinstance(result, dict) and "chunks" in result:
        transcript_data = {
            "segments": [
                {
                    "start": chunk["timestamp"][0],
                    "end": chunk["timestamp"][1],
                    "text": chunk["text"],
                }
                for chunk in result["chunks"]
            ]
        }
    elif isinstance(result, dict) and "text" in result:
        transcript_data = {
            "segments": [{"start": 0, "end": 0, "text": result["text"]}]
        }
    else:
        raise ValueError("Invalid transcription output format.")

    # Clean up resources
    del speech_pipeline, model, processor
    torch.cuda.empty_cache()

    return transcript_data

# Function to determine the file type (audio or video)
def get_file_type(file_path):
    # Create a magic object to identify file type
    file_magic = magic.Magic(mime=True)
    file_type = file_magic.from_file(file_path)
    
    # Check if the file type indicates audio or video
    if 'audio' in file_type:
        return "Audio"
    elif 'video' in file_type:
        return "Video"
    else:
        return "Unknown file type"

# Main script
file = 'videoplayback.mp4'  # Replace with your audio or video file path
file_type = get_file_type(file)
if file_type == "Video":
    file = extract_audio_from_video(file)
transcription_result = audio_to_transcript(file)

# Print raw transcription with timestamps
segments = transcription_result['segments']
# for segment in segments:
#     print(f"{format_time(segment['start'])} - {format_time(segment['end'])}: {segment['text']}")

mom_result = generate_mom(transcription_result)

# Print the generated meeting minutes
print("\n\nMinutes of Meeting (MoM):\n")
print(mom_result)
