__version__ = "0.3.0"
__all__ = [
    "analyze",
    "Audio",
    "load",
    "mir",
    "train"
]

import os.path
import pickle

import toml

from . import mir
from .audio import Audio
from .typing._common import Filepath
from .typing.mir import WordClass


def _dump(
    classifier: mir.WordClassifier,
    output_filepath: Filepath
) -> None:
    # pylint: disable=protected-access
    with open(output_filepath, "wb") as output_file:
        pickle.dump(
            [
                classifier._sample_rate,
                classifier._svm,
                classifier._embedding_dimensions
            ],
            output_file
        )


def load(model_filepath: Filepath) -> mir.WordClassifier:
    with open(model_filepath, "rb") as model_file:
        classifier = mir.WordClassifier(*pickle.load(model_file))
    return classifier


def train(config_filepath: Filepath, model_output_filepath: Filepath) -> None:
    classifier = mir.WordClassifier()
    base_directory = os.path.dirname(config_filepath)

    with open(config_filepath, "r", encoding="utf-8") as config_file:
        config = toml.loads(config_file.read())

    training_samples = []
    training_classes = []

    for audio_samples in config["audio_samples"]:
        word = audio_samples["class"]
        directory = os.path.normpath(
            os.path.join(
                base_directory,
                os.path.expanduser(audio_samples["directory"])
            )
        )

        for sample_filename in audio_samples["samples"]:
            sample_filepath = os.path.join(directory, sample_filename)

            training_samples.append(Audio.from_file(sample_filepath))
            training_classes.append(word)

    classifier.train(training_samples, training_classes)

    _dump(classifier, model_output_filepath)


def analyze(audio: Audio, model_filepath: Filepath) -> WordClass:
    return load(model_filepath).classify(audio)
