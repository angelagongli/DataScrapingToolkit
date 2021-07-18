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
from bs4.element import NavigableString
import datetime
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='Student_DB')
outerCursor = cnx.cursor(buffered=True)
innerCursor = cnx.cursor(buffered=True)

# Pull Identified Student/StudentRelative Results
pull_studentresults = ("SELECT id, student_id, resultName, resultData FROM StudentResults "
                    "WHERE student_id<=100 AND resultType='StudentVoterRecord' AND identificationStep='Identified'")
pull_studentrelativeresults = ("SELECT id, student_id, relativeResultName, relativeResultVoterRecordURL FROM StudentRelativeResults "
                    "WHERE student_id<=100 AND identificationStep='Identified'")

insert_voterrecord = ("INSERT INTO VoterRecords "
    "(student_id, studentRelative_id, partyAffiliation, registeredToVoteIn, "
    "registrationDate, voterStatus, statusReason, precinct, "
    "precinctSplit, ward, congressionalDistrict, houseDistrict, "
    "senateDistrict, countyDistrict, schoolBoardDistrict, voterRecordType) "
    "VALUES (%(student_id)s, %(studentRelative_id)s, %(partyAffiliation)s, %(registeredToVoteIn)s, "
    "%(registrationDate)s, %(voterStatus)s, %(statusReason)s, %(precinct)s, "
    "%(precinctSplit)s, %(ward)s, %(congressionalDistrict)s, %(houseDistrict)s, "
    "%(senateDistrict)s, %(countyDistrict)s, %(schoolBoardDistrict)s, %(voterRecordType)s)")
# Keep the fullness of information saved in the StudentRelativeResult sourced from the Student's
# Voter Record even with that of the StudentRelativeResult sourced from the Student's Relatives
# Returned by TruthFinder => We can only fully analyze StudentRelativeResults on the set of characteristics
# Possessed by the whole set of StudentRelativeResults
insert_studentrelativeresult = ("INSERT INTO StudentRelativeResults "
    "(student_id, relativeResultName, relativeResultVoterRecordURL, "
    "relativeResultSource, identificationStep) "
    "VALUES (%(student_id)s, %(relativeResultName)s, %(relativeResultVoterRecordURL)s, "
    "%(relativeResultSource)s, %(identificationStep)s)")

outerCursor.execute(pull_studentresults)

for (id, student_id, resultName, resultData) in outerCursor:
    driver.get(f"https://voterrecords.com{resultData}")
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
                    dataPoint = str(label.next_element.next_element)
                else:
                    dataPoint = dataTag.get_text()
            dataPointDictionary[labelString] = dataPoint
    StudentVoterRecord = {
        'student_id': student_id,
        'studentRelative_id': None,
        # From Voter Registration Table:
        'partyAffiliation': dataPointDictionary['PartyAffiliation']
            if 'PartyAffiliation' in dataPointDictionary else None,
        'registeredToVoteIn': dataPointDictionary['RegisteredtoVoteIn']
            if 'RegisteredtoVoteIn' in dataPointDictionary else None,
        'registrationDate': datetime.date(int(dataPointDictionary['RegistrationDate'][-4:]),
            int(dataPointDictionary['RegistrationDate'][0:2]),
            int(dataPointDictionary['RegistrationDate'][3:5]))
            if 'RegistrationDate' in dataPointDictionary else None,
        'voterStatus': dataPointDictionary['VoterStatus']
            if 'VoterStatus' in dataPointDictionary else None,
        'statusReason': dataPointDictionary['StatusReason']
            if 'StatusReason' in dataPointDictionary else None,
        'precinct': dataPointDictionary['Precinct']
            if 'Precinct' in dataPointDictionary else None,
        'precinctSplit': dataPointDictionary['PrecinctSplit']
            if 'PrecinctSplit' in dataPointDictionary else None,
        'ward': dataPointDictionary['Ward']
            if 'Ward' in dataPointDictionary else None,
        'congressionalDistrict': dataPointDictionary['CongressionalDistrict']
            if 'CongressionalDistrict' in dataPointDictionary else None,
        'houseDistrict': dataPointDictionary['HouseDistrict']
            if 'HouseDistrict' in dataPointDictionary else None,
        'senateDistrict': dataPointDictionary['SenateDistrict']
            if 'SenateDistrict' in dataPointDictionary else None,
        'countyDistrict': dataPointDictionary['CountyDistrict']
            if 'CountyDistrict' in dataPointDictionary else None,
        'schoolBoardDistrict': dataPointDictionary['SchoolBoardDistrict']
            if 'SchoolBoardDistrict' in dataPointDictionary else None,
        # ... For All Key Fields in the Student's/Student's Relative's Voter Registration
        # Saved from Voter Record Page into DataPointDictionary
        'voterRecordType': 'StudentVoterRecord'
    }
    innerCursor.execute(insert_voterrecord, StudentVoterRecord)
    StudentRelativeResults = []
    # Menaka has brought up the Related Records table of the Student's Voter Record page as well =>
    # How do we verify the accuracy of the Student's Relative designation? Here we have not only the
    # Designated Student's Relative's name but his/her full voter record as well, we are going based
    # Entirely on the site's own algorithm but we can save the full voter record of all of the Student's
    # Relatives returned in the Student's Voter Record per Menaka's request
    for relativeDiv in soup.find(id="related-voters").div:
        if isinstance(relativeDiv, NavigableString):
            continue
        relativeDataPointDictionary = {}
        relativeInnerDiv = relativeDiv.div.div
        relativeDataPointDictionary["relativeName"] = relativeInnerDiv.span.a.get_text()
        relativeDataPointDictionary["relativeVoterRecordURL"] = relativeInnerDiv.span.a['href']
        relativeDataPointDictionary["relativeCity"] = relativeInnerDiv.find_all('span')[2].get_text()
        relativeDataPointDictionary["relativeState"] = relativeInnerDiv.find_all('span')[3].get_text()
        for dataPointLabelTag in relativeInnerDiv.find_all('strong'):
            dataPointLabel = dataPointLabelTag.string.strip()[:-1]
            dataPoint = ""
            if "Gender" in dataPointLabel:
                dataPoint = dataPointLabelTag.next_sibling.get_text()
            elif "Party Affiliation" in dataPointLabel:
                dataPoint = dataPointLabelTag.next_sibling.next_sibling.get_text()
            else:
                dataPoint = str(dataPointLabelTag.next_sibling)
            relativeDataPointDictionary[dataPointLabel] = dataPoint
        # Keep the fullness of information saved in the StudentRelativeResult sourced from the Student's
        # Voter Record even with that of the StudentRelativeResult sourced from the Student's Relatives
        # Returned by TruthFinder => We can only fully analyze StudentRelativeResults on the set of characteristics
        # Possessed by the whole set of StudentRelativeResults
        StudentRelativeResult = {
            'student_id': student_id,
            'relativeResultName': relativeDataPointDictionary['relativeName'],
            'relativeResultVoterRecordURL': relativeDataPointDictionary['relativeVoterRecordURL'],
            'relativeResultSource': 'StudentVoterRecord',
            # We save the set of designated Student's Relatives from the Student's Voter Record
            # Per Menaka's request => We will just have to trust the goodness of the site's own algorithm
            'identificationStep': 'Identified'
        }
        StudentRelativeResults.append(StudentRelativeResult)
    innerCursor.executemany(insert_studentrelativeresult, StudentRelativeResults)
    cnx.commit()
    sleep(randint(20,25))

outerCursor.execute(pull_studentrelativeresults)

for (id, student_id, relativeResultName, relativeResultVoterRecordURL) in outerCursor:
    driver.get(f"https://voterrecords.com{relativeResultVoterRecordURL}")
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
                    dataPoint = str(label.next_element.next_element)
                else:
                    dataPoint = dataTag.get_text()
            dataPointDictionary[labelString] = dataPoint
    StudentRelativeVoterRecord = {
        'student_id': student_id,
        'studentRelative_id': id,
        # From Voter Registration Table:
        'partyAffiliation': dataPointDictionary['PartyAffiliation']
            if 'PartyAffiliation' in dataPointDictionary else None,
        'registeredToVoteIn': dataPointDictionary['RegisteredtoVoteIn']
            if 'RegisteredtoVoteIn' in dataPointDictionary else None,
        'registrationDate': datetime.date(int(dataPointDictionary['RegistrationDate'][-4:]),
            int(dataPointDictionary['RegistrationDate'][0:2]),
            int(dataPointDictionary['RegistrationDate'][3:5]))
            if 'RegistrationDate' in dataPointDictionary else None,
        'voterStatus': dataPointDictionary['VoterStatus']
            if 'VoterStatus' in dataPointDictionary else None,
        'statusReason': dataPointDictionary['StatusReason']
            if 'StatusReason' in dataPointDictionary else None,
        'precinct': dataPointDictionary['Precinct']
            if 'Precinct' in dataPointDictionary else None,
        'precinctSplit': dataPointDictionary['PrecinctSplit']
            if 'PrecinctSplit' in dataPointDictionary else None,
        'ward': dataPointDictionary['Ward']
            if 'Ward' in dataPointDictionary else None,
        'congressionalDistrict': dataPointDictionary['CongressionalDistrict']
            if 'CongressionalDistrict' in dataPointDictionary else None,
        'houseDistrict': dataPointDictionary['HouseDistrict']
            if 'HouseDistrict' in dataPointDictionary else None,
        'senateDistrict': dataPointDictionary['SenateDistrict']
            if 'SenateDistrict' in dataPointDictionary else None,
        'countyDistrict': dataPointDictionary['CountyDistrict']
            if 'CountyDistrict' in dataPointDictionary else None,
        'schoolBoardDistrict': dataPointDictionary['SchoolBoardDistrict']
            if 'SchoolBoardDistrict' in dataPointDictionary else None,
        # ... For All Key Fields in the Student's/Student's Relative's Voter Registration
        # Saved from Voter Record Page into DataPointDictionary
        'voterRecordType': 'StudentRelativeVoterRecord'
    }
    innerCursor.execute(insert_voterrecord, StudentRelativeVoterRecord)
    cnx.commit()
    sleep(randint(20,25))

innerCursor.close()
outerCursor.close()
cnx.close()
