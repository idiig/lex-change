#!/bin/sh

python main.py --file_path //sub_after_3.txt \
    --name sub_after_3 \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1 


