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
# chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", options=chrome_options) #
driver.get("https://organic-oasis.cz/admin/")
time.sleep(0.5)

# Entering the login credentials
username = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[1]/input')
username.send_keys(email)
password = driver.find_element(By.XPATH, '//*[@id="main-form"]/fieldset/label[2]/input')
password.send_keys(passw)
password.send_keys(Keys.RETURN)

codes = {
    "ANTI-STRESSTHERAPY": "773",
    "MICROBIOMETHERAPY": "929",
    "PROBIOWOMANTHERAPY": "926",
    "PROBIOKIDSTHERAPY": "1025",
    "HAPPYSKINTHERAPY": "770",
    "LOVELYHAIRTHERAPY": "1013",
    "PROBIODETOXTHERAPY": "1159",
    "FINEBODYTHERAPY": "1180"
}

driver.get(f"https://www.organic-oasis.cz/admin/produkty-detail/?id=489") # product
time.sleep(10)

# Changing the price column = 6 is for the price column and 8 is for the standard price column
for row in range(1, 513):
    # Get info about the products of variant and split to list
    names = driver.find_element(By.XPATH, f'//*[@id="variant-product"]/div[2]/table/tbody/tr[{row}]/td[1]/a')
    names = names.text.replace(" ", "").split(",")

    if "PROBIOWOMANTHERAPY" in names:
        availability = driver.find_element(By.XPATH, f'//*[@id="variant-product"]/div[2]/table/tbody/tr[{row}]/td[7]/div/div/select')
        select = Select(availability)
        select.select_by_value("6") # 110
time.sleep(1000)