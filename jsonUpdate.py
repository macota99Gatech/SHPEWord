from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json

# updates the json file with the new ids of each folder
def getCourses(idSHPE_Folder, drive):
    print("\nProcess started\n")
    ToDo = {}
    alias = {}
    fileChild = drive.ListFile(
        {'q': "'%s' in parents and trashed=false" % (idSHPE_Folder)}).GetList()

    for file in fileChild:
        temp = {}
        title = file['title']
        courseTitle = title.split()[0]
        code = title[1:len(courseTitle) - 1]
        alias[code] = [title, file['id']]

        coursesInFile = drive.ListFile({'q': "'%s' in parents and trashed=false" % (file['id'])}).GetList()
        for courses in coursesInFile:
            newDict = {}
            newDict['id'] = courses['id']
            # this for now
            docTypes = drive.ListFile({'q': "'%s' in parents and trashed=false" % (courses['id'])}).GetList()
            for doc in docTypes:
                if doc['title'] == 'Homework and Notes':
                    newDict['Homework and Notes'] = doc['id']
                elif doc['title'] == 'Other':
                    newDict['Other'] = doc['id']
                elif doc['title'] == 'Quizzes and Midterms':
                    newDict['Quizzes and Midterms'] = doc['id']
            temp[courses['title']] = newDict

        ToDo[code] = temp
        # go inside the folder and get all the courses numbers
    return ToDo, alias


def courseRefresh(self):
    id_FolderSHPE = self.getMainFolder(self.drive)
    courses, codes = self.getCourses(id_FolderSHPE, self.drive)
    data = json.loads(json.dumps(courses))
    dataCode = json.loads(json.dumps(codes))

    with open('courses.json', 'w') as f:
        json.dump(data, f, indent=2)

    with open('codes.json', 'w') as f:
        json.dump(dataCode, f, indent=2)

    print("Courses Updated")

