import threading

import numpy
import pyaudio

from blah import Audio
from blah.typing.audio import AudioData, AudioSampleRate


class AudioRecorder:
    FRAMES_PER_BUFFER: int = 1024

    def __init__(
        self,
        sample_rate: AudioSampleRate = Audio.DEFAULT_SAMPLE_RATE,
    ) -> None:
        self.sample_rate = sample_rate

        self._audio_controller = pyaudio.PyAudio()
        self._recording_thread: None | threading.Thread = None
        self._last_recording: AudioData = numpy.array([])
        self._recording = False

    def __del__(self) -> None:
        self.stop()
        self._audio_controller.terminate()

    def start(self) -> None:
        if self._recording:
            return
        if self._recording_thread is not None:
            return

        self._recording = True

        self._recording_thread = threading.Thread(target=self._record)

        self._recording_thread.start()

    def stop(self) -> Audio:
        self._recording = False

        if self._recording_thread is not None:
            self._recording_thread.join()
            self._recording_thread = None

        return Audio(self._last_recording, self.sample_rate)

    def _record(self) -> None:
        frames = []
        stream = self._audio_controller.open(
            self.sample_rate,
            1,
            pyaudio.paFloat32,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
            input=True
        )

        while self._recording:
            frames.append(
                stream.read(self.FRAMES_PER_BUFFER)
            )

        self._last_recording = numpy.frombuffer(
            b''.join(frames),
            dtype=numpy.float32
        )

        stream.close()
