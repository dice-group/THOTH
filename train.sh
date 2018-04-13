#!/usr/bin/env bash
cd nmt
python -m nmt.nmt --src=$1 --tgt=$2 --vocab_prefix=../$3/vocab --dev_prefix=../$3/dev --test_prefix=../$3/test --train_prefix=../$3/train --out_dir=../$3_model --num_train_steps=$4 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=accuracy
cd ..
