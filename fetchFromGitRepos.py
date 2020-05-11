import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

import git
import pandas as pd
from pathlib import Path
import shutil
import os
from os.path import isfile, join
from pprint import pprint
import string
import pickle
import sys

#Fetch necessary data from config file
fetchGitRepoLogFile = cfg["log_file_names"]["fetch_git_repos"]
assignmentToBeGraded = cfg["assignment_details"]["name_of_assignment"]
csvFileName = cfg["assignment_details"]["form_responses_csv"]
gitFetchReposIntoDirectoryName = cfg["directory_names"]["git_repos_save_folder"]
studentToFolderMapperPickleFile = cfg["pickle_files"]["folder_mapper"]
incorrectSubmissionsPickleFile = cfg["pickle_files"]["incorrect_submissions"]

#Specify log file to write to
sys.stdout = open(fetchGitRepoLogFile, 'w')

#Create directory to clone git repos into
gitReposFolder = Path(gitFetchReposIntoDirectoryName)
if(not gitReposFolder.exists()):
    Path(gitReposFolder).mkdir(parents=True, exist_ok=True)

#Contains details of erroneus submissions
incorrectFormatSubmission = {}

#Store names of the directories for this assignment (Students have given different versions of Assignment_MLP as directory name)
folderMapper = {}

# Format names of students to be valid as a directory name
def convertToFolderName(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return(''.join(c for c in filename if c in valid_chars))

def deleteAllFiles(directory):
    print("Deleting the existing folders from Machine_Learning_Git_Submissions to clean up for every run")
    for folder in os.listdir(directory):
        dirpath = Path(directory, folder)
        if dirpath.exists() and dirpath.is_dir():
            print(folder + " , ", end='')
            shutil.rmtree(dirpath)
    print("\n")

deleteAllFiles(gitFetchReposIntoDirectoryName)

# FETCHING ALL REPOS FROM GITHUB
print("\n\n######## 1. Reading from CSV and Performing Git Clone ########")
gitData = pd.read_csv(csvFileName)
namesOfFolders = []
for (idx, row) in gitData.iterrows():
    try:
        row.loc["Full Name"] = convertToFolderName(row.loc["Full Name"])
        dirpath = Path(gitFetchReposIntoDirectoryName, row.loc['Full Name'])
        git.repo.base.Repo.clone_from(
            row.loc["GitHub Link"],
            str(Path(gitFetchReposIntoDirectoryName, row.loc['Full Name']))
        )
        print("SUCCESS: Successfully fetched Git Repo of", row.loc['Full Name'])
        namesOfFolders.append(row.loc['Full Name'])
    except Exception as e:
        incorrectFormatSubmission[row.loc['Full Name']] = "Error while fetching Git repo, ERROR: " + str(e)
        print("ERROR: Error while fetching Git Repo of", row.loc['Full Name'] , "Exception occurred: ", e)

# VERIFYING DIRECTORY STRUCTURE OF EACH REPO
def checkIfDirectoryExists(dir_path, directoryToCheck):
    dirlist = [ item for item in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, item)) ]
    for directory in dirlist:
        if( directoryToCheck.split("_")[0].lower() in directory.lower() and directoryToCheck.split("_")[1].lower() in directory.lower()):
            return(directory)
    return(False)

# VERIFYING IF .py FILE EXISTS IN THE DIRECTORY
def checkIfPythonFileExists(dir_path):
    onlyfiles = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]
    for file in onlyfiles:
        if file.endswith(".py"):
            return(True)

print("\n\n######## 2. Checking submission folder format ########")
correctFormatSubmission = []
for folder in namesOfFolders:
    dir_path = Path(gitFetchReposIntoDirectoryName, folder)
    directoryExists = checkIfDirectoryExists(dir_path, assignmentToBeGraded)
    if(directoryExists):
        if(checkIfPythonFileExists(Path(dir_path, directoryExists))):
            folderMapper[folder] = directoryExists
            correctFormatSubmission.append(folder)
        else:
            incorrectFormatSubmission[folder] = "No .py file found in Assignment_<assignmentName> directory (Note, please do not place the Python file in a subdirectory in the Assignment_<assignmentName> directory)"
    else:
        incorrectFormatSubmission[folder] = "Incorrect Assignment directory structure. Please name the directory Assignment_<assignmentName> format"

print("Students who have submitted correctly: ", correctFormatSubmission)
print("\nStudent who have NOT submitted correctly: \n")
pprint(incorrectFormatSubmission)

with open(incorrectSubmissionsPickleFile, 'wb') as f:
    pickle.dump(incorrectFormatSubmission, f)

with open(studentToFolderMapperPickleFile, 'wb') as f:
    pickle.dump(folderMapper, f)