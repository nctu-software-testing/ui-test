#!/usr/bin/python3
# coding: utf-8
import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WEBDRIVER_PATH = '/home/jhcheng/ui-test/chromedriver'
TARGET = "http://127.0.0.1:8000"
admin_addr = "admin"
admin_pwd = "admin"
custo_addr = "c"
custo_pwd = "c"
bm_addr = "b"
bm_pwd = "b"
# 20% 10% off, no discount
discount_20_code = "5F08-C0F0-0180-DB00"
discount_10_code = "590F-10E0-1260-B00B"
discount_no_code = "XXXX-YYYY-ZZZZ-AAAA"

# for location
location_address = '大學路1001號'

class UiTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        # options.add_argument('--shm-size=8g')
        options.add_argument('--disable-dev-shm-usage')
        # options.binary_location = CHROME_BINARY_LOCATION
        self.driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH, options=options)
        self.driver.implicitly_wait(30) 

    def tearDown(self):
        self.driver.quit()

    def login(self, acc=admin_addr, pwd=admin_pwd):
        driver = self.driver
        driver.get(TARGET)
        
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="navbar-static-login"]/span')[0])
        driver.find_element_by_name("account").send_keys(acc)
        driver.find_element_by_name("password").send_keys(pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        sleep(3)

    # TC 00- simple test
    def test_print_title(self):
        self.driver.get(TARGET)
        print(self.driver.title)
        self.assertEqual(self.driver.title, "Any Buy 任購網")

    # TC 01- Verify that the login state is correct.
    def test_login(self):
        driver = self.driver
        driver.get(TARGET)
        sleep(3)
        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "navbar-static-login"))
        # )        
        button_elem = driver.find_elements_by_xpath('//*[@id="navbar-static-login"]/span')[0]
        driver.execute_script("arguments[0].click();", button_elem)

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

        sleep(3)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="navbarSupportedContent"]/div[2]/div/div[2]/div/button')[0])
        button_text = driver.find_element_by_xpath('//*[@id="navbar-static-login"]/span').text
        self.assertEqual(button_text, "登入")

    # TC 02- Verify that clicking on add shopping cart button is correct.
    def test_put_in_shopping_cart(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET)
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="category-wrap"]/div/a[1]/div/i')[0])
        # select product
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

    # TC 03- Verify that clicking on clear button must to clear shopping cart.
    def test_clear_shopping_cart(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'/products/item/63')
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])

        driver.get(TARGET+'/shopping-cart')
        expect_column_count = 5
        actual_column_count = len(driver.find_elements_by_xpath("/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td"))
        self.assertEqual(actual_column_count, expect_column_count)

        # clear shopping cart
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div/div/div[1]/div[2]/button')[0])
        sleep(1)
        driver.switch_to.alert.accept() 
        sleep(3)

        expect_column_count = 1
        actual_column_count = len(driver.find_elements_by_xpath("/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td"))
        self.assertEqual(actual_column_count, expect_column_count)

    # TC 04- Verify that modifying the number of product.
    def test_modify_number_of_product(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'')
        driver.get(TARGET+'/products/item/63')
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])
        
        driver.get(TARGET+'/shopping-cart')
        # get number of product before modify
        origin_number = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td[3]').text
        self.assertEqual("1", origin_number)
        # click modify
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td[5]/button[1]')[0])
        sleep(1)
        # type new number
        new_number = 5
        alert_obj = driver.switch_to.alert
        alert_obj.send_keys(str(new_number))
        alert_obj.accept()
        # wait for update
        sleep(3)
        # get number of product before modify
        after_modift_number = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div[2]/form/div[1]/div/table/tbody/tr/td[3]').text
        self.assertEqual(after_modift_number, str(new_number))        
    
    # TC 05- Verify that buying a product successfully.
    def test_buy_product(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'')
        driver.get(TARGET+'/products/item/63')
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])
        
        driver.get(TARGET+'/shopping-cart')
        # click go to order info
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="checkout_info"]/div[2]/button')[0])
        product_name = driver.find_element_by_xpath('/html/body/main/div/div/form/div[1]/div[1]/table/tbody/tr[1]/td[1]/a').text
        number_of_product = int(driver.find_element_by_xpath('/html/body/main/div/div/form/div[1]/div[1]/table/tbody/tr[1]/td[3]').text)
        # click place the order
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/form/div[1]/div[2]/button')[0])
        # go to check order
        driver.get(TARGET+'/order')
        # click first order
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/a')[0])
        product_name_order = driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/table/tbody/tr/td[2]/a').text
        number_of_product_order = int(driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/table/tbody/tr/td[4]').text)
        self.assertEqual(product_name_order, product_name)
        self.assertEqual(number_of_product_order, number_of_product)

    # TC 06- Verify that discount state is correct.
    def test_discount_code(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'')
        driver.get(TARGET+'/products/item/63')
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[2]/div/div[3]/button')[0])
        
        driver.get(TARGET+'/shopping-cart')
        # type 20% off code 
        driver.find_element_by_xpath('//*[@id="discount"]').send_keys(discount_20_code)
        # click finish
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="discountBtn"]')[0])
        sleep(3)
        # assert discount correct
        price = int((driver.find_element_by_xpath('//*[@id="checkout_info"]/div[1]/table/tbody/tr[1]/td[2]/h5').text)[2:])
        discount_price = int((driver.find_element_by_xpath('//*[@id="discountValue"]').text))
        self.assertEqual(discount_price, int(price*(-0.2)))

        # type wrong code 
        driver.find_element_by_xpath('//*[@id="discount"]').send_keys(discount_no_code)
        # click finish
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="discountBtn"]')[0])
        sleep(3)
        # assert discount correct
        discount_price = int(driver.find_element_by_xpath('//*[@id="discountValue"]').text)
        self.assertEqual(discount_price, 0)


    # TC 07- Verify that updating the email. 
    def test_update_email(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'/profile')
        
        # click modify button
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/main/div/div/div[2]/div/div/div/div/ul/li[5]/span[2]/a')[0])
        sleep(3)
        # type email
        email = "asdf@gzxcv.qwer"
        driver.find_element_by_xpath('//*[@id="emailInput"]').send_keys(email)
        # click confirm ## xpath of this button may change!
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('/html/body/div[7]/div/div/div[2]/form/div[2]/button')[0])
        
        # get new profile email
        profile_email = (driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/div/div/ul/li[5]/span[2]').text).split(' ')[0]
        self.assertEqual(profile_email, email)

    # TC 08- Verify that adding a new customer address.
    def test_add_address(self):
        self.login(custo_addr, custo_pwd)
        driver = self.driver
        driver.get(TARGET+'/location')

        # click add address button
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="newlocation"]')[0])
        city_ele = driver.find_element_by_xpath('//*[@id="twzipcode"]/div[1]/input')
        area_ele = driver.find_element_by_xpath('//*[@id="twzipcode"]/div[2]/input')
        address_ele = driver.find_element_by_xpath('//*[@id="lo"]/form/input[1]')
        for i in range(5):
            city_ele.send_keys(Keys.DOWN)
        city_ele.send_keys(Keys.RETURN)
        address_ele.send_keys(location_address)
        
        # click save
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath('//*[@id="lo"]/form/button[1]')[0])

        # get last address
        last_index = len(driver.find_elements_by_xpath("/html/body/main/div/div/div[2]/div/div/table/tbody/tr"))
        last_address = driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/table/tbody/tr['+ str(last_index) +']/td[2]').text

        # check        
        self.assertEqual(last_address, location_address)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
