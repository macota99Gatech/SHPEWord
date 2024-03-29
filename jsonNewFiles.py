import pandas as pd
from collections import defaultdict
import json

# reads the csv file and transform it into a json file / dictionary
def newFiles(name):
    data = pd.read_csv(name)
    dic = defaultdict(dict)

    for _,row in data.iterrows():
        for i in range(1,6):
            try:
                course = row["Course Name {0}".format(i)]
                major = row["Course Name {0}".format(i)].split()[0]
                document_type = row["Document Type {0}".format(i)]
                id = row["Document Upload {0}".format(i)].split("id=")[1]
                if course not in dic[major]:
                    dic[major][course] = {"Quizzes and Midterms": [], "Homework and Notes": [], "Other": []}
                if document_type == "Quizzes and Midterms":
                    dic[major][course]["Quizzes and Midterms"].append(id)
                elif document_type == "Homework and Notes":
                    dic[major][course]["Homework and Notes"].append(id)
                else:
                    dic[major][course]["Other"].append(id)
            except AttributeError:
                continue

    data = json.loads(json.dumps(dic))
    with open('newFiles.json', 'w') as f:
        json.dump(data, f, indent=2)
        return dic
