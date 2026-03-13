import os
import get_listings
from config import get_preferences, get_prefs_path
from task_scheduler import schedule_task, unschedule_task


def main():
    if not os.path.exists(get_prefs_path()):
        unschedule_task()
        if os.path.exists("matching_listings.csv"):
            os.remove("matching_listings.csv")
        get_preferences()
        schedule_task()

    get_listings.main()


if __name__ == "__main__":
    main()