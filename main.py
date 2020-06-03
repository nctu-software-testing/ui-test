#!/home/jhcheng/108_2_UI_Testing/venv/bin/python3
## normal path: /usr/bin/python3
# coding: utf-8
import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CHROME_BINARY_LOCATION = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
WEBDRIVER_PATH = '/home/jhcheng/108_2_UI_Testing/venv/bin/chromedriver'
TARGET = "http://127.0.0.1:8000"
# TARGET = "http://christopher.su"

class UiTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # options.add_argument('--window-size=1920,1080')
        # options.add_argument('--shm-size=8g')
        options.add_argument('--disable-dev-shm-usage')
        # options.binary_location = CHROME_BINARY_LOCATION
        self.driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH, options=options)
        self.driver.implicitly_wait(30) 

    def tearDown(self):
        self.driver.quit()

    def login(self):
        driver = self.driver
        driver.get(TARGET)
        sleep(5)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="navbar-static-login"]/span')[0])
        driver.find_element_by_name("account").send_keys("admin")
        driver.find_element_by_name("password").send_keys("admin")
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        sleep(3)

    def test_login(self):
        driver = self.driver
        driver.get(TARGET)
        sleep(5)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "navbar-static-login"))
        )        
        # print(driver.title)
        button_elem = driver.find_elements_by_xpath('//*[@id="navbar-static-login"]/span')[0]
        # button_elem.click()
        driver.execute_script("arguments[0].click();",button_elem)
        acco_elem = driver.find_element_by_name("account")
        pass_elem = driver.find_element_by_name("password")
        acco_elem.send_keys("!@#$")
        pass_elem.send_keys("!@#$")
        pass_elem.send_keys(Keys.ENTER)    
        sleep(3)
        assert "登入失敗".encode('utf-8').decode('utf-8') in driver.page_source

        acco_elem.clear()
        acco_elem.send_keys("asdf")
        pass_elem.clear()
        pass_elem.send_keys("asdf")
        pass_elem.send_keys(Keys.ENTER)
        assert "登入失敗".encode('utf-8').decode('utf-8') not in driver.page_source

    def test_put_in_shopping_cart(self):
        self.login()
        driver = self.driver
        driver.get(TARGET)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="category-wrap"]/div/a[1]/div/i')[0])
        # select product
        sleep(3)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="products"]/div[2]/a/div[1]/div')[0])
        # click add to shopping cart suceessfully
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])
        sleep(3)
        assert "已加入購物車".encode('utf-8').decode('utf-8') in driver.find_elements_by_xpath('//*[@id="toast-container"]/div[contains(@class, "toast-success")]')[0].text

        driver.get(TARGET)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="category-wrap"]/div/a[1]/div/i')[0])
        # select product
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="products"]/div[1]/a/div[1]/div')[0])
        # click add to shopping cart and failed
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])
        sleep(3)
        assert "沒有庫存了".encode('utf-8').decode('utf-8') in driver.find_elements_by_xpath('//*[@id="toast-container"]/div[contains(@class, "toast-error")]')[0].text    

    def te1st_clear_shopping_cart(self):
        self.login()
        driver = self.driver
        driver.get(TARGET+'/products')
        driver.find_elements_by_xpath('//*[@id="products"]/div[1]/a/div[1]/div')[0].click()
        driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0].click()

        driver.get(TARGET+'/shopping-cart')
        expect_column_count = 5
        actual_column_count = len(driver.find_elements_by_xpath("/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td"))
        self.assertEqual(actual_column_count, expect_column_count)

        # clear shopping cart
        driver.find_elements_by_xpath('/html/body/main/div/div/div/div/div[1]/div[2]/button')[0].click()
        sleep(1)
        driver.switch_to.alert.accept() 
        sleep(3)

        expect_column_count = 1
        actual_column_count = len(driver.find_elements_by_xpath("/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td"))
        self.assertEqual(actual_column_count, expect_column_count)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
