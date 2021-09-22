# SHPEWord 
Takes google drive documents from google form responses and places them in appropriate drive folders

## Setup

Clone the repo to have a local copy of the code.

### Getting Google Drive API Credentials

Visit console.cloud.google.com and create a new project.\
Once the project is created, click the `CREATE CREDENTIALS` button followed by `OAuth Client ID`

If asked to configure consent screen, go ahead and follow the instructions and select `External` for the user type.
Continue filling out the necessary information such as app name and email with whatever is appropriate. No scopes nor test users are necessary.

Once the app registration process is complete, navigate to the `Credentials` tab on the sidebar and click on create credentials and OAuth Client ID once more.

Select 'Web Application' for the Application Type and fill in a name like 'SHPEWord' or anything else appropriate for the name field.
For the following two sections, `Authorized JavaScript origins` and `Authorized redirect URIs`, add the uri `http://localhost:8080`\
Upon successful creation you should be able to hit `Download JSON` or `Download OAuth Client`. Download this and name the file `client_secrets.json` and 
place it in the directory containing your copy of the code.

### Configuring the Code to Point to the Right Google Drive Folder

Admittedly this is pretty hacky, but on line 41 in `DocumentUploader.py`, line 9 in `jsonUpdate.py`, and line 9 in `createFolders.py` the Google Drive Folder ID is hardcoded to point to the 
current SHPEWord folder. **Leave this as is** if you wish to run this program on the folder, but feel free to change the ID to another folder's if you want to run a 
test on a dummy folder or anything else.

### How to Feed Google Form Responses Into the Program

[This Google Form](https://docs.google.com/forms/d/e/1FAIpQLSf48g9wgfDpt565137-Hoy1IqBkOs7nPmdvmA6tJ83MseKCcQ/viewform?usp=sf_link) can serve as an example template
for the necessary information to collect.\
**The fields that are strictly required and must match the exact strings are:**
- Document Upload X
- Course Name X
- Document Type X
- Quizzes and Midterms
- Homework and Notes

Where X ranges from 1-5.\
If the titles of these fields do not match the above strings, **the program will not execute properly.** The order in which the fields appear does not matter, 
as long as they are somewhere in the form. 

Once you have received responses, you can export and view them as a google sheet as well as download as a csv. Go ahead and download as a csv and place the file 
in the directory containing the program source code. 

## Running the Program

If all the above setup instructions have been successfully completed, you should be able to run the program!

Open up a terminal, `cd` into your directory containing the source code, and run the `DocumentUploader.py` script which takes in a command line argument of the 
name of your csv file containing your form responses.

```shell
martincorredor$ python3 DocumentUploader.py YourResponsesFile.csv
```
If execution is successful, you should be redirected to a google popup for authentication flow. Following authentication, the program will execute and temporarily 
download the files from the responses before reuploading them to the Drive folder and deleting the local copy. 

The `filesUploaded.json` file will also be updated and populated with the IDs of the uploaded files, if the ID of a file is already in this set, the file 
will not be reuploaded. 
