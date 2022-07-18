#!/bin/sh
python counter_from_doc.py -f ../../cache/before.txt -c before.pkl
python counter_from_doc.py -f ../../cache/after.txt -c after.pkl
echo "Counter from doc finished."

python id2word_from_counter.py --count_dic after.pkl before.pkl \
       --threshold 0
echo "ID to word from counter finished."

python main.py --file_path ../../cache/before.txt \
    --name before \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1 
python main.py --file_path ../../cache/after.txt \
    --name after \
    --pickle_id2word dic_id2word.pkl \
    --threshold 0 --has_cds --window_size 2 --shift 1
echo "finished train."

python save_joint_pmi.py --dic_id2word dic_id2word.pkl \
       --path_models model/after_SPPMI_w-2_s-1 model/before_SPPMI_w-2_s-1 \
       --dim 1000
echo "finished save joint matrice."

mv model/ ../../cache/sppmi-model/
echo "finished all."
