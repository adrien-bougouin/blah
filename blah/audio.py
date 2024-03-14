from __future__ import annotations

from typing import Type

import librosa

from blah.typing._common import Filepath
from blah.typing.audio import AudioData, AudioSampleRate


class Audio:
    @classmethod
    def from_file(cls: Type[Audio], filepath: Filepath) -> Audio:
        data, sample_rate = librosa.load(filepath)

        return cls(data, sample_rate)

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
