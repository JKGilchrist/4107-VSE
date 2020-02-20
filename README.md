# 4107-VSE
Vanilla Search Engine for CSI4107 by Group #1
Jess Gilchrist
Beatrice Johnston

## Set-up

To generate all of the required prerequisite files, run 

```
python main.py
``` 

To see the actual code used to generate them, see pre_processing.py, dictionary_builder.py, index_builder.py, generate_td_idf.py, and create_weighted_ed_df.py


## To Run
Install pandas, pickle, math, os, re, similarity, nltk, tkinter and numpy libraries. 

Or alternatively, run 
```
conda env create -f environment.yml
conda activate 4107-VSE
```

Then run
```
python view.py
```

To note: if nltk's stopwords aren't downloaded, one must manually go into string_formatting.py and uncomment line 9, which will download it. After its first execution, then it can be recommented. It is left commented as we assume you already have it downloaded.