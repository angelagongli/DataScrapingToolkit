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
    'Party Affiliation', 'Registered to Vote In', 'Registration Date', 'Voter Status',
    'Status Reason', 'Precinct', 'Precinct Split', 'Ward', 'Congressional District',
    'House District', 'Senate District', 'County District', 'School Board District'])
StudentRelativeVoterRecord = collections.namedtuple('StudentRelativeVoterRecord',
    ['studentRelativeName',
    # From Overview Table:
    'Lives in', 'Age', 'Gender', 'Race',
    # All Data Required to Uniquely Identify the Student the Relative Belongs to in
    # Whole Dataset Must Be Kept in Student's Relative Voter Record => Foreign Key
    # Based on the Composite Key
    'student_no', 'firstname', 'middlename', 'lastname',
    'school', 'cohort',
    # Rest of Data Saved in Student's Relative Voter Record Is Purely Voter Registration Data
    'Party Affiliation', 'Registered to Vote In', 'Registration Date', 'Voter Status',
    'Status Reason', 'Precinct', 'Precinct Split', 'Ward', 'Congressional District',
    'House District', 'Senate District', 'County District', 'School Board District'])

for tableColumn in soup.find(id="overview").find_all('div') + \
    soup.find(id="voter-registration").find_all('div'):
    for label in tableColumn.find_all('strong'):
        labelString = label.string.replace(":","").strip()
        dataTag = label.find_next_sibling()
        dataPoint = ""
        if dataTag.name == "br":
            dataPoint = label.next_element.next_element
        else:
            dataPoint = dataTag.string
        dataPointDictionary[labelString] = dataPoint

StudentVoterRecord = StudentVoterRecord(
    RegisteredtoVoteIn=dataPointDictionary['Registered to Vote In'],
    RegistrationDate=dataPointDictionary['Registration Date']
    # ... For All Key Fields in the Student's/Student's Relative's Voter Registration
    # Saved from Voter Record Page into DataPointDictionary
)
print(StudentVoterRecord)
