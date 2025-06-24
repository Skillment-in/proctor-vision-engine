import webrtcvad
import pyaudio
import collections
import time
import threading

class AudioMonitor:
    def __init__(self, flag_callback, aggressiveness=3):  # Set to most strict
        self.vad = webrtcvad.Vad(aggressiveness)  # 0 = sensitive, 3 = strict
        self.flag_callback = flag_callback
        self.chunk_duration_ms = 30  # each audio chunk is 30ms
        self.sample_rate = 16000
        self.chunk_size = int(self.sample_rate * self.chunk_duration_ms / 1000)  # 480
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
        print("[AudioMonitor]  Listening for real speech...")
        self.running = True

        while self.running:
            audio = stream.read(self.chunk_size, exception_on_overflow=False)
            is_speech = self.vad.is_speech(audio, self.sample_rate)

            ring_buffer.append(1 if is_speech else 0)

            # More strict: Require 10/10 positive speech detections
            if sum(ring_buffer) > 9:
                print("[AudioMonitor] Speech Detected!")
                self.flag_callback("speaking")  # More meaningful flag name
                ring_buffer.clear()
                time.sleep(5)  # Cooldown to prevent rapid repeat triggers

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_monitoring(self):
        self.running = False
