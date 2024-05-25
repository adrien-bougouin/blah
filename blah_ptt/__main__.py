import time

import click

import blah
from blah.typing._common import Filepath

import blah_ptt


@click.command(help="Start push-to-talk word recognizer.")
@click.option(
    "-m", "--model", metavar="MODEL",
    required=True, type=click.Path(exists=True),
    help="Word recognition model."
)
@click.option(
    "-n", "--now",
    is_flag=True,
    help="Don't actually wait for push action; Just run once right away."
)
def start(model: Filepath, now: bool) -> None:
    classifier = blah.load(model)
    recorder = blah_ptt.AudioRecorder()

    if now:
        recorder.start()
        print("Recording...")
        time.sleep(2)
        print("Done...")
        record = recorder.stop()

        print(classifier.classify(record))
        return


if __name__ == "__main__":
    start()  # pylint: disable=no-value-for-parameter
