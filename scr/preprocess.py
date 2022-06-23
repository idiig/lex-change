import pandas as pd
import json

INPUT = "../data/hachidai.db"
INDEX = "../data/id2lemma.json"
# INV_INDEX_PATH = "../data/lemma2id.json"
OUTPUT = "../data/parsed_hd.csv"

# read data
hd = pd.read_table(INPUT,
                   usecols=range(9),
                   sep=" ",
                   names=[
                       "id", "token_type", "bg_id", "chasen_id", "surface",
                       "lemma", "lemma_reading", "kanji", "kanji_reading"
                   ])

# reform data
hd = hd.assign(anthology_id=hd["id"].map(lambda x: x.split(":")[0]))
hd = hd.assign(poem_id=hd["id"].map(lambda x: x.split(":")[1]))
hd["anthology_poem_id"] = hd.anthology_id + ":" + hd.poem_id
hd = hd.assign(token_id=hd["id"].map(lambda x: x.split(":")[2]))
hd = hd.assign(general_id=hd["bg_id"].map(lambda x: x.split("-")[0]))
hd = hd.assign(pos_id=hd["bg_id"].map(lambda x: x.split("-")[1]))
hd = hd.assign(group_id=hd["bg_id"].map(lambda x: x.split("-")[2]))
hd = hd.assign(filed_id=hd["bg_id"].map(lambda x: x.split("-")[3]))
hd = hd.assign(exact_id=hd["bg_id"].map(lambda x: x.split("-")[4]))

# filter
hd = hd[hd.token_type.str.match("A00") |  # conventionized lexemes
        hd.token_type.str.match("B00") |  # compounds
        hd.token_type.str.match("D00")  # proper namen compounds
        ]

# obtain dictionary from metacode to lemma
id2lemma = {}
for bg_id in hd.bg_id.unique():
    id2lemma[bg_id] = (hd[hd.bg_id == bg_id]["lemma"].unique()[0],
                       hd[hd.bg_id == bg_id]["lemma_reading"].unique()[0])

with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(json.dumps(id2lemma))


def token2string(corpus, anthology_poem_id):
    t = corpus[corpus.anthology_poem_id.str.match(anthology_poem_id)]
    return t.bg_id, t.surface


poem_id_dic = {}
poem_sfc_dic = {}

for poem in hd.anthology_poem_id.unique():
    id_str, surface_str = token2string(hd, poem)
    poem_id_dic[poem] = ','.join(id_str)  # tokenized str
    poem_sfc_dic[poem] = ''.join(surface_str)  # surface str

# tokenized str
poem = pd.DataFrame(
    list(poem_id_dic.items()),
    columns=['id', 'source'],
)
poem = poem.sort_values(by='id', ignore_index=True)

# surface str
poem_sfc = pd.DataFrame(list(poem_sfc_dic.items()),
                        columns=['id', 'src_surface'])
poem_sfc = poem_sfc.sort_values(by='id', ignore_index=True)

# merge
parsed_poem = pd.merge(poem, poem_sfc)

# output
parsed_poem.to_csv(OUTPUT, index=False)
print("finished preprocess")
