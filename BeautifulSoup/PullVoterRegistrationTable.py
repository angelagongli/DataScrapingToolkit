from bs4 import BeautifulSoup
from bs4.element import NavigableString
import collections
from selenium import webdriver
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
ChromeOptions.add_experimental_option('useAutomationExtension', False)
ChromeOptions.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe', options=ChromeOptions)
from random import randint
from time import sleep
import pandas as pd
import os

# Menaka wants everything in the Overview table: City, Age, Gender and Race
# But there is no need to duplicate everything present in the saved StudentResult
# => Only useful for the StudentRelative: Make sure to keep Student/StudentRelative
# Clearly identified in the dataset all the way through

StudentVoterRecord = collections.namedtuple('StudentVoterRecord',
    # All Kept from StudentResult:
    ['student_no', 'firstname', 'middlename', 'lastname',
    'school', 'cohort', 'city', 'state', 'resultName', 'resultAge', 'resultCity',
    # From Voter Registration Table:
    'PartyAffiliation','RegisteredtoVoteIn','RegistrationDate','VoterStatus',
    'StatusReason','Precinct','PrecinctSplit','Ward','CongressionalDistrict',
    'HouseDistrict','SenateDistrict','CountyDistrict','SchoolBoardDistrict'])
StudentRelativeVoterRecord = collections.namedtuple('StudentRelativeVoterRecord',
    ['studentRelativeName',
    # From Overview Table:
    'Livesin','Age','Gender','Race',
    # All Data Required to Uniquely Identify the Student the Relative Belongs to in
    # Whole Dataset Must Be Kept in Student's Relative Voter Record => Foreign Key
    # Based on the Composite Key
    'student_no', 'school', 'cohort',
    # All of the Student's Information Entered into the URL Returning the StudentResult
    # In Turn Returning the Student's Relative Should be Saved per Menaka's Request:
    'firstname', 'middlename', 'lastname', 'city', 'state',
    # Rest of Data Saved in Student's Relative Voter Record Is Purely Voter Registration Data
    'PartyAffiliation','RegisteredtoVoteIn','RegistrationDate','VoterStatus',
    'StatusReason','Precinct','PrecinctSplit','Ward','CongressionalDistrict',
    'HouseDistrict','SenateDistrict','CountyDistrict','SchoolBoardDistrict'])

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'

for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    fullStudentResultFilePath = os.path.join(root, 'StudentResults', file)
    StudentVoterRecords = []
    StudentRelativeVoterRecords = []
    if os.path.isfile(fullFilePath) and os.path.isfile(fullStudentResultFilePath):
        StudentResult_DF = pd.read_excel(fullStudentResultFilePath, sheet_name='IdentifiedStudentResults')
        StudentVoterRecordResult_DF = StudentResult_DF[StudentResult_DF['resultType'] == 'StudentVoterRecord']
        for StudentResult in StudentVoterRecordResult_DF.itertuples(name='StudentResult'):
            driver.get(f"https://voterrecords.com{StudentResult.resultData}")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            dataPointDictionary = {}
            for tableColumn in soup.find(id="overview").find_all('div') + \
                soup.find(id="voter-registration").find_all('div'):
                for label in tableColumn.find_all('strong'):
                    labelString = label.string.replace(":","").replace(" ","").strip()
                    dataTag = label.find_next_sibling()
                    dataPoint = ""
                    if dataTag:
                        if dataTag.name == "br":
                            dataPoint = label.next_element.next_element
                        else:
                            dataPoint = dataTag.string
                    dataPointDictionary[labelString] = dataPoint
            studentVoterRecord = StudentVoterRecord(
                student_no=StudentResult.student_no,
                firstname=StudentResult.firstname,
                middlename=StudentResult.middlename,
                lastname=StudentResult.lastname,
                school=StudentResult.school,
                cohort=StudentResult.cohort,
                city=StudentResult.city,
                state=StudentResult.state,
                resultName=StudentResult.resultName,
                resultAge=StudentResult.resultAge,
                resultCity=StudentResult.resultCity,
                # From Voter Registration Table:
                PartyAffiliation=dataPointDictionary['PartyAffiliation']
                    if 'PartyAffiliation' in dataPointDictionary else None,
                RegisteredtoVoteIn=dataPointDictionary['RegisteredtoVoteIn']
                    if 'RegisteredtoVoteIn' in dataPointDictionary else None,
                RegistrationDate=dataPointDictionary['RegistrationDate']
                    if 'RegistrationDate' in dataPointDictionary else None,
                VoterStatus=dataPointDictionary['VoterStatus']
                    if 'VoterStatus' in dataPointDictionary else None,
                StatusReason=dataPointDictionary['StatusReason']
                    if 'StatusReason' in dataPointDictionary else None,
                Precinct=dataPointDictionary['Precinct']
                    if 'Precinct' in dataPointDictionary else None,
                PrecinctSplit=dataPointDictionary['PrecinctSplit']
                    if 'PrecinctSplit' in dataPointDictionary else None,
                Ward=dataPointDictionary['Ward']
                    if 'Ward' in dataPointDictionary else None,
                CongressionalDistrict=dataPointDictionary['CongressionalDistrict']
                    if 'CongressionalDistrict' in dataPointDictionary else None,
                HouseDistrict=dataPointDictionary['HouseDistrict']
                    if 'HouseDistrict' in dataPointDictionary else None,
                SenateDistrict=dataPointDictionary['SenateDistrict']
                    if 'SenateDistrict' in dataPointDictionary else None,
                CountyDistrict=dataPointDictionary['CountyDistrict']
                    if 'CountyDistrict' in dataPointDictionary else None,
                SchoolBoardDistrict=dataPointDictionary['SchoolBoardDistrict']
                    if 'SchoolBoardDistrict' in dataPointDictionary else None
                # ... For All Key Fields in the Student's/Student's Relative's Voter Registration
                # Saved from Voter Record Page into DataPointDictionary
            )
            print(studentVoterRecord)
            StudentVoterRecords.append(studentVoterRecord)
            sleep(randint(20,25))
        StudentVoterRecord_DF = pd.DataFrame(data=StudentVoterRecords)
        if not os.path.isdir(os.path.join(root, 'VoterRegistrationData')):
            os.mkdir(os.path.join(root, 'VoterRegistrationData'))
        StudentVoterRecord_DF.to_excel(os.path.join(root, 'VoterRegistrationData', file), sheet_name='StudentVoterRegistrationData')
        StudentRelativeResult_DF = pd.read_excel(fullStudentResultFilePath, sheet_name='IdentifiedStudentRelativeResults')
        for StudentRelativeResult in StudentRelativeResult_DF.itertuples(name='StudentRelativeResult'):
            driver.get(f"https://voterrecords.com{StudentRelativeResult.resultVoterRecordURL}")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            dataPointDictionary = {}
            for tableColumn in soup.find(id="overview").find_all('div') + \
                soup.find(id="voter-registration").find_all('div'):
                for label in tableColumn.find_all('strong'):
                    labelString = label.string.replace(":","").replace(" ","").strip()
                    dataTag = label.find_next_sibling()
                    dataPoint = ""
                    if dataTag:
                        if dataTag.name == "br":
                            dataPoint = label.next_element.next_element
                        else:
                            dataPoint = dataTag.string
                    dataPointDictionary[labelString] = dataPoint
            # Menaka has brought up the Related Records table of the Student's Voter Record page as well =>
            # How do we verify the accuracy of the Student's Relative designation? Here we have not only the
            # Designated Student's Relative's name but his/her full voter record as well, we are going based
            # Entirely on the site's own algorithm but we can save the full voter record of all of the Student's
            # Relatives returned in the Student's Voter Record per Menaka's request
            studentRelatives = []
            for relativeDiv in soup.find(id="related-voters").div:
                if isinstance(relativeDiv, NavigableString):
                    continue
                relativeDataPointDictionary = {}
                relativeInnerDiv = relativeDiv.div.div
                relativeDataPointDictionary["relativeName"] = relativeInnerDiv.span.a.string
                relativeDataPointDictionary["relativeVoterRecordURL"] = relativeInnerDiv.span.a['href']
                relativeDataPointDictionary["relativeCity"] = relativeInnerDiv.find_all('span')[2].string
                relativeDataPointDictionary["relativeState"] = relativeInnerDiv.find_all('span')[3].string
                for dataPointLabelTag in relativeInnerDiv.find_all('strong'):
                    dataPointLabel = dataPointLabelTag.string.strip()[:-1]
                    dataPoint = ""
                    if "Gender" in dataPointLabel:
                        dataPoint = dataPointLabelTag.next_sibling.string
                    elif "Party Affiliation" in dataPointLabel:
                        dataPoint = dataPointLabelTag.next_sibling.next_sibling.string
                    else:
                        dataPoint = dataPointLabelTag.next_sibling
                    relativeDataPointDictionary[dataPointLabel] = dataPoint
                studentRelatives.append(relativeDataPointDictionary)
            studentRelativeVoterRecord = StudentRelativeVoterRecord(
                student_no=StudentRelativeResult.student_no,
                firstname=StudentRelativeResult.firstname,
                middlename=StudentRelativeResult.middlename,
                lastname=StudentRelativeResult.lastname,
                school=StudentRelativeResult.school,
                cohort=StudentRelativeResult.cohort,
                city=StudentResult.city,
                state=StudentResult.state,
                studentRelativeName=StudentRelativeResult.resultName,
                # From Overview Table:
                Livesin=dataPointDictionary['Livesin']
                    if 'Livesin' in dataPointDictionary else None,
                Age=dataPointDictionary['Age']
                    if 'Age' in dataPointDictionary else None,
                Gender=dataPointDictionary['Gender']
                    if 'Gender' in dataPointDictionary else None,
                Race=dataPointDictionary['Race']
                    if 'Race' in dataPointDictionary else None,
                # From Voter Registration Table:
                PartyAffiliation=dataPointDictionary['PartyAffiliation']
                    if 'PartyAffiliation' in dataPointDictionary else None,
                RegisteredtoVoteIn=dataPointDictionary['RegisteredtoVoteIn']
                    if 'RegisteredtoVoteIn' in dataPointDictionary else None,
                RegistrationDate=dataPointDictionary['RegistrationDate']
                    if 'RegistrationDate' in dataPointDictionary else None,
                VoterStatus=dataPointDictionary['VoterStatus']
                    if 'VoterStatus' in dataPointDictionary else None,
                StatusReason=dataPointDictionary['StatusReason']
                    if 'StatusReason' in dataPointDictionary else None,
                Precinct=dataPointDictionary['Precinct']
                    if 'Precinct' in dataPointDictionary else None,
                PrecinctSplit=dataPointDictionary['PrecinctSplit']
                    if 'PrecinctSplit' in dataPointDictionary else None,
                Ward=dataPointDictionary['Ward']
                    if 'Ward' in dataPointDictionary else None,
                CongressionalDistrict=dataPointDictionary['CongressionalDistrict']
                    if 'CongressionalDistrict' in dataPointDictionary else None,
                HouseDistrict=dataPointDictionary['HouseDistrict']
                    if 'HouseDistrict' in dataPointDictionary else None,
                SenateDistrict=dataPointDictionary['SenateDistrict']
                    if 'SenateDistrict' in dataPointDictionary else None,
                CountyDistrict=dataPointDictionary['CountyDistrict']
                    if 'CountyDistrict' in dataPointDictionary else None,
                SchoolBoardDistrict=dataPointDictionary['SchoolBoardDistrict']
                    if 'SchoolBoardDistrict' in dataPointDictionary else None
                # ... For All Key Fields in the Student's/Student's Relative's Voter Registration
                # Saved from Voter Record Page into DataPointDictionary
            )
            print(studentRelativeVoterRecord)
            StudentRelativeVoterRecords.append(studentRelativeVoterRecord)
            sleep(randint(20,25))
        StudentRelativeVoterRecord_DF = pd.DataFrame(data=StudentRelativeVoterRecords)
        with pd.ExcelWriter(os.path.join(root, 'VoterRegistrationData', file),
                            mode='a') as writer:
            StudentRelativeVoterRecord_DF.to_excel(writer, sheet_name='StudentRelativeVoterRegistrationData')
