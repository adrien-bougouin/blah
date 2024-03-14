import argparse

import blah


def build_cli() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Simple low-resouce word recognition tool."
    )
    cli_commands = cli.add_subparsers(required=True)
    train_command = cli_commands.add_parser(
        "train",
        description="Train a new word recognition model.",
        help="train a new word recognition model"
    )
    analyze_command = cli_commands.add_parser(
        "analyze",
        description="Recognize a spoken word.",
        help="recognize a spoken word"
    )

    cli.add_argument(
        "--version", "-v", action="version",
        version="%(prog)s " + blah.__version__
    )

    train_command.set_defaults(command="train")
    setup_train_command(train_command)

    analyze_command.set_defaults(command="analyze")
    setup_analyze_command(analyze_command)

    return cli


def setup_train_command(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "model", metavar="MODEL_FILEPATH", type=str,
        help="output model"
    )
    command.add_argument(
        "-c", "--config", metavar="CONFIG_FILEPATH", type=str, required=True,
        help="training set configuration"
    )


def setup_analyze_command(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "audio", metavar="AUDIO_FILEPATH", type=str,
        help="audio record of the word to recognize"
    )
    command.add_argument(
        "-m", "--model", metavar="MODEL_FILEPATH", type=str, required=True,
        help="word recognition model"
    )


if __name__ == "__main__":
    cli_arguments = build_cli().parse_args()

    match cli_arguments.command:
        case "train":
            blah.train(cli_arguments.config, cli_arguments.model)
        case "analyze":
            print(
                blah.analyze(
                    blah.Audio.from_file(cli_arguments.audio),
                    cli_arguments.model
                )
            )
