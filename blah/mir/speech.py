import librosa
import numpy

from blah.audio import Audio
from blah.typing.mir import SpeechFeatures


def preprocess(audio: Audio) -> Audio:
    return Audio(
        librosa.effects.trim(
            # This filter amplifies high frequencies, which are parts of the
            # audio that changes rapidly. Lower frequencies are not as
            # important because they are not trivial in detecting audio
            # similarities.
            # --https://audiovideotestlab.com/blog/audio-comparison-using-mfcc-and-dtw/
            librosa.effects.preemphasis(audio.data)
        )[0],
        audio.sample_rate
    )


def extract_features(audio: Audio) -> SpeechFeatures:
    power_spectrogram = numpy.abs(
        librosa.stft(
            audio.data,
            # In speech processing, the recommended value is 512, corresponding
            # to 23 milliseconds at a sample rate of 22050 Hz.
            # --https://librosa.org/doc/main/generated/librosa.stft.html
            n_fft=512,
            # https://audiovideotestlab.com/blog/audio-comparison-using-mfcc-and-dtw/.
            window="hamming"
        )
    )**2

    # As humans don't interpret pitch in a linear manner, the Mel scale of
    # frequencies were devised to represent the way humans hear the distances
    # between pitches.
    # --https://github.com/meyda/meyda/blob/main/docs/audio-features.md
    return librosa.feature.mfcc(
        S=librosa.feature.melspectrogram(
            S=power_spectrogram,
            sr=audio.sample_rate
        ),
        sr=audio.sample_rate
    )
