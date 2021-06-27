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

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'
for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    if os.path.isfile(fullFilePath):
        df = pd.read_excel(fullFilePath, sheet_name='Sheet1')
        for student in df.itertuples(name='Student'):
            print(student.name + " is from " + student.city)
            if student.middlename.strip():
                driver.get(f"https://voterrecords.com/voters/{student.firstname}-{student.middlename}-{student.lastname}")
                if not os.path.isdir(f"./HTML/{student.school}/{student.cohort_yr}"):
                    if not os.path.isdir(f"./HTML/{student.school}"):
                        os.mkdir(f"./HTML/{student.school}")
                    os.mkdir(f"./HTML/{student.school}/{student.cohort_yr}")
                with open(f"./HTML/{student.school}/{student.cohort_yr}/{student.firstname}_{student.middlename}_{student.lastname}.html", "w") as f:
                    f.write(driver.page_source)
            else:
                driver.get(f"https://voterrecords.com/voters/{student.firstname}-{student.lastname}")
                with open(f"./HTML/{student.school}/{student.cohort_yr}/{student.firstname}_{student.lastname}.html", "w") as f:
                    f.write(driver.page_source)
            sleep(randint(20,25))

# df.to_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Relatives')
