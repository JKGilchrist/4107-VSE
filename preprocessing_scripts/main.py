from .pre_processing import main as pre_processing_main
from .dictionary_builder import main as dictionary_main
from .index_builder import main as index_main
from .generate_td_idf import generate_td_idf
from .create_weighted_ed_df import create_weighted_ed_df

import os

def main():
    '''
    Runs all necessary preprocessing scripts, as needed and in order.
    '''

    if not os.path.exists("./save_files/UO/corpus.csv") or not os.path.exists("./save_files/Reuters/corpus.csv"): 
        print("Missing a corpus. Generating now.")
        pre_processing_main()
    if not os.path.exists("./save_files/UO/descriptions_dic.obj") or not os.path.exists("./save_files/Reuters/descriptions_dic.obj"): 
        print("Missing a dictionary. Generating now.")
        dictionary_main()
    if not os.path.exists("./save_files/UO/descriptions_index.obj") or not os.path.exists("./save_files/Reuters/descriptions_index.obj"): 
        print("Missing an index. Generating now.")
        index_main()
    if not os.path.exists("./save_files/UO/descriptions_index_with_weight.csv"): #or not os.path.exists("./save_files/Reuters/corpus.csv"): 
        generate_td_idf()
    if not os.path.exists("./save_files/UO/weighted_ed_df.pkl"): #or not os.path.exists("./save_files/Reuters/corpus.csv"): 
        create_weighted_ed_df()
    
    print("All pre-processing has been prepared.")

