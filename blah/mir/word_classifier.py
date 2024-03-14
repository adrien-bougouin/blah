from typing import Optional

import librosa
import sklearn.svm

from blah.audio import Audio
from blah.typing.audio import AudioSampleRate
from blah.typing.mir import EmbeddingsVector, SpeechFeatures, WordClass

from . import speech


class WordClassifier:
    def __init__(
        self,
        svm: Optional[sklearn.svm.LinearSVC] = None,
        embedding_dimensions: Optional[list[SpeechFeatures]] = None,
        sample_rate: AudioSampleRate = 22050,
    ) -> None:
        self._sample_rate = sample_rate
        self._svm = svm or sklearn.svm.LinearSVC(dual=True, max_iter=100000)

        if embedding_dimensions is None:
            self._embedding_dimensions = []
        else:
            self._embedding_dimensions = embedding_dimensions

    def train(
        self,
        audio_examples: list[Audio],
        classes: list[WordClass]
    ) -> None:
        self._embedding_dimensions = [
            self._extract_features(audio.sampled_at(self._sample_rate))
            for audio
            in audio_examples
        ]
        self._svm.fit(
            [
                self._compute_vector_embedding(features)
                for features
                in self._embedding_dimensions
            ],
            classes
        )

    def classify(self, audio: Audio) -> WordClass:
        return self._svm.predict([
            self._compute_vector_embedding(
                self._extract_features(
                    audio.sampled_at(self._sample_rate)
                )
            )
        ])[0]

    def _extract_features(self, audio: Audio) -> SpeechFeatures:
        return speech.extract_features(
            speech.preprocess(audio)
        )

    def _compute_vector_embedding(
        self,
        features: SpeechFeatures
    ) -> EmbeddingsVector:
        vector_embedding = []

        for dimension_features in self._embedding_dimensions:
            vector_embedding.append(
                librosa.sequence.dtw(
                    features,
                    dimension_features,
                    backtrack=False
                )[-1][-1]
            )

        return vector_embedding
