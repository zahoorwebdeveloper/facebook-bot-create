class ChallengeDetector:

    KEYWORDS = {

        "CAPTCHA": [
            "captcha",
            "security check",
            "prove you're human"
        ],

        "VERIFICATION": [
            "verify your account",
            "verification code",
            "confirm your identity"
        ],

        "RESTRICTION": [
            "temporarily blocked",
            "unusual activity",
            "try again later"
        ]
    }

    def analyze(self, page):

        findings = []

        try:

            text = page.locator(
                "body"
            ).inner_text(timeout=10000).lower()

        except Exception:

            return findings

        for category, keywords in self.KEYWORDS.items():

            for keyword in keywords:

                if keyword in text:

                    findings.append({
                        "category": category,
                        "indicator": keyword
                    })

        return findings