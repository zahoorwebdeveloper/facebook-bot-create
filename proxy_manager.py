from urllib.parse import urlparse

from config import PROXY_FILE


class ProxyManager:

    SUPPORTED = [
        "http",
        "https",
        "socks5"
    ]

    def __init__(self):

        self.proxies = []

    def load(self):

        if not PROXY_FILE.exists():

            print("[!] proxies.txt not found")
            return []

        with open(PROXY_FILE, "r") as file:

            for line in file:

                proxy = line.strip()

                if not proxy or proxy.startswith("#"):
                    continue

                self.proxies.append(proxy)

        return self.proxies

    def analyze(self):

        results = []

        for proxy in self.proxies:

            parsed = urlparse(proxy)

            valid = (
                parsed.scheme in self.SUPPORTED
                and parsed.hostname is not None
                and parsed.port is not None
            )

            results.append({
                "proxy": (
                    f"{parsed.scheme}://"
                    f"{parsed.hostname}:"
                    f"{parsed.port}"
                    if valid else "INVALID"
                ),
                "protocol": parsed.scheme,
                "valid_format": valid
            })

        return results

    def summary(self):

        print("\n========== PROXY INVENTORY ==========")

        for item in self.analyze():

            print(item)

        print("Total:", len(self.proxies))