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
        StudentResult = collections.namedtuple('StudentResult',
            ['student_no', 'firstname', 'middlename', 'lastname',
            'school', 'cohort', 'resultType', 'resultData'])
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
                cityState = student.city.replace(" ","+") + "-" + US_StateAbbreviationLookUp[student.state.upper()]
                if student.middlename.strip():
                    queryString = f"{cityState}/{student.firstname}+{student.middlename}+{student.lastname}"
                else:
                    queryString = f"{cityState}/{student.firstname}+{student.lastname}"
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
                print("Pull Student's Relative Data from TruthFinder:")
                for link in soup.find_all('a', string="That's The One!"):
                    relativeString = ""
                    for relative in link.parent.find_previous_sibling().contents:
                        if isinstance(relative, NavigableString) and relative.strip():
                            relativeString += relative.strip() + ","
                    studentResult = StudentResult(student.student_no,
                        student.firstname, student.middlename, student.lastname,
                        school, year, 'Relatives', relativeString)
                    StudentResults.append(studentResult)
            else:
                print("Pull All from First Page:")
            sleep(randint(20,25))

# Menaka's Dataset Design: Unique ID of Student Record in Whole Dataset
# Is the Composite Key of (student_no, school, cohort/cohort_yr)
# TODO: Handle Hyphenated Name When Querystring Delimiter Is "+"
# TODO: Handle voterrecords.com's Listing of the Middle Initial/Middle Name
# df.to_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Relatives')
