import os
import get_listings
from config import get_preferences
from task_scheduler import schedule_task


def main():
    if not os.path.exists("preferences.json"):
        if os.path.exists("matching_listings.csv"):
            os.remove("matching_listings.csv")
        get_preferences()
        schedule_task()

    get_listings.main()


if __name__ == "__main__":
    main()