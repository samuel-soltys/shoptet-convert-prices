# Imports
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

# Load and access environment variables from .env file
load_dotenv()
email = str(os.environ['EMAIL'])
passw = str(os.environ['PASSWORD'])

# Webdriver setup
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", options=chrome_options) #
driver.get("https://organic-oasis.cz/admin/")
time.sleep(0.5)

# Entering the login credentials
username = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[1]/input')
username.send_keys(email)
password = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[2]/input')
password.send_keys(passw)
password.send_keys(Keys.RETURN)

driver.get(f"https://www.organic-oasis.cz/admin/produkty-detail/?id=489") # product

time.sleep(3)
b = driver.find_element(By.XPATH, '//*[@id="ui-id-2"]')
b.click()

# Changing the price column = 6 is for the price column and 8 is for the standard price column
for row in range(296, 513):
    dph_field = driver.find_element(By.XPATH, f'//*[@id="variant-product"]/div[2]/table/tbody/tr[{row}]/td[4]/div/div/select')
    select = Select(dph_field)
    select.select_by_value("1:1")
    print(f"Changed {row} DPH value")

button = driver.find_element(By.XPATH, '//*[@id="main-form"]/div[1]/p/a[2]')
button.click()

# Time to save and check the changes in Shoptet admin
time.sleep(15)
# driver.quit()