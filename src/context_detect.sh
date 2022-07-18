#!/bin/sh
cd sppmi_svd

python split_period.py -d ../../data/parsed_hd.csv \
       -a ../../cache/after.txt \
       -b ../../cache/before \
       -p 3

python counter_from_doc.py -f ../../cache/before.txt -c before.pkl
python counter_from_doc.py -f ../../cache/after.txt -c after.pkl

python id2word_from_counter.py --count_dic after.pkl before.pkl \
       --threshold 0

python main.py --file_path ../../cache/before.txt \
    --name before \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1 
python main.py --file_path ../../cache/after.txt \
    --name after \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1

python save_joint_pmi.py --dic_id2word dic_id2word.pkl \
       --path_models model/after_SPPMI_w-2_s-1 model/before_SPPMI_w-2_s-1 \
       --dim 1000

python most_changed.py -p dic_id2word.pkl \
       -m WV_joint_dim-*.npy \
       -n 2000

# mv model/ ../../cache/sppmi-model/
