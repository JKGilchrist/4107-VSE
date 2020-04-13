import pickle
from string_formatting import get_formatted_tokens, get_bigram_tokens

def complete(first_word, model_path):
    '''
    Returns a list of up to 5 words to recommend as the following word based on the given first_word
    '''
    with open(model_path, 'rb') as f: #open file
        blm_dict = pickle.load(f)

    word = get_formatted_tokens(first_word)
    print(word)
    if word == []:
        word = get_bigram_tokens(first_word)
    
    word = word[0]
    
    try :
        return blm_dict[word]
    except:
        return []

def main():
    print (complete("elementary", "./save_files/UO/blm_dic.pkl"))

if __name__ == "__main__":
    main()


