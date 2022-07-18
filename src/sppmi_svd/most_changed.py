import argparse
import numpy as np
import logging
import json
from tqdm import tqdm

from util import load_pickle


def main(args):
    """Find top n most changed word."""
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    logging.info(f"[INFO] args: {args}")

    logging.info("[INFO] Loading id2word...")

    id2word, word2id = load_pickle(args.dic_id2word)
    V = len(id2word)
    for i in range(V, V + V):
        id2word[i] = '_' + id2word[i - V]
    for word in list(word2id.keys()):
        word2id['_' + word] = word2id[word] * 2 + 1

    logging.info("[INFO] Done.")
    logging.info("[INFO] Loading model...")

    M = np.load(args.path_model)
    M_before = M[:2055]
    M_after = M[2055:]
    assert len(M_after) == len(M_before)

    logging.info("[INFO] Done.")
    id2change = {}

    logging.info("[INFO] Calculating degree of semantic/usage change.")
    for i in tqdm(range(V)):
        a = M_before[i]
        b = M_after[i]
        id2change[id2word[i]] = np.linalg.norm(a - b)
    logging.info("[INFO] Done.")
    id2change = dict(sorted(id2change.items(), key=lambda item: item[1]))
    logging.info("[INFO] Writing output.")
    with open("id2change.txt", "w") as fp:
        fp.write(json.dumps(id2change))
    context_words = list(id2change.keys())[:args.top_n]
    with open("context_words.txt", "w") as fp:
        for word in context_words:
            fp.write(f"{word}\n")
    logging.info("[INFO] Done.")
    logging.info("[INFO] Finished all.")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--dic_id2word", help="path of id2word dict")
    parser.add_argument("-m", "--path_model", help="path of model/matrix file")
    parser.add_argument("-n",
                        "--top_n",
                        type=int,
                        help="top n most changed words")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
