# -*- coding: utf-8 -*-
"""
Detect context words: method a.

Use algorithm proposed by
    https://github.com/a1da4/pmi-semantic-difference/tree/main/models/pmi-svd
"""

import pandas as pd
import subprocess
import json

CORPUS = "../data/parsed_hd.csv"
PERIOD = "shui"

periods = {
    'kokin': '01',
    'gosen': '02',
    'shui': '03',
    'goshui': '04',
    'kinyo': '05',
    'shika': '06',
    'sensai': '07',
    'shinkokin': '08'
}

hd = pd.read_csv(CORPUS)
period_id = int(periods[PERIOD])


def split_corpus(period=period_id, corpus=hd):
    '''return corpus A and corpus B.

    :param period: pseudo shift point: str
    :param corpus: whole corpus: pandas dataframe
    :return: splited sub corpus
    '''
    assert type(period) == int
    assert type(corpus) == pd.core.frame.DataFrame
    sub_corpus_a = corpus[corpus.id.str.split(':').map(
        lambda x: int(x[0]) <= period)]
    sub_corpus_b = corpus[corpus.id.str.split(':').map(
        lambda x: int(x[0]) > period)]
    with open('../cache/before.txt',
              mode='wt') as out_f_a,\
        open('../cache/after.txt',
             mode='wt') as out_f_b:
        for line in sub_corpus_a['source'].str.split(',').tolist():
            out_f_a.write(' '.join(line) + '\n')
        for line in sub_corpus_b['source'].str.split(',').tolist():
            out_f_b.write(' '.join(line) + '\n')
    return sub_corpus_a, sub_corpus_b


sub_corpus_a, sub_corpus_b = split_corpus(period=period_id, corpus=hd)

p = subprocess.Popen("cd sppmi_svd; sh train.py",
                     shell=True,
                     universal_newlines=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

# for line in p.stdout:
#     print()
