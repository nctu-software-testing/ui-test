from selenium.webdriver.chrome.options import Options
from selenium import webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/home/jhcheng/108_2_UI_Testing/venv/bin/chromedriver', chrome_options=chrome_options)
driver.get('http://christopher.su')
print(driver.title)