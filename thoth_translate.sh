#!/usr/bin/env bash

cd nmt
echo "$2" > to_ask.txt
python -m nmt.nmt  --vocab_prefix=../$1/vocab --model_dir=../$1_model  --inference_input_file=./to_ask.txt  --inference_output_file=./output.txt --out_dir=../$1_model --src=en --tgt=sparql > /dev/null 2>&1

if [ $? -eq 0 ]
then
    echo ""
    echo "ANSWER IN TARGET LANGUAGE:"
    cat output.txt
    echo ""
fi

cd ..

