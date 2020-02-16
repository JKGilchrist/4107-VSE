#Module 2

# Convert a collection of documents into a formatted corpus

import os
import sys
import pandas as pd
import re 

def read_and_munge_file(path):
    '''
    Returns list of titles, descriptions from given file. Highly personalized, so not very re-usable.
    '''
    titles = []
    descriptions = []

    with open(path, 'r', encoding="utf8") as f: 

        line = f.readline()

        while line:
            if "courseblocktitle noindent" in line:
                line = line[45:-14] #remove excess html

                if int(line[5]) >= 5 and int(line[5]) != 9: #french, toss
                    continue

                #removes french parts of bilingual courses
                if "/" in line:
                    new_line = line.split("/")
                    if len(new_line) == 2 and len(new_line[1]) < 10:
                        new_line = new_line[0].split("(")[0] + "(" + new_line[1][1:]
                    elif len(new_line) == 2:
                        new_line = new_line[0][:9] + new_line[1]
                    else:
                        if line.count("(") == 1:
                            new_line = new_line[0][:8] + new_line[1].split("(")[0] + "(" + new_line[2][1:]
                        else:
                            new_line = new_line[0][:8] + new_line[1][:-11] + "(" + new_line[2][1:]
                    
                    line = new_line

                titles.append(line)

                line = f.readline()
                if "courseblockdesc noindent" in line: #Not all courses have descriptions.
                    line = f.readline()
                    
                    line = line.split("</p>")[0].strip()
                    
                    if ("href" in line):
                        line = remove_link(line)

                    if "/" in line and ("é" in line or "à" in line or "è" in line): #Handling bilingual courses
                        index = line.find("/")
                        line = line[index+2:]
                        #print(line)
                    
                    descriptions.append(line)
                
                else: #course doesn't have a description. Filler used instead.
                    descriptions.append("NA")
                
                line = f.readline()
                
            else: #skip line
                line = f.readline()

    return titles, descriptions

def remove_link(str1):
    '''
    Removes html hyperlink metadata left in strings, returning the plain text
    '''
    str2 = re.sub(r'<a href="/search/\?P=\w{3}%\d{6}" title="\w{3} \d{4}" class="bubblelink code" onclick="return showCourse\(this, \'\w{3} \d{4}\'\);">', "", str1)
    str2 = re.sub("</a>", "", str2)
    return str2

def create_columns():
    '''
    In anticipation of later expansion and more files, uses the directory to access all the raw files that should be converted into a corpus. 
    '''
    
    path = "raw_files/"
    
    files = os.listdir(path)
    
    titles = []
    descriptions = []

    for a_file in files: #In case it becomes a series of files later.
        
        titles, descriptions = read_and_munge_file(path + a_file)
    

    ids = list(range(0, len(titles)))
    return ids, titles, descriptions

def create_csv_corpus(name):
    ids, titles, descriptions = create_columns()

    df = pd.DataFrame(list(zip(ids, titles, descriptions)), columns = ["id", "title", "description"])

    df.to_csv(name, sep = "|", index = False) #Uses | as separator as it's a character not contained within the corpus itself.

def main():
    create_csv_corpus("save_files/corpus.csv")
    

if __name__ == "__main__":
    main()