from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Specify the model name
# model_name = "openai/whisper-large-v3"
# model_name = "openai/whisper-base"
model_name = "openai/whisper-large-v3-turbo"

# Load the processor and model
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

# Specify your local directory
save_directory = "Turbo_model"
import os
os.makedirs(save_directory, exist_ok=True)

# Save the processor and model locally
processor.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"Model and processor saved to {save_directory}")
