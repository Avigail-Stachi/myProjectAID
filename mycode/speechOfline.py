from vosk import Model, KaldiRecognizer
import wave
import json
import subprocess
from vosk import SetLogLevel
SetLogLevel(-1)
def convert_format(input_path, output_path):
    ffmpeg_path=r"C:\ffmpeg\bin\ffmpeg.exe"
    command = [
        ffmpeg_path,
        "-loglevel", "quiet",  # רק שגיאות חזקות
        "-y",                  # overwrite בלי לשאול
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-sample_fmt", "s16",
        output_path
    ]
    subprocess.run(command, check=True)


def transcribe_audio(wav_path, model_path_vosk):
    wf = wave.open(wav_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio file must be mono, 16-bit, and 16000 Hz")

    model = Model(model_path_vosk)
    rec = KaldiRecognizer(model, wf.getframerate())

    audio_data = wf.readframes(wf.getnframes())
    rec.AcceptWaveform(audio_data)

    result = json.loads(rec.FinalResult()) #ממיר למילון
    return result.get("text", "")

model_path_vosk = r"C:\project\myModel\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
input_path = r"C:\Users\User\Documents\Sound Recordings\Recording.m4a"  # אפשר כל סוג
wav_path = r"C:\project\myModel\mycode.wav"
convert_format(input_path, wav_path)
text = transcribe_audio(wav_path, model_path_vosk)
print("Recognized text:", text)


