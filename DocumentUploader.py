from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import sys
import os

#implement json files so that the process is faster?
class Uploader:

    def __init__(self, csvFile):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        self.data = pd.read_csv(csvFile)
        self.data = self.data.fillna('null')

    def initUpload(self):
        for index, row in self.data.iterrows():
            for i in range(5):
                self.course = row[i]
                self.prof = row[i + 5]
                self.docType = row[i + 10]
                self.document = row[i + 15]
                self.insertFile()
                break
            break


    def getMainFolder(self):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == 'GT-SHPE Word Dev':
                return file['id']


    def insertFile(self):
        self.idSHPE_Folder = self.getMainFolder()
        if self.course != 'null':
            self.majorInfo = self.majorFolderExist()
            self.idMajorFolder = self.majorInfo[1]

            if self.majorInfo[0]:
                self.courseInfo = self.courseFolderExist()
                self.idCourseFolder = self.courseInfo[1]

                if self.courseInfo[0]:
                    self.docTypeInfo = self.docTypeExist()
                    self.idDocTypeFolder = self.docTypeInfo[1]
                    if self.docTypeInfo[0]:
                        self.uploadDoc(self.idDocTypeFolder)
                    else:
                        print("Error, DocType not Found")

                else:
                    self.newFolder_id = self.createCourseFolder()
                    newFoldID = self.createDocTypeFolder(self.newFolder_id)
                    self.uploadDoc(newFoldID)
            else:
                print("the folder for the major doesn't exist")
                # create the major folder, check for name, maybe dictionary?
                # how? if we only got the letters and not the full name


    def createDocTypeFolder(self, id):
        folderNew = self.drive.CreateFile({'title': 'newFolder', 'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{'id': id}]})
        folderNew.Upload()
        return folderNew['id']


    def uploadDoc(self, id):
        ind = self.document.index('=')
        idDoc = self.document[ind + 1:len(self.document)]

        file = drive.CreateFile({'id': idDoc})
        string = file['title']
        #manage having the correct name
        file.GetContentFile(string)

        file = self.drive.CreateFile({'title': string,
                                 'parents': [{'kind': 'drive#fileLink', 'id': id}]})
        file.SetContentFile(string)
        file.Upload()

        os.remove(string)


    def majorFolderExist(self):
        fileChild = self.drive.ListFile(
            {'q': "'%s' in parents and trashed=false" % (self.idSHPE_Folder)}).GetList()  # returns an empty list
        for file in fileChild:
            title = file['title']
            courseTitle = title.split()[0]
            alias = title[1:len(courseTitle) - 1]

            indCourseName = self.course.split()
            aliasCourse = indCourseName[0]
            if alias == aliasCourse:
                return True, file['id']

        return False, None


    def courseFolderExist(self):
        files = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.idMajorFolder}).GetList()
        for fil in files:
            if fil['title'] == self.course:
                return True, fil['id']
        return False, None


    def createCourseFolder(self):
        folderNew = self.drive.CreateFile({'title': self.course, 'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{'id': self.idMajorFolder}]})
        folderNew.Upload()
        return folderNew['id']


    def docTypeExist(self):
        files = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % (self.idCourseFolder)}).GetList()
        for file in files:
            if file['title'] == self.docType:
                return True, file['id']
        return False, None


if __name__ == '__main__':
    x = Uploader(sys.argv[1])
    print("process started")
    x.initUpload()
    print("process finished")