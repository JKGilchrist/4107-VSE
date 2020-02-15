
import string_formatting

def breakdown(string):
    if "(" in string:
        string = string.replace("(", " ( ")
    if ")" in string:
        string = string.replace(")", " ) ")
    
    lst = string.split()
    #print(lst)
    print (grouper(lst))


def lookup(string):
    string = string_formatting.get_formatted_tokens(string)
    #calls corpus access
    print(string)
    return string
    
def union(LHS, RHS):
    return list( set(LHS) | set(RHS) )
    
def intersection(LHS, RHS):
    return [i for i in LHS if i in  RHS]
    

def exception(LHS, RHS):
    return [i for i in LHS if i not in  RHS]
    

def grouper(lst):
    print("lst:", lst)
    if len(lst) == 1:
        return lookup(lst[0])
        #get values
    else:
        flip = False

        for i in range(len(lst)):
            if lst[i] == "AND" or lst[i] == "OR" or lst[i] == "AND_NOT":
                
                before_start = lst[:i].count("(")
                before_end = lst[:i].count(")")
                after_start = lst[i:].count("(")
                after_end = lst[i:].count(")")

                if before_start == before_end and after_start == after_end: # found the middle
                    LHS = []
                    RHS =  []                    
                    if i == 1: #either a single element by itself
                        LHS = grouper(lst[:i])
                    else: #or wrapped in ()
                        LHS = grouper(lst[1:i- 1])
                        
                    if i+2 == len(lst):
                        RHS = grouper(lst[i+1:])
                    else:
                        RHS = grouper(lst[i+2 : len(lst) - 1])
                    print("ON", LHS,lst[i],  RHS)
                    
                    if lst[i] == "OR":
                        x = union(LHS, RHS)
                        return x
                    elif lst[i] == "AND":
                        x = intersection(LHS, RHS)
                        return x
                    else:
                        x = exception(LHS, RHS)
                        return x
                    
                    #merge them

            elif i == len(lst) - 1: #couldnt find middle, due to extra parentheses around entire query
                flip = True

        if flip:
            return grouper(lst[1:len(lst) - 1])



if __name__ == "__main__":
    breakdown("operating AND system")
    print("\n\n\n")
    #breakdown("(B OR C) AND_NOT (A OR C)")
    #print("\n\n\n")
    #breakdown("((x AND (x OR y)) OR (c AND d))")