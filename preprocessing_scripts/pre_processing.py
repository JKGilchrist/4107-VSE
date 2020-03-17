#Module 2


#All unique reuters tages
#{'acq', 'zinc', 'dlr', 'peseta', 'cotton-oil', 'money-fx', 'heat', 'linseed', 'nat-gas', 'cpi', 'f-cattle', 'reserves', 'barley', 'naphtha', 'hog', 'lin-oil', 'corn-oil', 'housing', 'grain', 'gold', 'bop', 'coconut-oil', 'lei', 'sorghum', 'yen', 'groundnut', 'corn', 'oilseed', 'austdlr', 'income', 'sunseed', 'jobs', 'copper', 'palm-oil', 'gas', 'dmk', 'lin-meal', 'cornglutenfeed', 'potato', 'groundnut-oil', 'strategic-metal', 'wpi', 'rand', 'money-supply', 'l-cattle', 'coffee', 'cpu', 'hk', 'castor-oil', 'jet', 'ship', 'fishmeal', 'platinum', 'soybean', 'instal-debt', 'veg-oil', 'livestock', 'lead', 'soy-oil', 'can', 'rye', 'ipi', 'palmkernel', 'retail', 'tea', 'lumber', 'soy-meal', 'pork-belly', 'iron-steel', 'gnp', 'tin', 'dfl', 'alum', 'rice', 'sun-oil', 'stg', 'sfr', 'nzdlr', 'interest', 'inventories', 'plywood', 'sugar', 'nickel', 'crude', 'sun-meal', 'rapeseed', 'earn', 'carcass', 'rubber', 'silver', 'rape-oil', 'cruzado', 'meal-feed', 'wheat', 'orange', 'wool', 'cotton', 'fuel', 'oat', 'palladium', 'propane', 'trade', 'pet-chem', 'cocoa'}

# Convert a collection of documents into a formatted corpus

import os
import sys
import pandas as pd
import re 


#Uottawa bits
def munge_UO(path):
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
                        count = line.count("/")
                        num = 0
                        start = 0
                        while num + 1 != count // 2 + 1:
                            start = line.find("/", start) + 1
                            num +=1
                        if start != 0:
                            start -=1
                        index = line.find("/", start)
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


def create_UO_corpus(name):
    '''
    Creates the dataframe and saves it as a csv, using the given name as the file name
    '''

    path = "./raw_files/UofO_Courses.html"
    
    titles = []
    descriptions = []

    titles, descriptions = munge_UO(path)
        
    ids = list(range(0, len(titles)))

    df = pd.DataFrame(list(zip(ids, titles, descriptions)), columns = ["id", "title", "description"])

    df.to_csv(name, sep = "|", index = False) #Uses | as separator as it's a character not contained within the corpus itself.


#reuters bits
def munge_Reuters(path):
    ids = []
    titles = []
    descriptions = []
    topics = []
    id_start = 0
    with open(path, 'r') as f: 
        line = f.readline()

        while line:
            all_text = line

            if line.startswith("<REUT"):
                id = id_start
                id_start += 1

                title = "No title found"
                description = "No description found"
                topic = []
                while not line.startswith("</REUT"):
                    
                    if "<TOPICS" in line:
                        line = line.replace("<TOPICS>", "")
                        line = line.replace("</TOPICS>", "")
                        line = line.replace("<D>", "")
                        
                        topic = line.split("</D>")[:-1]

                    if "<TITLE" in line:
                        line = re.sub(r'\**<TITLE>', "", line)
                        #line = line.replace("<TITLE>", "")
                        line = line.replace("</TITLE>", "")    
                
                        line = line.replace("&lt;", "<")
                        line = line.strip()
                        if len(line) < 5:
                            print(line)
                        title = line

                    if "<DATELINE" in line:
                        
                        text = ""
                        while line.strip().lower() != "reuter":
                            text += (line)
                            line = f.readline()
                            all_text += line

                        text = text.replace("<DATELINE>", "")
                        text = text.replace("</DATELINE>", "\n")
                        text = text.replace("<BODY>", "")
                        text = text.replace("&lt;", "<")
                        text = text.strip()
                        text = text.replace("\n", " ")
                        text = text.replace("    ", "\\n")
                        text = text.replace('"', "'")
                        description = text
                    
                    line = f.readline()
                    all_text += line
                

                titles.append(title)
                descriptions.append(description)
                topics.append(topic)
                ids.append(id)

            line = f.readline()

    return titles, descriptions, topics


def create_Reuters_corpus(name):
    '''
    Creates the dataframe and saves it as a csv, using the given name as the file name
    '''
    path = "./raw_files/reuters21578.tar"
    
    titles, descriptions, topics = munge_Reuters(path)
    
    ids = list(range(0, len(titles)))

    df = pd.DataFrame(list(zip(ids, titles, descriptions, topics)), columns = ["id", "title", "description", "topics"])

    df.to_csv(name, sep = "|", index = False) #Uses | as separator as it's a character not contained within the corpus itself.


def main():
    '''
    The main function, that runs its all
    '''
    print("\nMaking both corpuses.")
    create_UO_corpus("save_files/UO/corpus.csv")
    create_Reuters_corpus("./save_files/Reuters/corpus.csv")
    print("Corpuses complete.")

if __name__ == "__main__":
    main()