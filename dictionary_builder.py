#Module 3

import pandas as pd
import string_formatting
import sys
import pickle

def open_file():
    df = pd.read_csv("save_files/corpus.csv", sep = "|")

    return df

def save(set1, name):
    with open("save_files/{name}.obj".format(name = name), "wb"  ) as f:
        pickle.dump(set1, f )

#TODO should take args for formatting
def build_dic(field, save_name):
    df = open_file()

    lst = []
    for x in df[field]:
        lst.append(x)

    dic = set()
    for elem in lst:
        tokens = string_formatting.get_formatted_tokens(elem)
        dic.update(tokens)
    
    save(dic, save_name)

def main():
    build_dic("title", "title_dic")
    build_dic("description", "description_dic")


if __name__ == "__main__": 

    main()