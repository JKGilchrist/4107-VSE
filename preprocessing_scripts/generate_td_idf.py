import pandas as pd
import pickle
import math
import numpy as np
from string_formatting import get_formatted_tokens

def generate_td_idf():
    infile = open("./save_files/UO/descriptions_index.obj", "rb")
    desc = pickle.load(infile)
    infile.close()
    infile = open("./save_files/UO/title_index.obj", "rb")
    title = pickle.load(infile)
    infile.close()
    corpus = pd.read_csv("save_files/UO/corpus.csv", sep="|")

    corpus['title'] = corpus['title'].apply(lambda x: get_formatted_tokens(x))
    corpus['description'] = corpus['description'].apply(lambda x: get_formatted_tokens(x))

    # Generate tf
    new = {}
    for k, v in title.items():
        v = list(v)
        for i in range(0, len(v)):
            lst = corpus.loc[v[i], 'title']
            v[i] = (v[i], lst.count(k))
        v = set(v)
        new.update({k: v})
    title = new

    new = {}
    for k, v in desc.items():
        v = list(v)
        for i in range(len(v)):
            lst = corpus.loc[v[i], 'description']
            v[i] = (v[i], lst.count(k))
        v = set(v)
        new.update({k: v})
    desc = new

    # Normalize using log(1+tf) where tf is the raw frequency
    new = {}
    for k, v in desc.items():
        v = list(v)
        for i in range(len(v)):
            v[i] = list(v[i])
            v[i][1] = math.log(1 + v[i][1])
            v[i] = tuple(v[i])
        v = set(v)
        new.update({k: v})
    desc = new

    new = {}
    for k, v in title.items():
        v = list(v)
        for i in range(len(v)):
            v[i] = list(v[i])
            v[i][1] = math.log(1 + v[i][1])
            v[i] = tuple(v[i])
        v = set(v)
        new.update({k: v})
    title = new

    #tf-idf
    new = {}
    for k, v in title.items():
        v = list(v)
        for i in range(len(v)):
            v[i] = list(v[i])
            v[i][1] = v[i][1] * math.log(624 / len(v))
            v[i] = tuple(v[i])
        v = set(v)
        new.update({k: v})
    title = new

    new = {}
    for k, v in desc.items():
        v = list(v)
        for i in range(len(v)):
            v[i] = list(v[i])
            v[i][1] = v[i][1] * math.log(624 / len(v))
            v[i] = tuple(v[i])
        v = set(v)
        new.update({k: v})
    desc = new

    pickle.dump(title, open("./save_files/UO/title_index_with_weight.obj", "wb"))
    pickle.dump(desc, open("./save_files/UO/descriptions_index_with_weight.obj", "wb"))
