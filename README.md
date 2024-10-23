# Blah

Simple single-word speech recognizer

## Usage

1. Setup: `make doctor && make deps`
2. Train a new word recognition model: `pipenv run train --config CONFIG OUTPUT_MODEL`
3. Recognize a spoken word from audio record: `pipenv run analyze --model MODEL INPUT_AUDIO`
4. Push-to-talk work recognizer (work-in-progress): `pipenv run ptt --model MODEL --now`

## Examples

See `./examples` and run `make examples` for more. Look at `examples/train/config.toml` for an example configuration for the model training.
