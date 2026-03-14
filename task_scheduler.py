import os
import sys
import subprocess


def schedule_task():
    script_path = os.path.abspath("main.py")
    python_path = sys.executable

    for name, time in [("KijijiScraper-9AM", "09:00"), ("KijijiScraper-9PM", "21:00")]:
        subprocess.run([
            "schtasks", "/create",
            "/tn", name,
            "/tr", f'cmd.exe /c ""{python_path}" "{script_path}""',
            "/sc", "daily",
            "/st", time,
            "/f"
        ], check=True)

    print("Task scheduled to run daily at 9 AM and 9 PM.")


def unschedule_task():
    for name in ["KijijiScraper-9AM", "KijijiScraper-9PM"]:
        try:
            subprocess.run(["schtasks", "/delete", "/tn", name, "/f"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass  # Task doesn't exist (e.g. first run)
    print("Scheduled tasks removed.")
