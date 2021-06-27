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

US_StateAbbreviationLookUp = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'
for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    if os.path.isfile(fullFilePath):
        df = pd.read_excel(fullFilePath)
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
                cityState = student.city.replace(" ","+") + "-" + US_StateAbbreviationLookUp[student.state]
                if student.middlename.strip():
                    queryString = f"{cityState}/{student.firstname}+{student.middlename}+{student.lastname}"
                else:
                    queryString = f"{cityState}/{student.firstname}+{student.lastname}"
            elif student.middlename.strip():
                queryString = f"{student.firstname}-{student.middlename}-{student.lastname}"
            driver.get(f"https://voterrecords.com/voters/{queryString}/1")
            if not os.path.isdir(f"./HTML/{school}/{year}"):
                if not os.path.isdir(f"./HTML/{school}"):
                    os.mkdir(f"./HTML/{school}")
                os.mkdir(f"./HTML/{school}/{year}")
            with open(f"./HTML/{school}/{year}/{student.student_no}_{student.firstname}_{student.lastname}.html", "w") as f:
                f.write(driver.page_source)
            sleep(randint(20,25))

# df.to_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Relatives')
