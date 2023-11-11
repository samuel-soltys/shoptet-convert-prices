# Imports
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load and access environment variables from .env file
load_dotenv()
email = str(os.environ['EMAIL'])
passw = str(os.environ['PASSWORD'])

# Webdriver setup
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://616551.myshoptet.com/admin/")
time.sleep(0.5)

# Entering the login credentials
username = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[1]/input')
username.send_keys(email)
password = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[2]/input')
password.send_keys(passw)
password.send_keys(Keys.RETURN)

driver.get("https://616551.myshoptet.com/admin/ceny/") # add ?from=2 to the end of the URL to begin from the second page

# Changing the price column = 6 is for the price column and 8 is for the standard price column
for column in [6, 8]:
    for row in range(1, 51):
        try:
            input = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{row}]/td[{column}]/div/div/input')
            value = input.get_attribute('value')
            value = value.replace(",", ".")

            if value != "":
                # Convert the price from EUR to CZK
                input.clear()
                input.send_keys(round(float(value) * 24.415))
                time.sleep(0.05)
        except NoSuchElementException:
            pass

# Time to save and check the changes in Shoptet admin
time.sleep(10)
driver.quit()