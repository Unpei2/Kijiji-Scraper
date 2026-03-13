from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

from notification import send_email
from config import get_prefs_path

import re
import os
import json
import time
import keyring

DRIVER = None
BASE_LINK = "https://www.kijiji.ca/b-cars-trucks/"

NEXT_BUTTON_ID = "pagination-next-link"
NUM_TOTAL_LISTINGS = "srp-results"

LISTING_LIST_ID = "srp-search-list"
TITLE_ID = "listing-link"        # listing link and title are in same <a> 
PRICE_ID = "autos-listing-price"
ODOMETER_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"
TRANSMISSION_CLASS = "sc-991ea11d-0 epsmyv sc-4b5a8895-2 eEvVV"

CITIES = {
    "edmonton":     ("edmonton-area",            "l1700202"),
    "calgary":      ("calgary",                  "l1700199"),
    "toronto gta":  ("gta-greater-toronto-area", "l1700272"),
    "toronto":      ("city-of-toronto",          "l1700273"),
    "mississauga":  ("mississauga-peel-region",  "l1700276"),
    "markham":      ("markham-york-region",       "l1700274"),
    "vancouver gta":("greater-vancouver-area",   "l80003"),
    "vancouver":    ("vancouver",                "l1700287"),
    "richmond":     ("richmond-bc",              "l1700288"),
    "victoria":     ("victoria-bc",              "l1700173"),
}

def build_url():
    with open(get_prefs_path(), "r") as f:
        prefs = json.load(f)

    city_slug, location_id = CITIES[prefs["city"]]
    year_range = f"{prefs['min_year']}__{prefs['max_year']}"
    transmission = prefs["transmission_type"]
    transmission_param = f"&transmission={transmission}" if transmission != 0 else ""

    brands = prefs.get("brands", [])
    if brands:
        makes = "__".join(b.replace(" ", "+") for b in brands)
        category = f"{makes}-{year_range}/c174{location_id}a54a68"
    else:
        category = f"{year_range}/c174{location_id}a68"

    return (
        f"{BASE_LINK}{city_slug}/{category}"
        f"?kilometers=0__{prefs['max_kilometers']}"
        f"&price={prefs['min_price']}__{prefs['max_price']}"
        f"{transmission_param}"
        f"&view=list"
    )

def traverse(listings, prefs):
    global num_listings
    try:
        WAIT.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{LISTING_LIST_ID}"]')))
    except Exception:
        print("No listings found on this page.")
        return None
    html_content = DRIVER.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    listing_list = soup.find("ul", attrs={"data-testid": LISTING_LIST_ID})

    # Extract next page URL directly from parsed HTML
    next_url = None
    next_container = soup.find("li", attrs={"data-testid": NEXT_BUTTON_ID})
    if next_container:
        next_link = next_container.find("a")
        next_url = next_link.get("href")
        
    num_listings = soup.find("h2", attrs={"data-testid": NUM_TOTAL_LISTINGS}).find_next("h2", attrs={"data-testid": NUM_TOTAL_LISTINGS})

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

        try:        # Link is found in title
            link = title.get("href")
            if link in SEEN:
                continue
        except Exception as e:
            link = "NA"
            print(f"{e}. Link error.")
            continue

        try:        # Price
            price = post.find("p", attrs={"data-testid": PRICE_ID})
            price_string = price.text
        except Exception as e:
            price_string = "NA"
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
            correct = "NA"
            print(f"{e}. Odometer finding error.")
            continue

        try:        # Transmission type
            transmission = odometer.find_next("p", class_=TRANSMISSION_CLASS)
            transmission_string = transmission.text
        except Exception as e:
            transmission = "NA"
            print(f"{e}. Transmission finding error.")
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
            parsed_year = "NA"

        if parsed_year == "NA" and (prefs.get("min_year") or prefs.get("max_year")):
            continue

        
        listings.append({"Title": title_string, "Price": price_string, "Kilometers": correct, "Transmission": transmission_string, "Year": parsed_year ,"Link":link})
        
    return next_url


def main():
    global DRIVER, WAIT, SEEN
    open_options = Options()

    # Gets rid of all extra console information
    open_options.add_argument("--log-level=3")
    open_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    open_options.add_argument("--headless=new")
    open_options.add_argument("--disable-gpu")
    open_options.add_argument("--no-sandbox")

    # Stop all images from loading
    open_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    })

    # Does not wait for everything to load, cuts down runtime from 30s to 1 s
    open_options.page_load_strategy = "eager"

    DRIVER = webdriver.Chrome(options=open_options)
    WAIT = WebDriverWait(DRIVER, 10)
    with open(get_prefs_path(), "r") as f:
        prefs = json.load(f)
    DRIVER.get(build_url())

    listings = []
    page = 1
    visited_urls = set()
    total_start = time.time()
    SEEN = set()
    if os.path.exists("matching_listings.csv"):
        with open("matching_listings.csv", "r") as f:
            for line in f:
                link = line.strip().split(";")[-1]  # link is the last column
                SEEN.add(link)

    while (True):
        current_url = DRIVER.current_url
        visited_urls.add(current_url)

        print(f"--- Scraping page {page} ---")
        before = len(listings)
        page_start = time.time()
        next_url = traverse(listings, prefs)
        after = len(listings)
        print(f"Page {page}: added {after - before} listings (total so far: {after} out of {num_listings.text}) | {time.time() - page_start:.1f}s | elapsed: {time.time() - total_start:.1f}s\n")

        if not next_url:
            print("No next page URL found, stopping.")
            break

        if next_url in visited_urls:
            print(f"Already visited {next_url}, stopping to avoid infinite loop.")
            break

        
        DRIVER.get(next_url)
        page += 1
        print(f"Navigating to: page {page}")
    
    print(f"\nTotal listings scraped: {len(listings)} out of {num_listings.text}")

    with open("matching_listings.csv", "a") as file:
        for item in listings:
            file.write(f'{item["Title"]};{item["Price"]};{item["Kilometers"]};{item["Transmission"]};{item["Year"]};{item["Link"]}\n')

    with open("matching_listings.csv", "r") as file:
        line_count = sum(1 for _ in file)
        
    
    if (len(listings) == 0):
        print("No new listings.")
    else:
        print(f"{len(listings)} listings added to matching_listings.csv: {line_count}")
        email = prefs["email"]
        password = keyring.get_password("kijiji-scraper", email)
        body = f"{len(listings)} new listings matching your preferences were found!\n\n"

        for item in listings:
            body += f"{item['Title']} - {item['Price']} - {item['Kilometers']}\n{item['Link']}\n\n"
        
        send_email(email, password, body)

    DRIVER.quit()
    print("Finished")

if __name__ == "__main__":
    main()