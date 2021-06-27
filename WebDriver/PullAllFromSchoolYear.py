from selenium import webdriver

driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe')

import pandas as pd
import os

df = pd.read_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Sheet1')
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

# df.to_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Relatives')
