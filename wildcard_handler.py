
def get_bigrams(string):
    '''
    Returns a list of bigrams from the given string
    '''
    lst = []

    i = 0
    while i < len(string) - 1:

        if i == 0 and string[i] != "*":
            lst.append("$" + string[0])

        if string[i] != "*" and string[i+1] != "*":
            lst.append(string[i] + string[i+1])
        i += 1

        if i == len(string) - 1 and string[i] != "*":
            lst.append(string[len(string) - 1] + "$")

    return lst
