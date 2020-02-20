#Helper function(s)
#The main function for external files is get_formatted_tokens, the rest just help that one perform
#It uses settings.py to indicate whether various modifications should occur

import settings

#modified from csi4106 notebook 5:
import nltk
#nltk.download('stopwords') #can be commented out after first run
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#end

import re

def rm_stopwords(tokens):
    '''
    Returns a list of the elements from the given list that aren't an english stopword
    '''
    good_tokens = []
    for token in tokens:
        if not (token in stopwords.words('english')):
            good_tokens.append(token)
    return good_tokens

def stemmer(tokens): #sometimes case-folds
    '''
    Returns a list of stemmed elements based off the given list
    '''
    ### modified from csi4106 notebook 5 
    return [PorterStemmer().stem(t) for t in tokens]
    ###end

def lower(tokens):
    '''
    Returns a list of strings without any capital letters
    '''
    good = []
    for token in tokens:
        if str.isalpha(token):
            good.append(token.lower())
        else:
            good.append(token)
    return good

#main function
def get_formatted_tokens(string):
    '''
    Returns a list of tokens, formatted based on the settings in settings.py, of the given string
    '''
    remove_units = settings.remove_units
    fully_normalize = settings.fully_normalize
    normalize = settings.normalize
    remove_stopwords = settings.remove_stopwords
    fully_lower = settings.fully_lower
    stem = settings.stem

    if type(string) == float:
        return []
    
    #remove accents - only changes words: québec, bézout, naïve. It adds unnecessary complexity. The stemmer performs the same in either case
    string = string.replace("é", "e")
    string = string.replace("ï", "i")

    if remove_units: #very useless for searching on
        string = re.sub(r" \(.+ unit.?\)", "", string)

    if fully_normalize: #Except for C++ we want to keep that
        if "C++" in string:
            string = re.sub(r"\W", " ", string) #replace all non letters and numbers with white space
            string = re.sub(r"\sC\s", " C++ ", string) #restore C++
        else:
            string = re.sub(r"\W", " ", string) #replace all non letters and numbers with white space
    elif normalize:
        string = string.replace("-", " ")     
        string = string.replace(".", "")
    
    tokens = string.split()
    if remove_stopwords:
        tokens = rm_stopwords(tokens)
    if fully_lower:
        tokens = lower(tokens)
    if stem:
        tokens = stemmer(tokens)
        
    return tokens


if __name__ == "__main__":
    print(get_formatted_tokens("international e-business strategies"))
    print(get_formatted_tokens("computer"))