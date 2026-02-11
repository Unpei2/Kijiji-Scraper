from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import time
import os


DRIVER = None

KIJIJI_URL = "https://www.kijiji.ca/b-cars-trucks/edmonton/c174l1700203?kilometers=0__150000&price=0__15000&transmission=1&view=list"
LISTING_LIST_CLASS = "sc-31c99dfc-0 dREgHU"
TITLE_CLASS = "sc-991ea11d-0 eZUULr sc-54de28bc-3 imlMOc"

def traverse():
    with open("source.txt", "w") as file:
        file.write(DRIVER.page_source)
    
    

    html_content = DRIVER.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    list = soup.find(By.CLASS_NAME, LISTING_LIST_CLASS)

    if list:
        listings = list.find_all("li")
    
        for post in listings:
            title = soup.find(By.CLASS_NAME, TITLE_CLASS)
            print(title)

    
    
def main():
    global DRIVER, WAIT
    open_options = Options()

    # Opens page until click close yourself, can delete later
    open_options.add_experimental_option("detach", True)

    # Gets rid of all extra console information
    open_options.add_argument("--log-level=3")
    open_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # # Gets rid of notification popup
    # notifications = {"profile.default_content_setting_values.notifications" : 2}
    # open_options.add_experimental_option("prefs", notifications)

    DRIVER = webdriver.Chrome(options=open_options)
    WAIT = WebDriverWait(DRIVER, 20)
    DRIVER.get(KIJIJI_URL)


if __name__ == "__main__":
    main()