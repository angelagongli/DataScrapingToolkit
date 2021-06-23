import pandas as pd

df = pd.read_excel('C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists\\Amherst_College_2004_clean.xlsx', sheet_name='Sheet1')
print(df)

from selenium import webdriver

driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe')
driver.get("https://voterrecords.com/voters/angela-li/1")
with open("./HTML/Angela_Li.html", "w") as f:
    f.write(driver.page_source)
