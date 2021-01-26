from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import sys
import os
import jsonNewFiles
import json

class Uploader:

    def __init__(self, csvFile):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        self.newFiles = jsonNewFiles.newFiles(csvFile)
        # self.data = pd.read_csv(csvFile)
        # self.data = self.data.fillna('null')

        with open('courses.json') as f:
            self.todo = json.load(f)

    def initUpload(self):
        for m, courses in self.newFiles.items():
            self.major = m
            for c, typeFiles in courses.items():
                self.course = c
                for t, list in typeFiles.items():
                    self.docType = t
                    for i in list:
                        self.document = i[0]
                        self.prof = i[1]
                        print("major:" + self.major)
                        print("course:" + self.course)
                        print("docType:" + self.docType)
                        print("document:" + self.document)
                        print("prof:" + self.prof)
                        # self.insertFile()


                break
            break


    def getMainFolder(self):
        file_list = self.drive.ListFile({'q': "title = 'GT-SHPE Word Dev' and trashed=false"}).GetList()
        #this is a bit hardcoded
        file = file_list[2]
        return file['id']

    def getIdMajor(self):
        fileChild = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.idSHPE_Folder}).GetList()
        for file in fileChild:
            title = file['title']
            arr = title.split(')')
            fixed = arr[0][1:len(arr[0])]

            if fixed == self.major:
                return file['id']

    def insertFile(self):
        refresh_json = False
        self.idSHPE_Folder = self.getMainFolder()
        if self.course != 'null':

            if self.course.split()[0] in self.todo:
                classes = self.todo[self.course.split()[0]]

                if self.course in classes:
                    info = classes[self.course]

                else:
                    refresh_json = True
                    self.idMajorFolder = self.getIdMajor()
                    info = self.createCourseFolder()

                if self.docType in info:
                    self.uploadDoc(info[self.docType])
                else:
                    self.uploadDoc(info['Other'])

            else:
                refresh_json = True
                print("the folder for the major doesn't exist")
                # create the major folder, check for name, maybe dictionary?
                # how? if we only got the letters and not the full name

        if refresh_json:
            self.courseRefresh()


    def uploadDoc(self, id):
        ind = self.document.index('=')
        idDoc = self.document[ind + 1:len(self.document)]

        file = self.drive.CreateFile({'id': idDoc})
        string = file['title']
        #manage having the correct name
        file.GetContentFile(string)

        file = self.drive.CreateFile({'title': string,
                                 'parents': [{'kind': 'drive#fileLink', 'id': id}]})
        file.SetContentFile(string)
        file.Upload()

        os.remove(string)


    def createCourseFolder(self):
        folderNew = self.drive.CreateFile({'title': self.course, 'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{'id': self.idMajorFolder}]})
        folderNew.Upload()
        wanted = ['Quizzes and Midterms', 'Other', 'Homework']
        id = {}
        id['id'] = folderNew['id']
        for name in wanted:
            fold = self.drive.CreateFile({'title': name, 'mimeType': 'application/vnd.google-apps.folder',
                                          'parents': [{'id': folderNew['id']}]})
            fold.Upload()
            id[name] = fold['id']
        return id

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


if __name__ == '__main__':
    x = Uploader(sys.argv[1])
    print("process started")
    x.initUpload()
    print("process finished")