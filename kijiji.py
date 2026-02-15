from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import time
import os
import re

DRIVER = None

KIJIJI_URL = "https://www.kijiji.ca/b-cars-trucks/edmonton/c174l1700203?kilometers=0__150000&price=0__15000&transmission=1&view=list"
LISTING_LIST_CLASS = "sc-31c99dfc-0 dREgHU"
LISTING_LIST_XPATH = '/html/body/div[1]/div/div/div/main/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/ul'

TITLE_CLASS = "sc-eb5dea32-1 gPyerW"

PRICE_CLASS = "sc-991ea11d-0 eZUULr sc-54de28bc-3 imlMOc"

ODOMETER_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"

TRANSMISSION_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"


def traverse():
    with open("source.txt", "w") as file:
        file.write(DRIVER.page_source)
    
    listings = []

    html_content = DRIVER.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    
    time.sleep(5)       # wait for listings to load

    list = soup.find("ul", class_=LISTING_LIST_CLASS)

    try:
        listings = list.find_all("li")
    except Exception as e:
        print(f"{e}, Listings could not be found.")

    with open ("titles.txt", "w") as file:
        
        for post in listings:
            
            try:        # Title
                title = post.find("a", class_=TITLE_CLASS)
                file.write(f"{title.text}|")
            except Exception as e:
                print(f"{e}. Title could not be found.")
                continue

            try:        # Price
                price = post.find("p", class_=PRICE_CLASS)
                file.write(f"{title.text}|")
            except Exception as e:
                print(f"{e}. Price finding error.")
                continue
                
            try:        # Kilometers
                odometer = post.find("p", class_=ODOMETER_CLASS)
                file.write(f"{odometer.text}|")
            except Exception as e:
                print(f"{e}. Odometer finding error.")
                continue

            try:        # Transmission type
                transmission = odometer.find_next("p", class_=TRANSMISSION_CLASS)
                file.write(f"{transmission.text}|")
            except Exception as e:
                print(f"{e}. Transmission finding error.")
                continue

            try:        # Link is found in title
                link = title.get("href")
                file.write(f"{link}\n")
            except Exception as e:
                print(f"{e}. Link error.")
                continue
            
            year = re.search("\\d{4}", title)
            print(year.group())
            listings.append({"Title:": title.text, "Price":price.text, "Kilometers":odometer.text, "Transmission:":transmission.text,"Year": year ,"Link":link})

    # with open ("dict.txt", "w") as file:
    for item in listings:
        print(item)

    print("Finished")
    
    
    
def main():
    global DRIVER, WAIT
    open_options = Options()

    # Opens page until click close yourself, can delete later
    open_options.add_experimental_option("detach", True)

    # Gets rid of all extra console information
    open_options.add_argument("--log-level=3")
    open_options.add_experimental_option("excludeSwitches", ["enable-logging"])


    DRIVER = webdriver.Chrome(options=open_options)
    WAIT = WebDriverWait(DRIVER, 20)
    DRIVER.get(KIJIJI_URL)
    traverse()

if __name__ == "__main__":
    main()