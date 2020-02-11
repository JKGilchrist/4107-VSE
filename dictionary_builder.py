#Module 3

import pandas as pd
import string_formatting
import sys
import pickle

def open_file():
    df = pd.read_csv("save_files/corpus.csv", sep = "|")

    return df

def save(set1, name):
    pickle.dump(set1, open("save_files/{name}.obj".format(name = name), "wb"  ) )
    
    
if __name__ == "__main__": 
    df = open_file()

    titles = []
    for x in df["title"]:
        titles.append(x)

    title_dic = set()
    for title in titles:
        tokens = string_formatting.get_formatted_tokens(title)
        title_dic.update(tokens)
    
    save(title_dic, "title_dic")

    descriptions = []
    for x in df["description"]:
        descriptions.append(x)

    description_dic = set()
    for description in descriptions:
        tokens = string_formatting.get_formatted_tokens(description)
        description_dic.update(tokens)

    save(description_dic, "description_dic")


