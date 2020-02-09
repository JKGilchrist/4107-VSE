#Helper for module 3 and ... 9?

#modified from csi4106 notebook 5:
import nltk
nltk.download('stopwords') #can be commented out after first run
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#end

import re

def rm_numbers(tokens):
    good_tokens = []
    for token in tokens:
        if not str.isdigit(token) and not str.isdigit(token[:-1]): #some course numbers have a letter at the end
            good_tokens.append(token)
    return good_tokens


def rm_stopwords(tokens):
    good_tokens = []
    for token in tokens:
        if not (token in stopwords.words('english')):
            good_tokens.append(token)
    return good_tokens

def stemmer(tokens): #also case-folds
    ### modified from csi4106 notebook 5 
    return [PorterStemmer().stem(t) for t in tokens]
    ###end

#main fucntion
def get_formatted_tokens(str1, remove_full_stops = 1, remove_hyphens = 1, remove_commas = 1, remove_colons = 1, remove_units = 1, remove_stopwords = 1, remove_numbers = 1, stem = 1):
    str1 = str1.strip()
    if remove_hyphens:
        str1 = str1.replace("-", " ")     
    if remove_full_stops:
        str1 = str1.replace(".", "")
    if remove_commas:
        str1 = str1.replace(",", "")
    if remove_colons:
        str1 = str1.replace(":", "")
    
    if remove_units:
        str1 = re.sub(r" \(.+ unit.?\)", "", str1)
    #print(str1)
    tokens = str1.split(" ")
    
    if remove_stopwords:
        tokens = rm_stopwords(tokens)
    if remove_numbers:
        tokens = rm_numbers(tokens)
    if stem:
        tokens = stemmer(tokens)
        
    return tokens
