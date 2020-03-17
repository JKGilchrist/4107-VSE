#Module 3

import pandas as pd
from string_formatting import get_formatted_tokens
import sys
import pickle

def build_dicts(df, save_path):
    titles_dic = build_dic ( df, "title" )
    with open(save_path + "titles_dic.obj", "wb"  ) as f:
        pickle.dump(titles_dic, f )
        
    descriptions_dic = build_dic ( df, "description" )
    with open(save_path + "descriptions_dic.obj", "wb"  ) as f:
        pickle.dump(descriptions_dic, f )
        


def build_dic(df, field):
    '''
    Generates a set of unique, formatted terms from the given list and saves it
    '''
    #Make list of df[field]
    lst = []
    for x in df[field]:
        lst.append(x)

    count = 0
    dic = set() #uses a set to avoid duplicates
    for elem in lst:
        count += 1
        print("\r\t{}s: ".format(field) + str(round(count / len(df), 2) * 100).split(".")[0] + "%", end = "")
        tokens = get_formatted_tokens(elem)
        dic.update(tokens)
    print()
    return dic
        

def main():
    '''
    The main function, that generates both dictionaries
    '''
    print("\nMaking dictionaries.")
    print("Creating UOttawa dictionary")
    df1 = pd.read_csv("./save_files/UO/corpus.csv", sep = "|")
    build_dicts(df1, "./save_files/UO/")
    
    print("\nCreating Reuters dictionary")
    df2 = pd.read_csv("./save_files/Reuters/corpus.csv", sep = "|")
    build_dicts(df2, "./save_files/Reuters/")
    
if __name__ == "__main__":
    main()