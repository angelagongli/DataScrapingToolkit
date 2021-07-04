from bs4 import BeautifulSoup
import collections

with open("C:\\Users\\angel\\GitHub\\DataScrapingToolkit\\HTML\\StudentID_VoterRecord.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

# Menaka wants everything in the Overview table: City, Age, Gender and Race
# But there is no need to duplicate everything present in the saved StudentResult
# => Only useful for the StudentRelative: Make sure to keep Student/StudentRelative
# Clearly identified in the dataset all the way through

dataPointDictionary = {}
StudentVoterRecord = collections.namedtuple('StudentVoterRecord',
    # All Kept from StudentResult:
    ['student_no', 'firstname', 'middlename', 'lastname',
    'school', 'cohort', 'resultName', 'resultAge', 'resultCity',
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
    'student_no', 'firstname', 'middlename', 'lastname',
    'school', 'cohort',
    # Rest of Data Saved in Student's Relative Voter Record Is Purely Voter Registration Data
    'PartyAffiliation','RegisteredtoVoteIn','RegistrationDate','VoterStatus',
    'StatusReason','Precinct','PrecinctSplit','Ward','CongressionalDistrict',
    'HouseDistrict','SenateDistrict','CountyDistrict','SchoolBoardDistrict'])

for tableColumn in soup.find(id="overview").find_all('div') + \
    soup.find(id="voter-registration").find_all('div'):
    for label in tableColumn.find_all('strong'):
        labelString = label.string.replace(":","").replace(" ","").strip()
        dataTag = label.find_next_sibling()
        dataPoint = ""
        if dataTag.name == "br":
            dataPoint = label.next_element.next_element
        else:
            dataPoint = dataTag.string
        dataPointDictionary[labelString] = dataPoint

StudentVoterRecord = StudentVoterRecord(
    student_no='student_no',
    firstname='firstname',
    middlename='middlename',
    lastname='lastname',
    school='school',
    cohort='cohort',
    resultName='resultName',
    resultAge='resultAge',
    resultCity='resultCity',
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
print(StudentVoterRecord)
