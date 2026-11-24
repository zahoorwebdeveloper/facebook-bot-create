from datetime import datetime

from telemetry import BrowserTelemetry
from detector import ChallengeDetector
from proxy_manager import ProxyManager

from database import (
    initialize,
    save_session,
    save_finding
)

from reports import export_csv


def start_research():

    telemetry = BrowserTelemetry()

    detector = ChallengeDetector()

    try:

        page = telemetry.launch()

        telemetry.collect_environment()

        telemetry.open_registration()

        print("\n[+] Browser telemetry active.")

        input(
            "\nObserve the page manually. "
            "Press ENTER to analyze..."
        )

        findings = detector.analyze(page)

        print("\n========== FINDINGS ==========")

        for finding in findings:

            print(finding)

            telemetry.log(
                "SECURITY_FINDING",
                finding
            )

        telemetry.collect_performance()

        session_id = save_session(
            datetime.now().isoformat(),
            "Chromium",
            telemetry.events
        )

        for finding in findings:

            save_finding(
                session_id,
                finding["category"],
                finding["indicator"],
                datetime.now().isoformat()
            )

        print("\n[+] Session saved.")

    except Exception as error:

        print("[!] Error:", error)

    finally:

        telemetry.close()


def main():

    initialize()

    while True:

        print("""
========================================
       FB SECURITY RESEARCH v3.0
========================================

1. Start browser telemetry
2. Analyze proxy inventory
3. Export CSV report
4. Exit

========================================
""")

        choice = input("Select: ").strip()

        if choice == "1":

            start_research()

        elif choice == "2":

            manager = ProxyManager()

            manager.load()

            manager.summary()

        elif choice == "3":

            export_csv()

        elif choice == "4":

            print("Exiting...")
            break

        else:

            print("[!] Invalid selection.")


if __name__ == "__main__":

    main()