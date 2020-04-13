'''
Module to take a corpus and creare a bigram language model, to be used by the query completion model

min threshold on the conditioning word frequency
remove stop words? stemming?

since it is directly user-facing we want to to speak in "user terms" hence, it lemmatizes but does not stem to allow for greater frequencies without changing words as much as stemming does
'''
import pandas as pd
import pickle
from string_formatting import get_bigram_tokens, get_formatted_tokens

'''
Output is a dictionary of stemmed words and their associated list of 5 most popular lemmatized words that follow them
e.g.
{
    "elementari": ["function", "probability"]
}

'''

def create_blm(df, save_path):
    blm = blm_generator(df)
    #print(blm)
    with open(save_path + "blm_dic.obj", "wb" ) as f:
        pickle.dump(blm, f )

def blm_generator(df):
    
    #Create a list of lists of tokens(strings), each representing the tokens of a sentence, to be used to create the BLM
    clean_sentences = [] 
    count = 0
    for _, row in df.iterrows():
        print("\r\tGathering sentences: " + str(round(count / len(df), 2) * 100).split(".")[0] + "%" , end = "")
        count += 1
        #Since you can't indicate whether you're searching on titles or descriptions, they're treated equally.
        title = get_bigram_tokens(row["title"])
        description = get_bigram_tokens(row["description"])
        if title != []:
            clean_sentences.append(title)
        if description != []:
            clean_sentences.append(description)
    print()
    
    #Create a set of all unique words, stemmed or lemmatized stop-words (so that all words can have a prediction)
    unique_words = set() 
    count = 0
    for x in clean_sentences:
        print("\r\tGathering unique words: " + str(round(count / len(clean_sentences), 2) * 100).split(".")[0] + "%" , end = "")
        count += 1
        for y in x:
            stemmed = get_formatted_tokens(y)
            if len(stemmed) != 0:
                stemmed = stemmed[0]
            else:
                stemmed = y
            unique_words.add(stemmed)
    print()
    
    #Time to generate the BLM
    blm = dict()
    for x in unique_words: #Fill it with empty lists
        blm[x] = []
    
    #Add every second word to the associated list of the first word
    count = 0
    for sentence in clean_sentences: 
        print("\r\tBuilding lists of bigram for each word: " + str(round(count / len(clean_sentences), 2) * 100).split(".")[0] + "%" , end = "")
        count += 1
        for i in range(len(sentence) - 1):
            first = get_formatted_tokens(sentence[i])
            if len(first) != 0:
                first = first[0]
            else:
                first = sentence[i]

            second = sentence[i+1]

            blm[first].append(second)
    print()
    
    #Using those lists of words, sort, count, and order so that the list of each dict entry only contains the 5 most popular distinct words from that list
    count = 0
    for x in unique_words:
        print("\r\tCleaning up lists: " + str(round(count / len(unique_words), 2) * 100).split(".")[0] + "%" , end = "")
        count += 1
        
        blm[x].sort()

        unique_words_in_x = set(blm[x])

        tuples = [] #list of tuples
        for word in unique_words_in_x:
            tuples.append((word, len([i for i in blm[x] if i == word])))
        
        #Sort words in descending order of counts
        tuples.sort(key = lambda count: count[1], reverse = True)
        #Assign the list
        blm[x] = [i[0] for i in tuples][:5]
    print()
    
    return blm
        

def main():
    '''
    The main function, that generates both blms
    '''
    print("\nMaking bigram language models.")
    print("Creating UOttawa bigram language model")
    df1 = pd.read_csv("./save_files/UO/corpus.csv", sep = "|") #remove first . when objectifying it
    create_blm(df1, "./save_files/UO/")
    
    print("\nCreating Reuters bigram language model")
    df2 = pd.read_csv("./save_files/Reuters/corpus.csv", sep = "|")
    create_blm(df2, "./save_files/Reuters/")
    
if __name__ == "__main__":
    main()
