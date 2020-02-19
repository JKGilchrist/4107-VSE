# 4107-VSE
Vanilla Search Engine for CSI4107

## Set-up

Delete the files save_files/corpus.csv, save_files/description_dic.obj, save_files/title_dic.ob,
save_files/description_index.obj, save_files/title_index.obj, save_files/description_secondary_index.obj, save_files/title_secondary_index.obj if they exist

Then to regenerate them:
```
python main.py
``` 

To see the actual code used to generate them, see pre_processing.py, dictionary_builder.py, and index_builder.py 

To regenerate weighted_ed_df.pkl, description_index_with_weight.obj, and title_index_with_weight.obj:

```
python create_Weighted_ed_df.ipynb
python generate_td_idf.ipynb
```

## To Run

Install pandas, pickle, math, os, re, similarity, nltk, tkinter and numpy libraries. 

Or alternatively, run 
```
conda env create -f environment.yml
conda activate 4107-VSE
python view.py
```

To note: if nltk's stopwords aren't downloaded, one must manually go into string_formatting.py and uncomment line 9, which will download it. After its first execution, then it can be recommented. It is left commented as we assume you already have it downloaded.