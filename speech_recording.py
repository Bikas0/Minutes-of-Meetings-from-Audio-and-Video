import os
import wave
import pyaudio
import warnings
warnings.filterwarnings("ignore")


def SpeechRecord(FOLDER):
    # Audio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    SECONDS = 10

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # List available devices
    device_count = p.get_device_count()
    print("Available devices:")
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}, input: {device_info['maxInputChannels']}")

    # Choose the input device (if the correct device is not the default one)
    input_device_index = None
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        # Developer Md Bikasuzzaman
        if device_info['maxInputChannels'] > 0:  # Only consider devices that can be used for input
            input_device_index = i
            break

    if input_device_index is None:
        print("No input device found.")
        p.terminate()
        exit()

    # Open the audio stream with the specified device
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=CHUNK)

    print("Start recording...")

    # Record the audio
    frames = []
    for i in range(0, int(RATE / CHUNK * SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(os.path.join(FOLDER, "input_audio.mp3"), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Audio saved as 'input_audio.mp3'.")
