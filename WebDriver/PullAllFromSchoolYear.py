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
import pandas as pd
import os
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import collections

US_StateAbbreviationLookUp = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'AMERICAN SAMOA': 'AS',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'DISTRICT OF COLUMBIA': 'DC',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'GUAM': 'GU',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'NORTHERN MARIANA ISLANDS':'MP',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'PUERTO RICO': 'PR',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGIN ISLANDS': 'VI',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY'
}

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'
for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    if os.path.isfile(fullFilePath):
        df = pd.read_excel(fullFilePath)
        # Menaka wants Name Entered and Name Returned for every student, as well as
        # All the rest of the student's information entered into the URL returning the
        # StudentResult kept together with the result data itself in the StudentResult record
        StudentResult = collections.namedtuple('StudentResult',
            ['student_no', 'firstname', 'middlename', 'lastname',
            'school', 'cohort', 'city', 'state', 'resultName', 'resultAge',
            'resultCity', 'resultCityHistory', 'resultType', 'resultData'])
        StudentResults = []
        for student in df.itertuples(name='Student'):
            school = student.school
            year = ""
            if hasattr(student, "cohort"):
                year = student.cohort
            elif hasattr(student, "cohort_yr"):
                year = student.cohort_yr
            cityState = ""
            queryString = ""
            if hasattr(student, "city") and student.country.upper() == "UNITED STATES":
                nameString = f"{student.firstname}+{student.middlename}+{student.lastname}"
                if not student.middlename.strip():
                    nameString = f"{student.firstname}+{student.lastname}"
                if "-" in student.name:
                    nameString = nameString.replace("-", "+")
                cityState = student.city.replace(" ","+") + "-" + (US_StateAbbreviationLookUp[student.state.upper()]
                    if student.state.upper() in US_StateAbbreviationLookUp.keys() else student.state.upper())
                queryString = f"{cityState}/{nameString}"
            elif student.middlename.strip():
                queryString = f"{student.firstname}-{student.middlename}-{student.lastname}"
            else:
                queryString = f"{student.firstname}-{student.lastname}"
            driver.get(f"https://voterrecords.com/voters/{queryString}/1")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            header = soup.find(attrs={"class":"BottomMargin10 TopH1"}).contents[1]
            headerRegex = re.compile("( has) ([\d|,]+) Voter Record")
            headerRegexMatch = headerRegex.match(header)
            voterRecordNumber = headerRegexMatch.group(2)
            if voterRecordNumber == "0":
                print("Pulling Student's Relative Data from TruthFinder...")
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
                    cursor = link.parent.find_previous_sibling()
                    for relative in cursor.contents:
                        if isinstance(relative, NavigableString) and relative.strip():
                            relativeString += relative.strip() + "*"
                    cursor = cursor.find_previous_sibling()
                    for city in cursor.contents:
                        if isinstance(city, NavigableString) and city.strip():
                            cityString += city.strip() + "*"
                    cursor = cursor.find_previous_sibling()
                    resultName = cursor.h4.get_text()
                    resultAge = ""
                    if "(" in resultName:
                        resultNameAge = resultName.split(" (")
                        resultName = resultNameAge[0]
                        resultAge = resultNameAge[1].replace(")","")
                    resultCity = cursor.p.string
                    if hasattr(student, "city"):
                        studentResult = StudentResult(student.student_no,
                            student.firstname, student.middlename, student.lastname,
                            school, year, student.city, student.state, resultName, resultAge,
                            resultCity, cityString, 'Relatives', relativeString)
                    else:
                        studentResult = StudentResult(student.student_no,
                            student.firstname, student.middlename, student.lastname,
                            school, year, None, None, resultName, resultAge,
                            resultCity, cityString, 'Relatives', relativeString)
                    StudentResults.append(studentResult)
            else:
                print("Pulling All from First Page...")
                for person in soup.find_all('tr'):
                    if person.find_next().name == "th":
                        print("Header")
                        continue
                    # In the early stage of entering the Student/pulling the StudentResult,
                    # Only scrape the data required to identify the student we want
                    cursor = person.find_next()
                    resultName = cursor.span.span.a.get_text().strip()
                    # We can start narrowing the StudentResult set right now at the point
                    # When everything is still only on the page, saving only when the person's
                    # Name exactly matches the student's first name/last name. We can save
                    # Everything for the sake of completeness/documentation of the process as well
                    # But for e.g. the married student with a new surname since college, if we
                    # Save her as well hoping to correctly identify her downstream in our process,
                    # Keep in mind we will still rule her out based on her name further on in our process
                    if not (student.firstname.upper() in resultName.upper() and
                    student.lastname.upper() in resultName.upper()):
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
                    if hasattr(student, "city"):
                        studentResult = StudentResult(student.student_no,
                            student.firstname, student.middlename, student.lastname,
                            school, year, student.city, student.state, resultName, resultAge,
                            resultCity, resultCity, 'StudentVoterRecord', resultVoterRecordURL)
                    else:
                        studentResult = StudentResult(student.student_no,
                            student.firstname, student.middlename, student.lastname,
                            school, year, None, None, resultName, resultAge,
                            resultCity, resultCity, 'StudentVoterRecord', resultVoterRecordURL)
                    StudentResults.append(studentResult)
            sleep(randint(20,25))
        StudentResult_DF = pd.DataFrame(data=StudentResults)
        if not os.path.isdir(os.path.join(root, 'StudentResults')):
            os.mkdir(os.path.join(root, 'StudentResults'))
        StudentResult_DF.to_excel(os.path.join(root, 'StudentResults', file), sheet_name='StudentResults')

# Menaka's Dataset Design: Unique ID of Student Record in Whole Dataset
# Is the Composite Key of (student_no, school, cohort/cohort_yr)
# TODO: Handle voterrecords.com's Listing of the Middle Initial/Middle Name
# TODO: Handle Pagination: How much does Menaka want to scrape for every student?
# df.to_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Relatives')
