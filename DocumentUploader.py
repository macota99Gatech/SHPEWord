from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import os
import jsonNewFiles
import json


class Uploader:

    def __init__(self, csvFile):
        # initialize the google drive api elements
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        # load a dictionary with the values from the csv file
        self.newFiles = jsonNewFiles.newFiles(csvFile)

        # loads the json file with all the ids from the possible needed folders

    def initUpload(self):
        # start the uploading process for each file
        for m, courses in self.newFiles.items():
            self.major = m
            for c, typeFiles in courses.items():
                self.course = c
                for t, list in typeFiles.items():
                    self.docType = t
                    for i in list:
                        self.document = i
                        with open('filesUploaded.json') as f:
                            fileSet = json.load(f)
                            if i not in fileSet:
                                self.insertFile()
                            # else:
                            #     print(self.document + " already in json")


    def getMainFolder(self):
        return "0B5c1_0cbw7-USnk4eG5FQ0hwR1k"


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
        with open('courses.json') as f:
            self.todo = json.load(f)

        # gets the id from the GT-SHPE folder
        self.idSHPE_Folder = self.getMainFolder()
        if self.course != 'null':
            if self.course.split()[0] in self.todo:
                classes = self.todo[self.course.split()[0]]

                # create a folder with the course if it doesn't exist, otherwise we use the existing one
                if self.course in classes:
                    info = classes[self.course]

                else:
                    refresh_json = True
                    self.idMajorFolder = self.getIdMajor()
                    info = self.createCourseFolder()

                # upload the file into the folder
                if self.docType in info:
                    self.uploadDoc(info[self.docType])
                else:
                    self.uploadDoc(info['Other'])

            else:
                # refresh_json = True
                print("the folder for the major doesn't exist")

        # entered only if a major is created or a new course is created
        if refresh_json:
            # refresh the json file with the new ids
            self.refreshJson(info)


    def uploadDoc(self, id):
        try:
            idDoc = self.document

            file = self.drive.CreateFile({'id': idDoc})
            #removes peoples' names from file names
            string = file['title'].split(" - ")[0]
            # get downloads the file into the computer
            file.GetContentFile(string)

            # uploads the file into the drive
            file = self.drive.CreateFile({'title': string,
                                          'parents': [{'kind': 'drive#fileLink', 'id': id}]})
            file.SetContentFile(string)
            file.Upload()

            with open("filesUploaded.json") as f:
                files = json.load(f)

            files[self.document] = ""

            with open("filesUploaded.json", "w") as f:
                json.dump(files, f, indent=2)

            # deletes the file from computer
            os.remove(string)
        except:
            return


    def createCourseFolder(self):
        folderNew = self.drive.CreateFile({'title': self.course, 'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{'id': self.idMajorFolder}]})
        folderNew.Upload()
        self.newFolderID = folderNew["id"]
        wanted = ['Quizzes and Midterms', 'Other', 'Homework']
        id = {}
        id['id'] = folderNew['id']
        for name in wanted:
            fold = self.drive.CreateFile({'title': name, 'mimeType': 'application/vnd.google-apps.folder',
                                          'parents': [{'id': folderNew['id']}]})
            fold.Upload()
            id[name] = fold['id']
        return id

    def getCourses(self, idSHPE_Folder, drive):
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
        id_FolderSHPE = self.getMainFolder()
        courses, codes = self.getCourses(id_FolderSHPE, self.drive)
        data = json.loads(json.dumps(courses))
        dataCode = json.loads(json.dumps(codes))

        with open('courses.json', 'w') as f:
            json.dump(data, f, indent=2)

        with open('codes.json', 'w') as f:
            json.dump(dataCode, f, indent=2)

        print("Courses Updated")

    def refreshJson(self, info):
        print("Started updating json file \n")
        with open('courses.json') as f:
            oldDict = json.load(f)

        major = self.course.split()[0]
        oldDict[major][self.course] = info

        with open('courses.json', 'w') as f:
            json.dump(oldDict, f, indent=2)

        print("Finish updating json files \n")


if __name__ == '__main__':
    # run from command line with csv file as argument
    x = Uploader(sys.argv[1])
    print("process started")

    # after initializing, start the upload
    x.initUpload()
    print("process finished, all files uploaded")