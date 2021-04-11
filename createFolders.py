from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# hardcoded the id of the GT-SHPE word folder
id = '0B5c1_0cbw7-USnk4eG5FQ0hwR1k'

fileChild = drive.ListFile(
    {'q': "'%s' in parents and trashed=false" % (id)}).GetList()


# normalize all the folders in each courses
for file in fileChild:
    idMajor = file['id']

    courses = drive.ListFile(
    {'q': "'%s' in parents and trashed=false" % (idMajor)}).GetList()
    for course in courses:
        try:
            courseId = course['id']

            folders = drive.ListFile(
                {'q': "'%s' in parents and trashed=false" % (courseId)}).GetList()

            names = {}
            for folderName in folders:
                names[folderName['title']] = folderName['id']

            wanted = ['Quizzes and Midterms', 'Other', 'Homework and Notes']

            for name in wanted:
                if name not in names:
                    #create the file in coureId with the name
                    folderNew = drive.CreateFile({'title': name, 'mimeType': 'application/vnd.google-apps.folder',
                                                  'parents': [{'id': courseId}]})
                    folderNew.Upload()
        except:
            continue
