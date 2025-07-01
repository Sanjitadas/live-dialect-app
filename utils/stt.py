# utils/stt.py
import whisper
import pyaudio
import numpy as np
import torch
import time
import wave

model = whisper.load_model("base")

def capture_streaming(callback, lang="en"):
    RATE = 16000
    CHUNK = int(RATE / 4)  # 250ms
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RECORD_SECONDS = 30  # fallback safety

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎤 Listening live... Press Ctrl+C to stop")
    frames = []
    start_time = time.time()

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(np.frombuffer(data, dtype=np.int16))

            # Process every second
            if len(frames) >= int(RATE / CHUNK):
                audio_np = np.concatenate(frames[-int(RATE / CHUNK):])
                audio_fp = f"temp_stream.wav"
                wf = wave.open(audio_fp, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(audio_np.tobytes())
                wf.close()

                result = model.transcribe(audio_fp, language=lang, fp16=torch.cuda.is_available())
                if result["text"].strip():
                    callback(result["text"].strip())

            # Stop after timeout
            if time.time() - start_time > RECORD_SECONDS:
                break

    except KeyboardInterrupt:
        print("\n🛑 Live stream stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    