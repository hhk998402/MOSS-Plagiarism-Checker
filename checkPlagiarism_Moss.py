import sys
sys.stdout = open('checkPlagiarism_Moss_LOGS.txt', 'w')

#Accessing .env file
import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import pickle
import mosspy

userid = int(os.getenv("MOSS_USER_ID")) #Fetch from .env file
m = mosspy.Moss(userid, "python")

# # Adding base files
# m.addBaseFile("submission/a01.py")
# m.addBaseFile("submission/test_student.py")

# Submission Files
homeDir = "Machine_Learning_Git_Submissions"
# Fetching pickled mapped folders dictionary
with open('folderMapper.pkl', 'rb') as f:
    folderMapper = pickle.load(f)

for studentName in folderMapper.keys():
    print("Folder accessed for " + studentName + " is " + str(Path(homeDir, studentName, folderMapper[studentName])))
    m.addFilesByWildcard(str(Path(homeDir, studentName, folderMapper[studentName])) + "/*.py")

url = m.send() # Submission Report URL

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, "MOSS-report-raw.html")