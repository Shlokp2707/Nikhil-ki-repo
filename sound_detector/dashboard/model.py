# ==========================
# IMPORTS
# ==========================
import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import tensorflow as tf
import matplotlib.pyplot as plt
from langchain_core.messages import HumanMessage
import os
BASE_DIR =os.path.dirname(os.path.abspath(__file__))
# ==========================
# CONFIG (MATCH TRAINING)
# ==========================
MODEL_PATH = os.path.join(BASE_DIR,"esc50_sound111.keras")

SAMPLE_RATE = 16000
DURATION = 5
TARGET_SAMPLES = SAMPLE_RATE * DURATION

N_MELS = 128
HOP_LENGTH = 512
FMAX = 8000

# ==========================
# CLASS NAMES
# ==========================
CLASS_NAMES = [
    "footsteps", "glass_breaking", "mouse_click","dog","sneezing", "clapping",
    "laughing", "door_wood_knock", "door_wood_creaks",
    "wood_crack","keyboard_typing"
 
]
# ==========================
# LOAD MODEL
# ==========================
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded")
# ==========================
# RECORD AUDIO
# ==========================

def record_audio():
    print("🎙️ Recording for 5 seconds...")
    buffer = []

    def callback(indata, frames , time_info, status):
        if status:
            print(status)
        buffer.append(indata.copy())

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=callback,
            blocksize=1024  # IMPORTANT: stabilizes callback
        ):
            sd.sleep(int(DURATION * 1000))

    except Exception as e:
        print("Audio stream error:", e)

    if len(buffer) == 0:
        return np.zeros(SAMPLE_RATE * DURATION, dtype=np.float32)

    audio = np.concatenate(buffer, axis=0).flatten()
    return audio

# ==========================
# SILENCE CHECK (OPTIONAL BUT GOOD)
# ==========================
def is_silence(y, threshold=0.0015): 
    rms = librosa.feature.rms(y=y)

    return np.mean(rms) < threshold
# ==========================
# AUDIO → MEL
# =========================
def audio_to_mel(y):
    if len(y) < TARGET_SAMPLES:
        y = np.pad(y, (0, TARGET_SAMPLES - len(y)))
    else:
        y = y[:TARGET_SAMPLES]

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=SAMPLE_RATE,
        n_mels=N_MELS,
        hop_length=HOP_LENGTH,
        fmax=FMAX
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)
    return mel_db

# ==========================
# PREDICT SOUND
# ==========================
from datetime import datetime, date
def predict_sound(iter):
    li = []
    i =0
    while(i<iter):
        audio = record_audio()

        sd.wait()
    # Silence check
        if is_silence(audio):
            # continue
            print("🤫 Silence detected. Skipping prediction.")
  
        else:
            mel = audio_to_mel(audio)
            # show_mel(mel)
            mel = mel[..., np.newaxis]
            mel = np.expand_dims(mel, axis=0)

            preds = model.predict(mel, verbose=0)
            idx = np.argmax(preds)
            conf = preds[0][idx]

            # print("\n🔊 Prediction Result")
            # print("Class      :", CLASS_NAMES[idx])
            # print("Confidence :", round(conf * 100, 2), "%")
            # dic ={
            #     "class":CLASS_NAMES[idx],
            #     "confidence":round(conf*100,2),
            #     "cur_time":datetime.now().time().strftime("%H:%M:%S"),
            #     "date":datetime.now().date()
            # }

            li.append(HumanMessage(content = f"confidence = {round(conf,2)}, class = {CLASS_NAMES[idx]}, time = {datetime.now().time().strftime("%H:%M:%S")}, date = {date.today()}"))            
        i+=1
    return li
# ==========================
# RUN LOOP
# ==========================
# if __name__ == "__main__":         
#     print("Press ENTER to record (Ctrl+C to exit)")
#     while True:
#         input()
#         predict_sound()