#!/bin/bash

# just have ./input folder with normal .mp4 files, then ./input/gt/ folder with _gt.mp4 files

runFile() {
  filepath=$1
  # 111.mp4
  filename=${filepath##*/}
  # 111.txt
  output=${filename%.mp4}.txt
  # ./experiments/111.txt
  output_filepath="./experiments/$output"
  # ./input/gt/111_gt.mp4
  gt=./input/gt/${filename%.mp4}_gt.mp4
  python -m cvapr.boilerplate --input="$filepath" --algo=MOG --gt="$gt" >> "$output_filepath"
  python -m cvapr.boilerplate --input="$filepath" --algo=MOG2 --gt="$gt" >> "$output_filepath"
  python -m cvapr.boilerplate --input="$filepath" --algo=KNN --gt="$gt" >> "$output_filepath"
  sed -i 's/Experiment finished//g' "$output_filepath"
}

for file in ./input/*.mp4; do
  echo "$file"
  runFile "$file" &
done
