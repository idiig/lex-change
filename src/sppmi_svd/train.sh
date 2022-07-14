#!/bin/sh
python counter_from_doc.py -f ../../data/before.txt -c ../../data/before.pkl
python counter_from_doc.py -f ../../data/after.txt -c ../../data/after.pkl
python id2word_from_counter.py --count_dic after.pkl before.pkl --threshold 0
python main.py --file_path after.txt \
    --name after \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1 
