import webrtcvad
import pyaudio
import collections
import time
import threading


class AudioMonitor:
    def __init__(self, flag_callback, face_monitor, aggressiveness=3):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.flag_callback = flag_callback
        self.face_monitor = face_monitor
        self.chunk_duration_ms = 30
        self.sample_rate = 16000
        self.chunk_size = int(self.sample_rate * self.chunk_duration_ms / 1000)
        self.format = pyaudio.paInt16
        self.channels = 1
        self.running = False

    def start_monitoring(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk_size)

        ring_buffer = collections.deque(maxlen=10)
        print("[AudioMonitor] Listening for speaking...")

        self.running = True
        while self.running:
            audio = stream.read(self.chunk_size, exception_on_overflow=False)
            is_speech = self.vad.is_speech(audio, self.sample_rate)
            lip_recent = self.face_monitor.is_lip_moving_recently()
            ring_buffer.append(1 if is_speech else 0)
            print(f"[Debug] is_speech={is_speech}, lip_recent={lip_recent}, buffer={list(ring_buffer)}")

            if sum(ring_buffer) > 9 and lip_recent:
                print("[AudioMonitor] 💬 Speaking Detected (voice + lips)")
                self.flag_callback("speaking")
                ring_buffer.clear()
                time.sleep(2)


        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_monitoring(self):
        self.running = False
