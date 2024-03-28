#!/usr/bin/env bash

if [[ $# -ne 3 ]]; then
  cat <<- MSG
		Usage: $0 LANGUAGE WORD_LIST OUTPUT_DIRECTORY

		Example:
		  $0 en_US "foo bar baz" ./train_2020911
	MSG

  exit 1
fi

if [[ ! $(command -v say) ]]; then
  echo "Error: This tool was made for macOS with the built-in \`say\` command."
  exit 1
fi

if [[ ! $(command -v ffmpeg) ]]; then
  echo "Error: This tool requires \`ffmpeg\`."
  exit 1
fi

language=$1
words=($2)
output_directory=$3

IFS=$'\n' voices=(
  $(say -v "?" | grep ${language} | awk -F "${language}" '{ gsub(/ +$/, "", $1); print $1 }')
)

samples_directory="${output_directory}/samples"
mkdir -p "${samples_directory}"

for word in ${words[@]}; do
  echo "[[audio_samples]]"
  echo "class = \"${word}\""
  echo "directory = \"samples\""

  echo "samples = ["
  for voice in ${voices[@]}; do
    short_voice_name=$(echo "${voice}" | awk '{ print $1 }')
    output_audio_filename=$(echo "${word}_${short_voice_name}" | tr '[:upper:]' '[:lower:]')
    say_output_filepath="${samples_directory}/${output_audio_filename}.aiff"

    echo "  \"${output_audio_filename}.wav\","
    say -v "${voice}" "${word}"
    say -v "${voice}" "${word}" -o "${say_output_filepath}"
    ffmpeg -i "${say_output_filepath}" "${samples_directory}/${output_audio_filename}.wav"
    rm "${say_output_filepath}"
  done
  echo "]"
  echo ""
done > "${output_directory}/config.toml"
