import time
from datetime import datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from config import TARGET_URL, HEADLESS, TIMEOUT


class BrowserTelemetry:

    def __init__(self):

        self.events = []
        self.browser = None
        self.page = None
        self.playwright = None

    def log(self, category, details):

        event = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "details": details
        }

        self.events.append(event)

        print(f"[{category}] {details}")

    def safe_url(self, url):

        parsed = urlparse(url)

        return (
            f"{parsed.scheme}://"
            f"{parsed.netloc}"
            f"{parsed.path}"
        )

    def launch(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        self.page.set_default_timeout(TIMEOUT)

        self.register_events()

        self.log("BROWSER", "Chromium initialized")

        return self.page

    def register_events(self):

        self.page.on(
            "request",
            lambda req: self.log(
                "REQUEST",
                {
                    "method": req.method,
                    "resource": req.resource_type,
                    "url": self.safe_url(req.url)
                }
            )
        )

        self.page.on(
            "response",
            lambda res: self.log(
                "RESPONSE",
                {
                    "status": res.status,
                    "url": self.safe_url(res.url)
                }
            )
        )

        self.page.on(
            "pageerror",
            lambda error: self.log(
                "JAVASCRIPT_ERROR",
                str(error)[:300]
            )
        )

        self.page.on(
            "console",
            lambda message: self.log(
                "CONSOLE_ERROR",
                message.text[:300]
            ) if message.type == "error" else None
        )

    def collect_environment(self):

        result = self.page.evaluate("""
            () => ({
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,

                hardwareConcurrency:
                    navigator.hardwareConcurrency,

                deviceMemory:
                    navigator.deviceMemory || null,

                screen: {
                    width: screen.width,
                    height: screen.height
                },

                viewport: {
                    width: innerWidth,
                    height: innerHeight
                },

                timezone:
                    Intl.DateTimeFormat()
                    .resolvedOptions().timeZone,

                cookiesEnabled:
                    navigator.cookieEnabled
            })
        """)

        self.log("ENVIRONMENT", result)

        return result

    def collect_performance(self):

        result = self.page.evaluate("""
            () => {

                const nav =
                    performance.getEntriesByType(
                        "navigation"
                    )[0];

                return {
                    domContentLoaded:
                        nav?.domContentLoadedEventEnd,

                    loadEvent:
                        nav?.loadEventEnd,

                    responseEnd:
                        nav?.responseEnd,

                    resourceCount:
                        performance.getEntriesByType(
                            "resource"
                        ).length
                };
            }
        """)

        self.log("PERFORMANCE", result)

        return result

    def open_registration(self):

        self.log("NAVIGATION", "Opening registration page")

        self.page.goto(
            TARGET_URL,
            wait_until="domcontentloaded"
        )

        self.log("PAGE_TITLE", self.page.title())

    def close(self):

        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()