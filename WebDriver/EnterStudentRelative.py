from selenium import webdriver

driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe')
driver.get("https://voterrecords.com/voters/yinquan-li/")
with open("./HTML/Yinquan_Li.html", "w") as f:
    f.write(driver.page_source)
