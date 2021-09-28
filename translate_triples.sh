#!/usr/bin/env bash

SRC_LANG=$1
TGT_LANG=$2
IN_FILE=$3
OUT_FILE=$4
LOG_DIR=$5
VOCAB_DIR=$6
MODEL_DIR=$6
cd nmt
python -m nmt.nmt  --vocab_prefix=$VOCAB_DIR --model_dir=$MODEL_DIR  --inference_input_file=$IN_FILE  --inference_output_file=$OUT_FILE --out_dir=$LOG_DIR --src=$SRC_LANG --tgt=$TGT_LANG
echo "Translation complete."