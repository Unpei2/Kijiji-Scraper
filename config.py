import json


PREFS_FILE = "preferences.json"

def get_preferences():
    brands = []
    print("Please enter user preferences. This can be changed later")

    print("Enter preferred car brands (Enter DONE when finished).")
    while (True):
        user_input = str(input("Brand: ")).strip().lower()
        if (user_input == "done"):
            break
        brands.append(user_input)

    min_price = int(input("Enter minimum price: "))
    max_price = int(input("Enter maximum price: "))
    min_year = int(input("Enter minimum year: "))
    max_year = int(input("Enter maximum year: "))
    max_kilometers = int(input("Enter maximum kilometers: "))
    transmission_type = int(input("Enter transmission preference (0 for no preference, 1 for manual, 2 for automatic): "))

    print("Available cities: Edmonton, Calgary, Toronto GTA, Toronto, Mississauga, Markham, Vancouver GTA, Vancouver, Richmond, Victoria")
    city = str(input("Enter city to search in: ")).strip().lower()

    prefs = {
        "brands": brands,
        "min_price": min_price,
        "max_price": max_price,
        "min_year": min_year,
        "max_year": max_year,
        "max_kilometers": max_kilometers,
        "transmission_type": transmission_type,
        "city": city
    }

    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=4)

get_preferences()
