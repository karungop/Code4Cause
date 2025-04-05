from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchaudio
import wave
import threading
from datetime import datetime
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os
import pyaudio

app = Flask(__name__)
CORS(app)

# Load processor and model once
processor = AutoProcessor.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")
model = AutoModelForSpeechSeq2Seq.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")

class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.frames = []
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None


    def start_recording(self):
        if self.recording:
            return
        self.frames = []
        self.recording = True

        # Remove the `input_device_index` so it uses the default input device
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        threading.Thread(target=self._record, daemon=True).start()

    def _record(self):
        while self.recording:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

    def stop_recording(self):
        if not self.recording:
            return None

        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()  # Explicitly terminate the audio stream to clean up resources

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_audio_{timestamp}.wav"

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

        return filename

def transcribe_audio(filepath):
    audio, rate = torchaudio.load(filepath)
    
    # Ensure audio file is not empty
    if audio.numel() == 0:
        raise ValueError(f"Audio file {filepath} is empty.")

    if rate != 16000:
        audio = torchaudio.functional.resample(audio, orig_freq=rate, new_freq=16000)

    inputs = processor(audio.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")

    with torch.no_grad():
        predicted_ids = model.generate(inputs["input_features"])

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription

def delete_recording(filepath):
    os.remove(filepath)

recorder = AudioRecorder()
current_filepath = None

@app.route('/start', methods=['POST'])
def start():
    if not recorder.recording:
        recorder.start_recording()
        return jsonify({"status": "recording started"})
    return jsonify({"status": "already recording"}), 400

@app.route('/stop', methods=['POST'])
def stop():
    global current_filepath
    if recorder.recording:
        current_filepath = recorder.stop_recording()
        if current_filepath:
            try:
                transcription = transcribe_audio(current_filepath)
                return jsonify({"status": "recording stopped", "transcription": transcription})
            finally:
                delete_recording(current_filepath)  # Ensure the recording is deleted after use
    return jsonify({"status": "not recording"}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
