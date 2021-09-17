#!/usr/bin/env bash
SRC_LANG=$1
TGT_LANG=$2
DATA_DIR=$3
OUT_DIR=$4
NUM_TRAIN_STEPS=$5
LEARNING_RATE=$6
WARMUP_STEPS=$7
cd nmt
python -m nmt.nmt --src=$SRC_LANG --tgt=$TGT_LANG --vocab_prefix=../$DATA_DIR/vocab --dev_prefix=../$DATA_DIR/dev --test_prefix=../$DATA_DIR/test --train_prefix=../$DATA_DIR/train --out_dir=OUT_DIR --num_train_steps=$NUM_TRAIN_STEPS --attention=bahdanau --steps_per_stats=100 --num_layers=2 --num_units=500 --dropout=0.2 --metrics=accuracy --log_device_placement --learning_rate=$LEARNING_RATE --decay_scheme=luong10 --warmup_steps=$WARMUP_STEPS --warmup_scheme=t2t
cd ..