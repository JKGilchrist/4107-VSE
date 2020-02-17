#Module 3

import pandas as pd
import string_formatting
import sys
import pickle

def get_list_from_df(df, field):
    '''
    Returns a list containing df[field]
    '''
    lst = []
    for x in df[field]:
        lst.append(x)
    return lst

def build_dic(lst, save_name):
    '''
    Generates a set of unique, formatted terms from the given list and saves it
    '''

    dic = set() #uses a set to avoid duplicates
    for elem in lst:
        tokens = string_formatting.get_formatted_tokens(elem)
        dic.update(tokens)
        
    with open("save_files/{name}.obj".format(name = save_name), "wb"  ) as f:
        pickle.dump(dic, f )

def main():
    '''
    The main function, that generates both dictionaries
    '''
    df = pd.read_csv("save_files/corpus.csv", sep = "|")
    
    build_dic(get_list_from_df(df, "title"), "title_dic")
    build_dic(get_list_from_df(df, "description"), "description_dic")
