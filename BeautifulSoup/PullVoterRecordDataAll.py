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
# pull_studentrelativeresults = ("SELECT id, student_id, relativeResultName, relativeResultVoterRecordURL FROM StudentRelativeResults "
#                     "WHERE student_id<=100 AND identificationStep='Identified'")

insert_voterrecord = ("INSERT INTO VoterRecords "
    "(student_id, studentRelative_id, partyAffiliation, registeredToVoteIn, "
    "registrationDate, voterStatus, statusReason, precinct, "
    "precinctSplit, ward, congressionalDistrict, houseDistrict, "
    "senateDistrict, countyDistrict, schoolBoardDistrict, voterRecordType) "
    "VALUES (%(student_id)s, %(studentRelative_id)s, %(partyAffiliation)s, %(registeredToVoteIn)s, "
    "%(registrationDate)s, %(voterStatus)s, %(statusReason)s, %(precinct)s, "
    "%(precinctSplit)s, %(ward)s, %(congressionalDistrict)s, %(houseDistrict)s, "
    "%(senateDistrict)s, %(countyDistrict)s, %(schoolBoardDistrict)s, %(voterRecordType)s)")

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
    cnx.commit()
    sleep(randint(20,25))

innerCursor.close()
outerCursor.close()
cnx.close()
