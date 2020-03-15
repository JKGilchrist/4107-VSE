from pre_processing import main as pre_processing_main
from dictionary_builder import main as dictionary_main
from index_builder import main as index_main
from generate_td_idf import generate_td_idf
from create_weighted_ed_df import create_weighted_ed_df

import os

if __name__ == "__main__":
    
    #All the initially required files, in order
    if not os.path.exists("save_files/UO/corpus.csv"): 
        pre_processing_main()
    if not os.path.exists("save_files/UO/description_dic.obj"): 
        dictionary_main()
    if not os.path.exists("save_files/UO/description_index.csv"): 
        index_main()
    if not os.path.exists("save_files/UO/description_index_with_weight.csv"):
        generate_td_idf()
    if not os.path.exists("save_files/UO/weighted_ed_df.pkl"):
        create_weighted_ed_df()
