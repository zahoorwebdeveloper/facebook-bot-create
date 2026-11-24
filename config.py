from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

DATABASE = DATA_DIR / "research.db"
PROXY_FILE = BASE_DIR / "proxies.txt"

TARGET_URL = "https://www.facebook.com/reg/"

HEADLESS = False

TIMEOUT = 60000

for directory in [DATA_DIR, REPORT_DIR]:
    directory.mkdir(exist_ok=True)