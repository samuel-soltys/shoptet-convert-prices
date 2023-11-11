# open URL https://616551.myshoptet.com/admin/ with Selenium library and enter login. Use the Chrome browser, the driver is located in the home ~ directory
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
email = os.environ['EMAIL']
password = os.environ['PASSWORD']

driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome(executable_path="~/chromedriver")

driver.get("https://616551.myshoptet.com/admin/")

time.sleep(1)
username = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[1]/input')
# username.clear()
username.send_keys(str(email))

password = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[2]/input')
# password.clear()
password.send_keys(str(password))
password.send_keys(Keys.RETURN)

driver.get("https://616551.myshoptet.com/admin/ceny/?from=2")

for i in range(1, 51):
    try:
        input = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{i}]/td[6]/div/div/input')
        value = input.get_attribute('value')
        # replace , with .
        value = value.replace(",", ".")
        if value != "":
            input.clear()
            
            # insert new value to the input. the new value is the old value * 24.415 , round to whole number
            input.send_keys(round(float(value) * 24.415))
            time.sleep(0.05)
    except NoSuchElementException:
        pass
        

# time.sleep(20)
# make the same process as above but replace the xpath td[6] with td[8] to change the second price
for i in range(1, 51):
    try:
        input = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{i}]/td[8]/div/div/input')
        value = input.get_attribute('value')
        if value != "":
            value = value.replace(",", ".")
            input.clear()
            input.send_keys(round(float(value) * 24.415))
            time.sleep(0.05)
    except NoSuchElementException:
        pass

time.sleep(30)
driver.quit()