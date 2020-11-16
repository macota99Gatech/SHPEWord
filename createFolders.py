from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

id = '1b5sxUu2RZQCfs_RdBAfofcFjxX0x3dyn'

fileChild = drive.ListFile(
    {'q': "'%s' in parents and trashed=false" % (id)}).GetList()

for file in fileChild:
    idMajor = file['id']

    courses = drive.ListFile(
    {'q': "'%s' in parents and trashed=false" % (idMajor)}).GetList()
    for course in courses:
        coureId = course['id']

        folders = drive.ListFile(
            {'q': "'%s' in parents and trashed=false" % (coureId)}).GetList()

        names = {}
        for folderName in folders:
            names[folderName['title']] = 0

        wanted = ['Quizzes and Midterms', 'Other', 'Homework']

        for name in wanted:
            if name not in names:
                #create the file in coureId with the name
                folderNew = drive.CreateFile({'title': name, 'mimeType': 'application/vnd.google-apps.folder',
                                              'parents': [{'id': coureId}]})
                folderNew.Upload()

