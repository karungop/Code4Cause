import torch
import torchaudio

# Load model directly
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")
model = AutoModelForSpeechSeq2Seq.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")

# Load and preprocess audio
audio, rate = torchaudio.load("your_audio.wav")
if rate != 16000:
    audio = torchaudio.functional.resample(audio, orig_freq=rate, new_freq=16000)

# Process the input
inputs = processor(audio.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")

# Generate prediction
with torch.no_grad():
    predicted_ids = model.generate(inputs["input_features"])

# Decode output
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
print("Transcription:", transcription)