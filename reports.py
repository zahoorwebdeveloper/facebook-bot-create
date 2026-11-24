import csv
import json

from config import REPORT_DIR
from database import get_sessions


def export_csv():

    sessions = get_sessions()

    output = REPORT_DIR / "telemetry.csv"

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Session ID",
            "Timestamp",
            "Browser",
            "Category",
            "Details"
        ])

        for session in sessions:

            session_id, timestamp, browser, events = session

            for event in json.loads(events):

                writer.writerow([
                    session_id,
                    timestamp,
                    browser,
                    event["category"],
                    json.dumps(event["details"])
                ])

    print(f"[+] Report saved: {output}")