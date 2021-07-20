# We want to come to only one StudentResult for every student in Menaka's dataset,
# => Narrow the set of StudentResult based on exact First Name and Last Name as well as
# Middle Name/Middle Initial, Expected Age and City where we can

from selenium import webdriver
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
ChromeOptions.add_experimental_option('useAutomationExtension', False)
ChromeOptions.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe', options=ChromeOptions)

# Advice from Menaka: WebDriver must sleep generated time interval of 20-25 seconds
# Before every scrape, waiting enough time to be able to handle CAPTCHA <- TODO
from random import randint
from time import sleep
from bs4 import BeautifulSoup
import re
import datetime
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='Student_DB')
outerCursor = cnx.cursor(buffered=True)
innerCursor = cnx.cursor(buffered=True)

pull_studentinformation = ("SELECT cohort, firstName, middleName, lastName, "
                            "city, state, country FROM Students WHERE id=%(student_id)s")

pull_allresultsforstudentatstep = ("SELECT id, resultName, resultAge, resultCity, resultCityHistory, resultType, resultData "
                                    "FROM StudentResults WHERE student_id=%(student_id)s AND identificationStep=%(identificationStep)s")

update_studentresultidentificationstep = ("UPDATE StudentResults SET identificationStep=%s WHERE id=%s")

insert_studentrelativeresult = ("INSERT INTO StudentRelativeResults "
    "(student_id, relativeResultName, relativeResultVoterRecordURL, relativeResultSource) "
    "VALUES (%(student_id)s, %(relativeResultName)s, %(relativeResultVoterRecordURL)s, "
    "%(relativeResultSource)s)")

for i in range(1, 100):
    student_data = {
        'student_id': i,
        'identificationStep': 'Not Identified'
    }

    outerCursor.execute(pull_studentinformation, student_data)

    for (cohort, firstName, middleName, lastName, city, state, country) in outerCursor:
        desiredStudentAge = datetime.datetime.now().year - cohort + 22
        firstName = firstName
        middleName = middleName
        lastName = lastName
        city = city

    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory, resultType, resultData) in outerCursor:
        if (firstName in resultName.upper() and
            lastName in resultName.upper()):
            innerCursor.execute(update_studentresultidentificationstep, ('First Pass', id))
            cnx.commit()

    student_data['identificationStep'] = 'First Pass'
    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory, resultType, resultData) in outerCursor:
        if middleName and (middleName in resultName.upper() or
            f" {middleName[0:1]} " in resultName.upper()):
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()
        elif resultAge and (resultAge >= desiredStudentAge - 1 and
            resultAge <= desiredStudentAge + 1):
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()
        elif city and city in resultCityHistory.upper():
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()

    student_data['identificationStep'] = 'Refined'
    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory, resultType, resultData) in outerCursor:
        if ((middleName and (middleName in resultName.upper() or
            f" {middleName[0:1]} " in resultName.upper())) and
            (resultAge and (resultAge >= desiredStudentAge - 1 and
            resultAge <= desiredStudentAge + 1)) and
            (city and city in resultCityHistory.upper())):
            innerCursor.execute(update_studentresultidentificationstep, ('Identified', id))
            cnx.commit()
            break

    student_data['identificationStep'] = 'Identified'
    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    # Once the desired Student is identified and when the desired Student's StudentResult
    # Contains the Student's Relative data, we generate all of the Student's StudentRelativeResults,
    # Trusting the accuracy of TruthFinder's designation of the Student's Relatives
    for (id, resultName, resultAge, resultCity, resultCityHistory, resultType, resultData) in outerCursor:
        if resultType == "StudentRelatives":
            IdentifiedStudentRelativeNames = resultData.split("*")
            for StudentRelativeName in IdentifiedStudentRelativeNames:
                print(f"Now Looking Up {StudentRelativeName}...")
                StudentRelativeNameArr = StudentRelativeName.split(" ")
                if len(StudentRelativeNameArr) == 2:
                    studentRelativeFirstName = StudentRelativeNameArr[0]
                    studentRelativeLastName = StudentRelativeNameArr[1]
                elif len(StudentRelativeNameArr) == 3:
                    studentRelativeFirstName = StudentRelativeNameArr[0]
                    studentRelativeMiddleName = StudentRelativeNameArr[1]
                    studentRelativeLastName = StudentRelativeNameArr[2]
                elif len(StudentRelativeNameArr) > 3:
                    studentRelativeFirstName = StudentRelativeNameArr[0]
                    studentRelativeMiddleName = StudentRelativeNameArr[1]
                    for namePiece in StudentRelativeNameArr[2:-1]:
                        studentRelativeMiddleName = studentRelativeMiddleName + namePiece
                    studentRelativeLastName = StudentRelativeNameArr[-1]
                if studentRelativeMiddleName.strip():
                    queryString = f"{studentRelativeFirstName}-{studentRelativeMiddleName}-{studentRelativeLastName}"
                else:
                    queryString = f"{studentRelativeFirstName}-{studentRelativeLastName}"
                driver.get(f"https://voterrecords.com/voters/{queryString}/1")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                header = soup.find(attrs={"class":"BottomMargin10 TopH1"}).contents[1]
                headerRegex = re.compile("( has) ([\d|,]+) Voter Record")
                headerRegexMatch = headerRegex.match(header)
                voterRecordNumber = headerRegexMatch.group(2)
                if voterRecordNumber != "0":
                    print(f"Pulling All from {StudentRelativeName}'s First Page...")
                    StudentRelativeResults = []
                    for person in soup.find_all('tr'):
                        if person.find_next().name == "th":
                            print("Header")
                            continue
                        driverCursor = person.find_next()
                        resultName = driverCursor.span.span.a.get_text().strip()
                        # Keep Only Exact First Name/Last Name Because the Relative's Name is All We Have to Go On
                        if not (studentRelativeFirstName.upper() in resultName.upper() and
                            studentRelativeLastName.upper() in resultName.upper()):
                            continue
                        resultVoterRecordURL = driverCursor.span.span.a['href']
                        if not resultVoterRecordURL:
                            continue
                        resultAge = ""
                        resultAgeExistingTag = driverCursor.span.find('strong', text=re.compile(".*Age.*"))
                        if resultAgeExistingTag is not None:
                            resultAge = str(resultAgeExistingTag.next_element.next_element)
                        driverCursor = driverCursor.find_next_sibling()
                        resultCity = ""
                        resultCityExistingTag = driverCursor.find('strong', text=re.compile(".*Residential Address.*"))
                        if resultCityExistingTag is not None:
                            resultCity = resultCityExistingTag.find_next('span').get_text()
                        StudentRelativeResult = {
                            'student_id': i,
                            'relativeResultName': resultName,
                            'relativeResultVoterRecordURL': resultVoterRecordURL,
                            'relativeResultSource': 'StudentRelatives'
                        }
                        StudentRelativeResults.append(StudentRelativeResult)
                innerCursor.executemany(insert_studentrelativeresult, StudentRelativeResults)
                cnx.commit()
                sleep(randint(20,25))

innerCursor.close()
outerCursor.close()
cnx.close()
