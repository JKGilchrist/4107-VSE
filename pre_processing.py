# Convert a collection of documents into a formatted corpus

import os
import pandas as pd
import re

#to remove
from bs4 import BeautifulSoup

#WIP
def french_formatting(str1):
    #print("frecnh: ", str1)
    if "Ã‰" in str1:
        str1 = str1.replace("Ã‰", "É", -1)
    if 'Ã¨' in str1:
        str1 = str1.replace('Ã¨', 'è', -1)
    if 'Ã©' in str1:
        str1 = str1.replace('Ã©', 'é', -1)
    if 'Ã' in str1:
        str1 = str1.replace('Ã ', 'à', -1)
    
    x = False
    x = re.sub("  +", " ", str1)
    if x:
        print(str1)
        str1 = x
    return str1


def process_html(a_file):
    
    
    with open(a_file, 'r') as f: #open file

        soup = BeautifulSoup(f, 'html.parser')

        titles = soup.find_all("p", "courseblocktitle noindent")

        ps = soup.find_all("p", "courseblockdesc noindent")

        print(len(titles))
        print(len(ps))


if __name__ == "__main__": 
    
    path = "raw_files/"
    
    files = os.listdir(path)
    
    titles = []
    descriptions = []

    for a_file in files: #In case it becomes a series of files later.
        
        with open(path + a_file, 'r') as f: #open file

            line = f.readline()

            while line:
                if line.__contains__("courseblocktitle noindent"):
                    line = line[45:-14] #remove excess text

                    if "Ã" in line:
                        line = french_formatting(line)

                    titles.append(line)
                    line = f.readline()
                    if line.__contains__("courseblockdesc noindent"):
                        line = f.readline()
                        
                        line = line.split("</p>")[0].strip()
                        if "Ã" in line:
                            line = french_formatting(line)
                        
                        #still a WIP
                        #if ("href" in line):
                        #    print(line)
                        #print(line, "\n\n")
                        descriptions.append(line)
                    
                    else: #course doesn't have a description. Filler used instead.
                        descriptions.append("NA")
                    
                    line = f.readline()
                    
                else: #skip line
                    line = f.readline()

    if False:
            
        for x, y in zip(titles, descriptions):
            print (x)
            print (y)
            print("\n\n\n\n")

