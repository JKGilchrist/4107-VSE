# Convert a collection of documents into a formatted corpus

import os

if __name__ == "__main__": 
    
    path = "raw_files/"
    
    files = os.listdir(path)
    
    for a_file in files:
        print(a_file)
