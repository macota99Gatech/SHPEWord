import pandas as pd
from collections import defaultdict
import numpy as np
import json

def newFiles(name):
    data = pd.read_csv(name)
    dic = defaultdict(dict)

    for _,row in data.iterrows():
        for i in range(5):
            try:
                course = row[i]
                major = row[0].split()[0]
                dType = row[i+10]
                id = row[i + 15].split("=")[1]
                prof = row[i+5]
                if course not in dic[major]:
                    dic[major][course] = {"Quizzes and Midterms": [], "Homework and Notes": [], "Other": []}
                if dType == "Tests and Quizzes":
                    dic[row[0].split()[0]][row[i]]["Quizzes and Midterms"].append((id, prof))
                elif dType == "Homework and Notes":
                    dic[row[0].split()[0]][row[i]]["Homework and Notes"].append((id, prof))
                else:
                    dic[row[0].split()[0]][row[i]]["Other"].append((id, prof))
            except AttributeError:
                continue
                # do break for everything or just the row?

    data = json.loads(json.dumps(dic))
    with open('newFiles.json', 'w') as f:
        json.dump(data, f, indent=2)
        return dic
