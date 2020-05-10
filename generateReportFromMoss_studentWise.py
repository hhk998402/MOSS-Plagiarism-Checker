from bs4 import BeautifulSoup
import requests as req
import pickle
import re
import xlwt 
from xlwt import Workbook
from pathlib import Path
import os
import shutil
from pprint import pprint

import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

import sys
sys.stdout = open('LOGS - Student Wise Report Generation.txt', 'w')

# ####### Data you must fill in ##########
# reportURL = "http://moss.stanford.edu/results/3/2475779986448/"
# reportURL = "http://moss.stanford.edu/results/9/9592813757221/"
reportURL = "http://moss.stanford.edu/results/2/363941784921"
thresholdPercentage = 50

#Create directory to store Plagiarism Reports
plagiarismReportsFolder = Path(cfg["directory_names"]["save_reports_to"])
if(not plagiarismReportsFolder.exists()):
    Path(plagiarismReportsFolder).mkdir(parents=True, exist_ok=True)

def deleteAllFiles(directory):
    for file in os.listdir(directory):
        filePath = Path(directory, file)
        if filePath.exists() and filePath.is_file():
            filePath.unlink()

deleteAllFiles(cfg["directory_names"]["save_reports_to"])

print("#### " + str(thresholdPercentage) + "% CODE PLAGIARISM REPORT GENERATION - Student who have not copied ####\n")
totalNumNotCopied = 0

def addHeaders(sheet):
    style = xlwt.easyxf('font: bold 1, color red;')
    sheet.write(0,0,"Name of Student",style)
    sheet.write(0,1,"File Name",style)
    sheet.write(0,2,"Copied From",style)
    sheet.write(0,3,"File Name",style)
    sheet.write(0,4,"Percentage similarity",style)
    sheet.write(0,5,"Link to Code Comparison",style)
    return(sheet)

def prepareReport(table, studentName, sheet):
    global totalNumNotCopied
    flag = False
    sheet = addHeaders(sheet)
    rowCount = 1
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if(len(cells) > 0):
            nameOfFileOne = cells[0].find(text=True)
            nameOfFileTwo = cells[1].find(text=True)
            studentFileTwo = nameOfFileTwo.split("/")[1]
            linesMatched = cells[2].find(text=True)
            if(studentName in nameOfFileOne):
                percentageSimilarity = nameOfFileOne.split(" ")[-1]
                percentageParseAsInt = int(re.findall('\d+', percentageSimilarity)[0])
                linkToComparison = cells[0].find('a', attrs={'href': re.compile("^http://")}).get('href')
                nameOfStudentComparedTo = nameOfFileTwo.split("/")[1]
                if(percentageParseAsInt > thresholdPercentage):
                    flag = True
                    #Write to corresponding excel sheet
                    sheet.write(rowCount, 0, studentName)
                    sheet.write(rowCount, 1, ('/'.join(nameOfFileOne.split("/")[2:])).split(" ")[0])
                    sheet.write(rowCount, 2, nameOfStudentComparedTo)
                    sheet.write(rowCount, 3, ('/'.join(nameOfFileTwo.split("/")[2:])).split(" ")[0])
                    sheet.write(rowCount, 4, percentageSimilarity)
                    sheet.write(rowCount, 5, linkToComparison)
                    rowCount += 1
            
            if(studentName in nameOfFileTwo):
                linkToComparison = cells[1].find('a', attrs={'href': re.compile("^http://")}).get('href')
                percentageSimilarity = nameOfFileTwo.split(" ")[-1]
                percentageParseAsInt = int(re.findall('\d+', percentageSimilarity)[0])
                nameOfStudentComparedTo = nameOfFileOne.split("/")[1]
                if(percentageParseAsInt > thresholdPercentage):
                    flag = True
                    #Write to corresponding excel sheet
                    sheet.write(rowCount, 0, studentName)
                    sheet.write(rowCount, 1, ('/'.join(nameOfFileTwo.split("/")[2:])).split(" ")[0])
                    sheet.write(rowCount, 2, nameOfStudentComparedTo)
                    sheet.write(rowCount, 3, ('/'.join(nameOfFileOne.split("/")[2:])).split(" ")[0])
                    sheet.write(rowCount, 4, percentageSimilarity)
                    sheet.write(rowCount, 5, linkToComparison)
                    rowCount += 1

    if(flag == False):
        totalNumNotCopied += 1
        print(str(totalNumNotCopied) + ". " + studentName)

# Fetching pickled dictionary with student names
with open(cfg["pickle_files"]["incorrect_submissions"], 'rb') as f:
    incorrectFormatSubmission = pickle.load(f)

with open(cfg["pickle_files"]["folder_mapper"], 'rb') as f:
    folderMapper = pickle.load(f)
    studentNames = [x.replace(' ','_') for x in folderMapper.keys()]

resp = req.get(reportURL)

soup = BeautifulSoup(resp.text, 'lxml')
table = soup.find('table')

count = 0
count2 = 0
for studentName in studentNames:
    wb = Workbook()
    sheet = wb.add_sheet(studentName)
    prepareReport(table, studentName, sheet)
    if(len(sheet._Worksheet__rows)>1):
        wb.save(str(Path(cfg["directory_names"]["save_reports_to"], studentName)) + ".xls")
        count2 += 1
    count += 1

print("\n\nTotal Number of Submissions with NO issues = " + str(len(studentNames)))
print("Total Number of Submissions with issues = " + str(len(incorrectFormatSubmission.keys())))
pprint(incorrectFormatSubmission)
print("\nTotal number of students who have NOT COPIED at " + str(thresholdPercentage) + "% threshold percentage = " + str(totalNumNotCopied))
print("\nTotal number of students who have plagiarism issues " + str(thresholdPercentage) + "% threshold percentage = " + str(len(studentNames)- totalNumNotCopied))
print("\nSaved Excel sheets to " + cfg["directory_names"]["save_reports_to"] + " directory")