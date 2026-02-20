🎧 Smart Home Ear
Real-Time Environmental Sound Detection System

Smart Home Ear is a real-time sound classification system that listens through a microphone, converts audio into Mel spectrograms, and predicts environmental sounds using a deep learning model.

It is designed for smart home monitoring and intelligent sound awareness.

🚀 Features

🎙️ 5-second real-time audio recording

🔊 Playback of recorded sound

📊 Mel spectrogram visualization

🧠 CNN-based sound classification

📈 Confidence score output

🧠 Model Details

Framework: TensorFlow / Keras

Sampling Rate: 16 kHz

Input: 128-band Mel Spectrogram

Duration: 5 seconds

Output: Softmax probability distribution

🎯 Detected Sound Classes

Footsteps, Breathing, Coughing, Sneezing, Clapping, Laughing,
Glass breaking, Door knock, Door creak, Wood crack, Clock tick,
Keyboard typing, Mouse click, Washing machine, Vacuum cleaner,
Thump, Slam, Dog bark.

🔁 System Flow
Microphone
   ↓
Audio Preprocessing
   ↓
Mel Spectrogram Extraction
   ↓
CNN Model
   ↓
Prediction + Confidence
🛠️ Tech Stack

Python • TensorFlow • Librosa • NumPy • SoundDevice • Matplotlib

⚠️ Limitations

Single-label classification

Sensitive to background noise

Depends on microphone quality

👨‍💻 Author

Shlok Pandey
B.Tech CSE | ML & AI Enthusiast |Full-Stack Developer
Passionate about building unique real-world AI systems.
