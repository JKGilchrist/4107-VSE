#Module 3

import pandas as pd
import string_formatting
import sys



def open_file():
    df = pd.read_csv("corpus.csv", sep = "|")

    return df

if __name__ == "__main__": 
    df = open_file()

    titles = []
    for x in df["title"]:
        titles.append(x)

    title_dic = set()
    for title in titles:
        tokens = string_formatting.get_formatted_tokens(title)
        title_dic.update(tokens)
    title_dic.remove('')
    print(title_dic)
    #TODO later
    if False:
        descriptions = []
        for x in df["description"]:
            descriptions.append(x)
    
    
        




