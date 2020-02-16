#Helper for module 3 and ... 9??

import settings

#modified from csi4106 notebook 5:
import nltk
#nltk.download('stopwords') #can be commented out after first run
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#end

import re

def rm_stopwords(tokens):
    good_tokens = []
    for token in tokens:
        if not (token in stopwords.words('english')):
            good_tokens.append(token)
    return good_tokens

def stemmer(tokens): #sometimes case-folds??
    ### modified from csi4106 notebook 5 
    return [PorterStemmer().stem(t) for t in tokens]
    ###end

def lower(tokens):
    good = []
    for token in tokens:
        if str.isalpha(token):
            good.append(token.lower())
        else:
            good.append(token)
    return good

#main function
def get_formatted_tokens(str1):

    remove_units = settings.remove_units
    fully_normalize = settings.fully_normalize
    normalize = settings.normalize
    remove_stopwords = settings.remove_stopwords
    fully_lower = settings.fully_lower
    stem = settings.stem


    if type(str1) == float:
        return []
    
    #remove accents - only changes words: québec, bézout, naïve
    str1 = str1.replace("é", "e")
    str1 = str1.replace("ï", "i")

    if remove_units:
        str1 = re.sub(r" \(.+ unit.?\)", "", str1)

    if fully_normalize: #Except for C++ we want to keep that
        if "C++" in str1:
            str1 = re.sub(r"\W", " ", str1) #replace all non letters and numbers with white space
            str1 = re.sub(r"\sC\s", " C++ ", str1) #restore C++
        else:
            str1 = re.sub(r"\W", " ", str1) #replace all non letters and numbers with white space
    elif normalize:
        str1 = str1.replace("-", " ")     
        str1 = str1.replace(".", "")
    
    #str1 = str(str1).strip()
    tokens = str1.split()
    if remove_stopwords:
        tokens = rm_stopwords(tokens)
    if fully_lower:
        tokens = lower(tokens)
    if stem:
        tokens = stemmer(tokens)
        
    return tokens
