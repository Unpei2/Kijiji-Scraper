import os
import get_listings
from config import get_preferences, get_prefs_path, get_listings_csv_path
from task_scheduler import schedule_task, unschedule_task


def main():
    if not os.path.exists(get_prefs_path()):
        unschedule_task()
        if os.path.exists(get_listings_csv_path()):
            os.remove(get_listings_csv_path())
        get_preferences()
        schedule_task()

    get_listings.main()


if __name__ == "__main__":
    main()