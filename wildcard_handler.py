#maintain a second inverted index from bigrams to dictionary terms that match each bigram


def create_bigrams(string):

    lst = ["$" + string[0], string[len(string) - 1] + "$"]

    i = 0
    while i < len(string) - 1:
        if string[i] != "*" and string[i+1] != "*":
            lst.append(string[i] + string[i+1])
        i += 1
    
    print(lst)

if __name__ == "__main__":
    create_bigrams("abc*def")