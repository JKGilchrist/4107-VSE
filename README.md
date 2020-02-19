# 4107-VSE
Vanilla Search Engine for CSI4107

## Set-up

Delete the files save_files/corpus.csv, save_files/description_dic.obj, save_files/description_index.csv, save_files/title_dic.csv, save_files/title_index.csv.

Then to regenerate them:
```
python main.py
``` 

## To Run

Install pandas, pickle, math, os, re, similarity, nltk, tkinter and numpy libraries. 

Or alternatively, run 
```
conda env create -f environment.yml
conda activate 4107-VSE
python view.py
```

To note: if nltk's stopwords aren't downloaded, one must manually go into string_formatting.py and uncomment line 9, which will download it. After its first execution, then it can be recommented.