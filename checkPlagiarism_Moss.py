from pathlib import Path
import pickle
import mosspy
#Accessing .env file
import os
from dotenv import load_dotenv
load_dotenv()

import yaml
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

#Fetch necessary data from config file
mossPlagiarismCheckLogFile = cfg["log_file_names"]["check_moss_plagiarism"]
language = cfg["assignment_details"]["language"]
gitFetchReposIntoDirectoryName = cfg["directory_names"]["git_repos_save_folder"]
mossReportUrlPickleFile = cfg["pickle_files"]["moss_report_url"]
studentToFolderMapperPickleFile = cfg["pickle_files"]["folder_mapper"]

import sys
sys.stdout = open(mossPlagiarismCheckLogFile, 'w')

userid = int(os.getenv("MOSS_USER_ID")) #Fetch from .env file
m = mosspy.Moss(userid, language)

# # Adding base files
# m.addBaseFile("submission/a01.py")
# m.addBaseFile("submission/test_student.py")

# Submission Files
homeDir = gitFetchReposIntoDirectoryName
# Fetching pickled mapped folders dictionary
with open(studentToFolderMapperPickleFile, 'rb') as f:
    folderMapper = pickle.load(f)

for studentName in folderMapper.keys():
    print("Folder accessed for " + studentName + " is " + str(Path(homeDir, studentName, folderMapper[studentName])))
    m.addFilesByWildcard(str(Path(homeDir, studentName, folderMapper[studentName])) + "/*.py")

url = m.send() # Submission Report URL

print ("Report Url: " + url)

# # Save report file
# m.saveWebPage(url, "MOSS-report-raw.html")

# Save report URL to pickle file
with open(mossReportUrlPickleFile, 'wb') as f:
    pickle.dump(url, f)