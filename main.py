from pre_processing import main as pre_processing_main
from dictionary_builder import main as dictionary_main
from index_builder import main as index_main
from generate_td_idf import generate_td_idf

import os

if __name__ == "__main__":
    
    #All the initially required files, in order
    if not os.path.exists("save_files/corpus.csv"): 
        pre_processing_main()
    if not os.path.exists("save_files/description_dic.obj"): 
        dictionary_main()
    if not os.path.exists("save_files/description_index.csv"): 
        index_main()
    if not os.path.exists("save_files/description_index_with_weight.csv"):
        generate_td_idf()
