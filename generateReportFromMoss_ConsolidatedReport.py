from bs4 import BeautifulSoup
import requests as req
import pickle
import re
import xlwt 
from xlwt import Workbook
from pathlib import Path

import sys
sys.stdout = open('LOGS - Consolidated Report Generation.txt', 'w')

# ####### Data you must fill in ##########
# reportURL = "http://moss.stanford.edu/results/3/2475779986448/"
# reportURL = "http://moss.stanford.edu/results/9/9592813757221/"
reportURL = "http://moss.stanford.edu/results/2/363941784921"

print("#### CONSOLIDATED CODE PLAGIARISM REPORT GENERATION ####\n")

# Workbook is created 
wb = Workbook()

totalStudentsNotCopied = 0

def addHeaders(sheet):
    style = xlwt.easyxf('font: bold 1, color red;')
    sheet.write(0,0,"Name of Student",style)
    sheet.write(0,1,"File Name",style)
    sheet.write(0,2,"Copied From",style)
    sheet.write(0,3,"File Name",style)
    sheet.write(0,4,"Percentage similarity",style)
    sheet.write(0,5,"Link to Code Comparison",style)
    return(sheet)

def prepareReport(table, studentName):
    global totalStudentsNotCopied
    flag = False
    sheet = wb.add_sheet(studentName)
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
                flag = True
                linkToComparison = cells[0].find('a', attrs={'href': re.compile("^http://")}).get('href')
                percentageSimilarity = nameOfFileOne.split(" ")[-1]
                nameOfStudentComparedTo = nameOfFileTwo.split("/")[1]
                #Write to corresponding excel sheet
                sheet.write(rowCount, 0, studentName)
                sheet.write(rowCount, 1, ('/'.join(nameOfFileOne.split("/")[2:])).split(" ")[0])
                sheet.write(rowCount, 2, nameOfStudentComparedTo)
                sheet.write(rowCount, 3, ('/'.join(nameOfFileTwo.split("/")[2:])).split(" ")[0])
                sheet.write(rowCount, 4, percentageSimilarity)
                sheet.write(rowCount, 5, linkToComparison)
                rowCount += 1
            
            if(studentName in nameOfFileTwo):
                flag = True
                linkToComparison = cells[1].find('a', attrs={'href': re.compile("^http://")}).get('href')
                percentageSimilarity = nameOfFileTwo.split(" ")[-1]
                nameOfStudentComparedTo = nameOfFileOne.split("/")[1]
                #Write to corresponding excel sheet
                sheet.write(rowCount, 0, studentName)
                sheet.write(rowCount, 1, ('/'.join(nameOfFileTwo.split("/")[2:])).split(" ")[0])
                sheet.write(rowCount, 2, nameOfStudentComparedTo)
                sheet.write(rowCount, 3, ('/'.join(nameOfFileOne.split("/")[2:])).split(" ")[0])
                sheet.write(rowCount, 4, percentageSimilarity)
                sheet.write(rowCount, 5, linkToComparison)
                rowCount += 1

    if(flag == False):
        totalStudentsNotCopied+=1
        print(str(totalStudentsNotCopied) + ". " + studentName)
    return(sheet)


# Fetching pickled dictionary with student names
with open('folderMapper.pkl', 'rb') as f:
    folderMapper = pickle.load(f)
    studentNames = [x.replace(' ','_') for x in folderMapper.keys()]
    print("Total number of Submissions = " + str(len(studentNames)))
    print("List of Submissions: ", studentNames)

resp = req.get(reportURL)

soup = BeautifulSoup(resp.text, 'lxml')
table = soup.find('table')

print("\n\nStudents who have not copied at all: ")
for studentName in studentNames:
    sheet = prepareReport(table, studentName)

wb.save('ConsolidatedReport_Assignment_MLP.xls')
print("\n\nSaved data to following excel file in root directory: " + 'ConsolidatedReport_Assignment_MLP.xls')