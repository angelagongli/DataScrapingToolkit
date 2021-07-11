from selenium import webdriver
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
ChromeOptions.add_experimental_option('useAutomationExtension', False)
ChromeOptions.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe', options=ChromeOptions)

# All we know about the student's relative is the student's relative's name since the
# Student's relative's hometown cannot be inferred with certainty from the student's own hometown =>
# Pulling of Student's Relative Voter Registration Data will be based entirely on the student's relative's name

from random import randint
from time import sleep
import pandas as pd
import os
from bs4 import BeautifulSoup
import re
import collections

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'
for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    fullStudentResultFilePath = os.path.join(root, 'StudentResults', file)
    if os.path.isfile(fullFilePath) and os.path.isfile(fullStudentResultFilePath):
        df = pd.read_excel(fullStudentResultFilePath, sheet_name='IdentifiedStudentRelatives')
        StudentRelativeResult = collections.namedtuple('StudentRelativeResult',
            ['student_no', 'firstname', 'middlename', 'lastname',
            'school', 'cohort', 'city', 'state', 'studentRelativeFirstName',
            'studentRelativeMiddleName', 'studentRelativeLastName', 'resultName',
            'resultAge', 'resultCity', 'resultVoterRecordURL'])
        StudentRelativeResults = []
        for identifiedStudentRelative in df.itertuples(name='IdentifiedStudentRelative'):
            if identifiedStudentRelative.studentRelativeMiddleName.strip():
                queryString = f"{identifiedStudentRelative.studentRelativeFirstName}-{identifiedStudentRelative.studentRelativeMiddleName}-{identifiedStudentRelative.studentRelativeLastName}"
            else:
                queryString = f"{identifiedStudentRelative.studentRelativeFirstName}-{identifiedStudentRelative.studentRelativeFirstName}"
            driver.get(f"https://voterrecords.com/voters/{queryString}/1")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            header = soup.find(attrs={"class":"BottomMargin10 TopH1"}).contents[1]
            headerRegex = re.compile("( has) ([\d|,]+) Voter Record")
            headerRegexMatch = headerRegex.match(header)
            voterRecordNumber = headerRegexMatch.group(2)
            if voterRecordNumber != "0":
                print("Pulling All from First Page...")
                for person in soup.find_all('tr'):
                    if person.find_next().name == "th":
                        print("Header")
                        continue
                    cursor = person.find_next()
                    resultName = cursor.span.span.a.get_text().strip()
                    # Keep Only Exact First Name/Last Name Because the Relative's Name is All We Have to Go On
                    if not (identifiedStudentRelative.studentRelativeFirstName.upper() in resultName.upper() and
                    identifiedStudentRelative.studentRelativeLastName.upper() in resultName.upper()):
                        continue
                    resultVoterRecordURL = cursor.span.span.a['href']
                    resultAge = ""
                    resultAgeExistingTag = cursor.span.find('strong', text=re.compile(".*Age.*"))
                    if resultAgeExistingTag is not None:
                        resultAge = resultAgeExistingTag.next_element.next_element
                    cursor = cursor.find_next_sibling()
                    resultCity = ""
                    resultCityExistingTag = cursor.find('strong', text=re.compile(".*Residential Address.*"))
                    if resultCityExistingTag is not None:
                        resultCity = resultCityExistingTag.find_next('span').string
                    studentRelativeResult = StudentRelativeResult(identifiedStudentRelative.student_no,
                        identifiedStudentRelative.firstname, identifiedStudentRelative.middlename,
                        identifiedStudentRelative.lastname, identifiedStudentRelative.school,
                        identifiedStudentRelative.cohort, identifiedStudentRelative.city,
                        identifiedStudentRelative.state, identifiedStudentRelative.studentRelativeFirstName,
                        identifiedStudentRelative.studentRelativeMiddleName, identifiedStudentRelative.studentRelativeLastName,
                        resultName, resultAge, resultCity, resultVoterRecordURL)
                    StudentRelativeResults.append(studentRelativeResult)
            sleep(randint(20,25))
        StudentRelativeResult_DF = pd.DataFrame(data=StudentRelativeResults)
        StudentRelativeResult_DF.to_excel(os.path.join(root, 'StudentResults', file), sheet_name='IdentifiedStudentRelativeResults')
