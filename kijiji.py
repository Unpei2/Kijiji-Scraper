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
NEXT_BUTTON_XPATH = "/html/body/div[1]/div/div/div/main/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/div[3]/div/div/nav/ul/li[3]/a"
NEXT_BUTTON_REL_XPATH = '//*[@id="base-layout-main-wrapper"]/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/div[3]/div/div/nav/ul/li[3]/a'
NEXT_BUTTON_CLASS = "sc-c8742e84-0 jwUdte sc-4c795659-3 garPwt"
NEXT_BUTTON_ID = "pagination-next-link"

LISTING_LIST_ID = "srp-search-list"
TITLE_ID = "listing-link"        # listing link and title are in same <a> 
PRICE_ID = "autos-listing-price"
ODOMETER_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"
TRANSMISSION_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"




def traverse(listings):
    WAIT.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{LISTING_LIST_ID}"]')))
    html_content = DRIVER.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    listing_list = soup.find("ul", attrs={"data-testid": LISTING_LIST_ID})

    # Extract next page URL directly from parsed HTML
    next_url = None
    next_link = soup.find("a", attrs={"data-testid": NEXT_BUTTON_ID})
    if next_link:
        next_url = next_link.get("href")
        if next_url and next_url.startswith("/"):
            next_url = "https://www.kijiji.ca" + next_url

    

    try:
        all_listings = listing_list.find_all("li")
    except Exception as e:
        
        print(f"{e}, Listings could not be found.")
        return
        
    for post in all_listings:
        
        try:        # Title
            title = post.find("a", attrs={"data-testid": TITLE_ID})
            title_string = title.text
        except AttributeError as e:
            # print(f"{e}. Title could not be found.")
            continue

        try:        # Price
            price = post.find("p", attrs={"data-testid": PRICE_ID})
            price_string = price.text
        except Exception as e:
            print(f"{e}. Price finding error.")
            continue
            
        try:        # Kilometers
            odometer = post.find("p", class_=ODOMETER_CLASS)
            odometer_string = odometer.text
            space_index = odometer_string.find(" ")
            corrected_odometer = int(odometer_string[:space_index])
            if (corrected_odometer < 1000):
                corrected_odometer = corrected_odometer * 1000
            correct = str(corrected_odometer) + ' km'
        except Exception as e:
            print(f"{e}. Odometer finding error.")
            continue

        try:        # Transmission type
            transmission = odometer.find_next("p", class_=TRANSMISSION_CLASS)
            transmission_string = transmission.text
        except Exception as e:
            print(f"{e}. Transmission finding error.")
            continue

        try:        # Link is found in title
            link = title.get("href")
        except Exception as e:
            print(f"{e}. Link error.")
            continue
        
        # Regex expression for year
        try:
            year = re.search("\\d{4}", title.text)
            if year:
                parsed_year = year.group()
            else:
                parsed_year = "NA"
        except Exception as e:
            print(f"{e}. Year parsing error.")

        
        listings.append({"Title": title_string, "Price": price_string, "Kilometers": correct, "Transmission": transmission_string, "Year": parsed_year ,"Link":link})

    return next_url


def main():
    global DRIVER, WAIT
    open_options = Options()

    # Opens page until click close yourself, can delete later
    open_options.add_experimental_option("detach", True)

    # Gets rid of all extra console information
    open_options.add_argument("--log-level=3")
    open_options.add_experimental_option("excludeSwitches", ["enable-logging"])


    DRIVER = webdriver.Chrome(options=open_options)
    WAIT = WebDriverWait(DRIVER, 10)
    DRIVER.get(KIJIJI_URL)

    listings = []
    page = 1
    visited_urls = set()

    while (True):
        current_url = DRIVER.current_url
        visited_urls.add(current_url)

        print(f"\n--- Scraping page {page} ---")
        before = len(listings)
        next_url = traverse(listings)
        after = len(listings)
        print(f"Page {page}: added {after - before} listings (total so far: {after})")

        if not next_url:
            print("No next page URL found, stopping.")
            break

        if next_url in visited_urls:
            print(f"Already visited {next_url}, stopping to avoid infinite loop.")
            break

        print(f"Navigating to: {next_url}")
        DRIVER.get(next_url)
        page += 1

    print(f"\nTotal listings scraped: {len(listings)}")

    with open ("dict.txt", "w") as file:
        for item in listings:
            file.write(f'{item["Title"]}|{item["Price"]}|{item["Kilometers"]}|{item["Transmission"]}|{item["Year"]}|{item["Link"]}\n')

    with open("dict.txt", "r") as file:
        line_count = sum(1 for _ in file)
        
    print(f"Lines written to dict.txt: {line_count}")
    print("Finished")

if __name__ == "__main__":
    main()