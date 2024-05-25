from __future__ import annotations

from typing import Type

import librosa

from blah.typing._common import Filepath
from blah.typing.audio import AudioData, AudioSampleRate


class Audio:
    DEFAULT_SAMPLE_RATE: AudioSampleRate = 22050

    @classmethod
    def from_file(cls: Type[Audio], filepath: Filepath) -> Audio:
        data, _ = librosa.load(filepath, sr=cls.DEFAULT_SAMPLE_RATE)

        return cls(data, cls.DEFAULT_SAMPLE_RATE)

    def __init__(self, data: AudioData, sample_rate: AudioSampleRate) -> None:
        self.data = data
        self.sample_rate = sample_rate

    def sampled_at(self, sample_rate: AudioSampleRate) -> Audio:
        if sample_rate == self.sample_rate:
            return self

        return Audio(
            librosa.resample(
                self.data,
                orig_sr=self.sample_rate,
                target_sr=sample_rate
            ),
            sample_rate
        )
