# Imports
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

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

products = {
    "ANTI-STRESSTHERAPY": 659,
    "MICROBIOMETHERAPY": 1099,
    "PROBIOWOMANTHERAPY": 952,
    "PROBIOKIDSTHERAPY": 816,
    "HAPPYSKINTHERAPY": 879,
    "LOVELYHAIRTHERAPY": 1099,
    "PROBIODETOXTHERAPY": 1099,
    "FINEBODYTHERAPY": 1650
}

for page in range(4, 12):
    driver.get(f"https://www.organic-oasis.cz/admin/ceny/?f%5BpricelistId%5D=1&f%5BproductName%5D=PROSINCOVÉ+COMBO&from={page}") # product

    # Changing the price column = 6 is for the price column and 8 is for the standard price column
    for row in range(1, 51):
        try:
            names_row = 4
            
            names = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{row}]/td[{names_row}]/a/span/span[1]/span[1]')
            # Get info about the products of variant from <span> tag and remove unnecessary characters
            names = names.text
            names = names.replace("První produkt:", "")
            names = names.replace("Druhý produkt:", "")
            names = names.replace("Třetí produkt:", "")
            names = names.replace("\n", "")
            names = names.replace(" ", "")
            
            # Split the product names into a list
            names = names.split(",")

            # Search for the price and standard price input fields and clear them
            price = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{row}]/td[6]/div/div/input')
            price.clear()
            
            standard_price = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{row}]/td[8]/div/div/input')
            standard_price.clear()

            # Getting the price of each product from products dictionary
            sum_price = 0
            for name in names:
                sum_price += products[name]
            discount_price = int(round(sum_price * 0.8))

            # Enter the price and standard price into the input fields
            price.send_keys(discount_price)
            standard_price.send_keys(sum_price)

        except NoSuchElementException:
            pass
    
    # Time to save and check the changes in Shoptet admin
    button = driver.find_element(By.XPATH, '//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[1]/div/a[1]')
    button.click()
    time.sleep(1)

    # setting the stock of the products to 100
    driver.get(f"https://www.organic-oasis.cz/admin/sklad/?f%5BproductName%5D=PROSINCOVÉ+COMBO&from={page}") # stock 

    for row in range(1, 51):
        try:
            # find the stock input field
            stock = driver.find_element(By.XPATH, f'//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[2]/table/tbody/tr[{row}]/td[5]/div/div/input')
            stock.clear()
            stock.send_keys(100)

        except NoSuchElementException:
            pass
    
    # Time to save and check the changes in Shoptet admin
    button = driver.find_element(By.XPATH, '//*[@id="css"]/body/div[1]/div[2]/div[2]/form/fieldset/div[1]/p/a[2]')
    button.click()
    time.sleep(1)

driver.quit()