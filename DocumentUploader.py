from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import sys
import os
import jsonNewFiles
import json

#implement json files so that the process is faster?
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
                        break
                    break
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

            if fixed == self.course.split()[0]:
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
                    self.idMajorFolder = self.getIdMajor()
                    info = self.createCourseFolder()

                if self.docType in info:
                    self.uploadDoc(info[self.docType])
                else:
                    self.uploadDoc(info['Other'])

            else:
                print("the folder for the major doesn't exist")
                # create the major folder, check for name, maybe dictionary?
                # how? if we only got the letters and not the full name

        if refresh_json:
            self.refresh()


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


if __name__ == '__main__':
    x = Uploader(sys.argv[1])
    print("process started")
    x.initUpload()
    print("process finished")