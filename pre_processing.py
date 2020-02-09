# Convert a collection of documents into a formatted corpus

import os
import pandas as pd
import re

def read_and_munge_file(path):
    '''
    Returns list of titles, descriptions from given file. Highly personalized, so not very re-usable.
    '''
    titles = []
    descriptions = []

    with open(path, 'r') as f: #open file

        line = f.readline()

        while line:
            if "courseblocktitle noindent" in line:
                line = line[45:-14] #remove excess html

                if "Ã" in line:
                    line = french_formatting(line)

                titles.append(line)

                line = f.readline()
                if "courseblockdesc noindent" in line: #Not all courses have descriptions.
                    line = f.readline()
                    
                    line = line.split("</p>")[0].strip()

                    if "Ã" in line:
                        line = french_formatting(line)
                    
                    if ("href" in line):
                        line = remove_link(line)

                    descriptions.append(line)
                
                else: #course doesn't have a description. Filler used instead.
                    descriptions.append("NA")
                
                line = f.readline()
                
            else: #skip line
                line = f.readline()

    return titles, descriptions

def french_formatting(str1):
    '''
    Corrects strings for french accents
    '''
    
    str1 = re.sub('Ã€', "À", str1)
    str1 = re.sub('Ã¢', "â", str1)
    str1 = re.sub(r"Ã\s", "à", str1)
    
    str1 = re.sub('Ã§', "ç", str1)

    str1 = re.sub("Ã‰", "É", str1)
    str1 = re.sub('Ã¨', "è", str1)
    str1 = re.sub('Ã©', "é", str1)
    str1 = re.sub('Ãª', "ê", str1)

    str1 = re.sub('Ã®', "î", str1)
    str1 = re.sub('Ã¯', "ï", str1)
    
    str1 = re.sub('Ã´', "ô", str1)

    str1 = re.sub('Ã¹', "ù", str1)
    str1 = re.sub('Ã»', "û", str1)
    
    return str1

def remove_link(str1):
    '''
    Removes html hyperlink metadata left in strings, returning the plain text
    '''
    str2 = re.sub(r'<a href="/search/\?P=\w{3}%\d{6}" title="\w{3} \d{4}" class="bubblelink code" onclick="return showCourse\(this, \'\w{3} \d{4}\'\);">', "", str1)
    str2 = re.sub("</a>", "", str2)
    return str2

def create_columns():
    
    path = "raw_files/"
    
    files = os.listdir(path)
    
    titles = []
    descriptions = []

    for a_file in files: #In case it becomes a series of files later.
        
        titles, descriptions = read_and_munge_file(path + a_file)
    

    ids = list(range(0, len(titles)))
    return ids, titles, descriptions



def create_xml_corpus(path):
    
    ids, titles, descriptions = create_columns()

    text = '<?xml version="1.0" encoding="UTF-8"?>\n'

    for id, title, description in zip(ids, titles, descriptions):
        text = text + "<course>\n"  + "\t<id>" + str(id) + "</id>\n"   + "\t<title>" + title + "</title>\n" + "\t<description>" + description + "</description>\n" + "</course>\n"
    
    with open(path, 'w') as f: #open file
        f.write(text)

def create_csv_corpus(name):

    ids, titles, descriptions = create_columns()

    df = pd.DataFrame(list(zip(ids, titles, descriptions)), columns = ["id", "title", "description"])

    df.to_csv(name, sep = "|", index = False) #Uses | as separator as it's a character not contained within the corpus itself.
    



if __name__ == "__main__": 
    

    if not os.path.exists("corpus.csv") :
        create_csv_corpus("corpus.csv")
    
    if not os.path.exists("corpus.xml"): #Whichever is easier.
        create_xml_corpus("corpus.xml")