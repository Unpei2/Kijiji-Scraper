import json
import getpass
import keyring
import os

def get_prefs_path():
    """Get absolute path to preferences.json in the script's directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "preferences.json")

def get_preferences():
    brands = []
    print("Please enter user preferences. This can be changed later")

    print("Enter preferred car brands (Enter DONE when finished).")
    while (True):
        user_input = str(input("Brand: ")).strip().lower()
        if (user_input == "done"):
            break
        brands.append(user_input)

    min_price = int(input("Minimum price: "))
    max_price = int(input("Maximum price: "))
    min_year = int(input("Minimum year: "))
    max_year = int(input("Maximum year: "))
    max_kilometers = int(input("Maximum kilometers: "))
    transmission_type = int(input("Transmission preference (0 for no preference, 1 for manual, 2 for automatic): "))

    print("Available cities: Edmonton, Calgary, Toronto GTA, Toronto, Mississauga, Markham, Vancouver GTA, Vancouver, Richmond, Victoria")
    city = str(input("Enter city to search in: ")).strip().lower()

    import smtplib
    email = str(input("Enter email: ")).strip()
    existing_password = keyring.get_password("kijiji-scraper", email)
    if existing_password:
        print("A saved App Password was found for this email. Using existing password.")
    else:
        while True:
            password = getpass.getpass("Enter Gmail App Password (input hidden): ")
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(email, password)
                keyring.set_password("kijiji-scraper", email, password)
                print("Email verified and saved successfully.")
                break
            except smtplib.SMTPAuthenticationError:
                print("Incorrect email or App Password. Please try again.")

    prefs = {
        "brands": brands,
        "min_price": min_price,
        "max_price": max_price,
        "min_year": min_year,
        "max_year": max_year,
        "max_kilometers": max_kilometers,
        "transmission_type": transmission_type,
        "city": city,
        "email": email
    }

    with open(get_prefs_path(), "w") as f:
        json.dump(prefs, f, indent=4)

