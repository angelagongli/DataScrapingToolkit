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
import re
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='Student_DB')
outerCursor = cnx.cursor(buffered=True)
innerCursor = cnx.cursor(buffered=True)

school = "AMHERST COLLEGE"
year = 2004

pull_schoolyear = ("SELECT id, firstName, middleName, lastName, "
                    "city, state, country FROM Students "
                    "WHERE school=%s AND cohort=%s")

insert_studentresult = ("INSERT INTO StudentResults "
    "(student_id, resultName, resultAge, resultCity, "
    "resultCityHistory, resultType, resultData) "
    "VALUES (%(student_id)s, %(resultName)s, %(resultAge)s, %(resultCity)s, "
    "%(resultCityHistory)s, %(resultType)s, %(resultData)s)")

outerCursor.execute(pull_schoolyear, (school, year))

for (id, firstName, middleName, lastName, city, state, country) in outerCursor:
    StudentResults = []
    cityState = ""
    queryString = ""
    if city and state and len(state) == 2:
        nameString = f"{firstName}+{middleName}+{lastName}"
        if not middleName:
            nameString = f"{firstName}+{lastName}"
        if "-" in nameString:
            nameString = nameString.replace("-", "+")
        cityState = city.replace(" ","+") + "-" + state
        queryString = f"{cityState}/{nameString}"
    elif middleName:
        queryString = f"{firstName}-{middleName}-{lastName}"
    else:
        queryString = f"{firstName}-{lastName}"
    driver.get(f"https://voterrecords.com/voters/{queryString}/1")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    header = soup.find(attrs={"class":"BottomMargin10 TopH1"}).contents[1]
    headerRegex = re.compile("( has) ([\d|,]+) Voter Record")
    headerRegexMatch = headerRegex.match(header)
    voterRecordNumber = headerRegexMatch.group(2)
    if voterRecordNumber == "0":
        print(f"Pulling {firstName} {lastName}'s Relative Data from TruthFinder...")
        # TO ASK Question for Menaka: How does Menaka hope to study the relationship between the
        # Student's major choice and political beliefs, here adding as well the dimension of the
        # Student's family's political beliefs to her main research question, when
        # We do not have the most crucial piece of data, the Student's Voter Record?
        # How then can it be helpful to scrape the additional information of the Student's
        # Relative's voter registration data when we cannot be analyzing it vis-a-vis
        # Our main data point that the student's family's political belief component would
        # Hopefully just shed additional light upon?
        for link in soup.find_all('a', string="That's The One!"):
            relativeString = ""
            cityString = ""
            driverCursor = link.parent.find_previous_sibling()
            for relative in driverCursor.contents:
                if isinstance(relative, NavigableString) and relative.strip():
                    relativeString += relative.strip() + "*"
            if not relativeString:
                continue
            driverCursor = driverCursor.find_previous_sibling()
            for city in driverCursor.contents:
                if isinstance(city, NavigableString) and city.strip():
                    cityString += city.strip() + "*"
            driverCursor = driverCursor.find_previous_sibling()
            resultName = driverCursor.h4.get_text()
            resultAge = ""
            if "(" in resultName:
                resultNameAge = resultName.split(" (")
                resultName = resultNameAge[0]
                resultAge = resultNameAge[1].replace(")","")
            resultCity = str(driverCursor.p.string)
            StudentResult = {
                'student_id': id,
                'resultName': resultName,
                'resultAge': resultAge if resultAge else None,
                'resultCity': resultCity if resultCity else None,
                'resultCityHistory': cityString if cityString else None,
                'resultType': 'StudentRelatives',
                'resultData': relativeString
            }
            StudentResults.append(StudentResult)
    else:
        print(f"Pulling All from {firstName} {lastName}'s First Page...")
        for person in soup.find_all('tr'):
            if person.find_next().name == "th":
                print("Header")
                continue
            # In the early stage of entering the Student/pulling the StudentResult,
            # Only scrape the data required to identify the student we want
            driverCursor = person.find_next()
            resultName = driverCursor.span.span.a.get_text().strip()
            # We can start narrowing the StudentResult set right now at the point
            # When everything is still only on the page, saving only when the person's
            # Name exactly matches the student's first name/last name. We can save
            # Everything for the sake of completeness/documentation of the process as well
            # But for e.g. the married student with a new surname since college, if we
            # Save her as well hoping to correctly identify her downstream in our process,
            # Keep in mind we will still rule her out based on her name further on in our process
            if not (firstName in resultName.upper() and
            lastName in resultName.upper()):
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
            StudentResult = {
                'student_id': id,
                'resultName': resultName,
                'resultAge': resultAge if resultAge else None,
                'resultCity': resultCity if resultCity else None,
                'resultCityHistory': resultCity if resultCity else None,
                'resultType': 'StudentVoterRecord',
                'resultData': resultVoterRecordURL
            }
            StudentResults.append(StudentResult)
    innerCursor.executemany(insert_studentresult, StudentResults)
    cnx.commit()
    sleep(randint(20,25))

innerCursor.close()
outerCursor.close()
cnx.close()
