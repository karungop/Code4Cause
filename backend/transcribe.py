import torch
import torchaudio
import wave
import threading
from datetime import datetime
from pynput import keyboard
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os
import pyaudio

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

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print("🎙️ Recording started. Press 's' to stop...")

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

        print("🛑 Recording stopped")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_audio_{timestamp}.wav"

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

        print(f"💾 Audio saved to {filename}")
        return filename

def transcribe_audio(filepath):
    print("🧠 Loading model for transcription...")
    processor = AutoProcessor.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("rishabhjain16/whisper_medium_en_to_myst_pf")

    audio, rate = torchaudio.load(filepath)
    if rate != 16000:
        audio = torchaudio.functional.resample(audio, orig_freq=rate, new_freq=16000)

    inputs = processor(audio.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")

    with torch.no_grad():
        predicted_ids = model.generate(inputs["input_features"])

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    print("📝 Transcription:", transcription)

def delete_recording(filepath):
    os.remove(filepath)
    
def on_press(key, recorder):
    try:
        if key.char == 'r' and not recorder.recording:
            recorder.start_recording()
        elif key.char == 's' and recorder.recording:
            filepath = recorder.stop_recording()
            if filepath:
                transcribe_audio(filepath)
                delete_recording(filepath)
    except AttributeError:
        pass

def on_release(key, recorder):
    if key == keyboard.Key.esc:
        if recorder.recording:
            recorder.stop_recording()
        return False


def main():
    recorder = AudioRecorder()
    print("🔴 Press 'r' to start recording, 's' to stop and transcribe, 'esc' to quit")

    with keyboard.Listener(
        on_press=lambda key: on_press(key, recorder),
        on_release=lambda key: on_release(key, recorder)
    ) as listener:
        listener.join()

    

if __name__ == "__main__":
    main()
