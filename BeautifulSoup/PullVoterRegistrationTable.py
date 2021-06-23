from bs4 import BeautifulSoup

with open("C:\\Users\\angel\\GitHub\\DataScrapingToolkit\\HTML\\StudentID_VoterRecord.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

for label in soup.find(id="voter-registration").div.find_all('strong'):
    print("Label: " + label.string)
for data_point in soup.find(id="voter-registration").div.find_all('span'):
    print("Data Point: " + data_point.string)
