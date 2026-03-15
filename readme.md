# **Kijiji Car Scraper**

Automatically scrapes Kijiji for car listings matching your preferences and sends email notifications when new ones are found.

---

## Overview

Kijiji Car Scraper is a lightweight tool that monitors Kijiji for used car listings based on your filters — brand, price, year, mileage, transmission, and city. Run it once and it will notify you by email every time a new matching listing appears, twice a day.


---

## Requirements

- Windows 10 or later
- Python 3.10 or later
- Google Chrome

---

## Installation

### 1. Install Python

**Option A: Microsoft Store (easier)**
1. Open the **Microsoft Store**
2. Search for **Python**
3. Click **Python 3.x** published by Python Software Foundation
4. Click **Install**

**Option B: Python website**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **Download Python** and run the installer
3. **Important:** Check the box that says **"Add python.exe to PATH"** before clicking Install
4. Click **Install Now**

To verify it installed correctly, open Command Prompt and run:
```
python --version
```

### 2. Download the Scraper

Download or clone this project folder to your computer.

### 3. Install Dependencies

Open Command Prompt, navigate to the project folder, and run:
```
pip install selenium beautifulsoup4 keyring
```

---

## Setup

### Gmail App Password

The scraper sends notifications using your Gmail account. It requires a **Gmail App Password** — this is NOT your regular Gmail password.

Steps to create one:
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** on the left
3. Make sure **2-Step Verification** is turned on (required)
4. Search for **"App Passwords"** in the search bar at the top
5. Give it a name (e.g. "Kijiji Scraper") and click **Create**
6. Google gives you a 16-character password like `abcd efgh ijkl mnop`
7. Copy that password — you will enter it during setup

---

## Running the Scraper

1. Open Command Prompt
2. Navigate to the project folder:
```
cd "C:\path\to\Kijiji Scraper"
```
3. Run:
```
python main.py
```
4. On first run you will be prompted to enter your car preferences and Gmail App Password
5. The scraper will run immediately and email you if any matching listings are found
6. It will then automatically run again every day at 9 AM and 9 PM

---

## How It Works

1. On first run, your preferences and email are saved locally
2. The scraper builds a Kijiji search URL from your filters and opens it in a headless Chrome browser
3. It scrapes all listing pages and filters out any previously seen listings
4. New listings are saved to `matching_listings.csv`
5. If any new listings matching your preferences were found, a summary email is sent to your Gmail

---

## Changing Preferences

Delete `preferences.json` and rerun `main.py`. You will be prompted to enter your preferences again. Old listings saved will be deleted. There is also an option to directly change the file, which will not remove old listings.

---

## _Automatic Scheduling_

During first-time setup, the scraper registers itself to run daily at **9 AM** and **9 PM** via Windows Task Scheduler.

To remove the scheduled tasks, open Command Prompt and run:
```
schtasks /delete /tn KijijiScraper-9AM /f
schtasks /delete /tn KijijiScraper-9PM /f
```
