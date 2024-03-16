import click

import blah
from blah.typing._common import Filepath


@click.group(help="Simple low-resouce word recognition tool.")
def cli() -> None:
    pass


@cli.command(help="Train a new word recognition model.")
@click.argument("model", metavar="OUTPUT_MODEL", type=click.Path())
@click.option("-c", "--config", metavar="CONFIG",
              required=True, type=click.Path(exists=True),
              help="Training set configuration.")
def train(model: Filepath, config: Filepath) -> None:
    blah.train(config, model)


@cli.command(help="Recognize a spoken word.")
@click.argument("audio", metavar="INPUT_AUDIO", type=click.Path(exists=True))
@click.option("-m", "--model", metavar="MODEL",
              required=True, type=click.Path(exists=True),
              help="Word recognition model.")
def analyze(audio: Filepath, model: Filepath) -> None:
    print(blah.analyze(blah.Audio.from_file(audio), model))


if __name__ == "__main__":
    cli()
