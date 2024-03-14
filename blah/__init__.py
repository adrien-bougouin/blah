__version__ = "0.1.0"
__all__ = [
    "analyze",
    "Audio",
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


def train(config_filepath: Filepath, model_output_filepath: Filepath) -> None:
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        config = toml.loads(config_file.read())

    training_directory = config["directory"]

    classifier = mir.WordClassifier()
    training_samples = []
    training_classes = []

    for word in config["words"]:
        for sample_filename in config[word]["samples"]:
            sample_filepath = os.path.join(training_directory, sample_filename)

            training_samples.append(Audio.from_file(sample_filepath))
            training_classes.append(word)

    classifier.train(training_samples, training_classes)

    with open(model_output_filepath, "wb") as model_output_file:
        pickle.dump(classifier, model_output_file)


def analyze(audio: Audio, model_filepath: Filepath) -> WordClass:
    with open(model_filepath, "rb") as model_file:
        classifier = pickle.load(model_file)

    return classifier.classify(audio)
