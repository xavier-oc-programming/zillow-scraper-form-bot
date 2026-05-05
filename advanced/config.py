# ============================================================
# URLs
# ============================================================
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfeaG5K1ujPpAqb82tWWqDHM9BYI0HU5iUhTXVStgG5faB-hg/viewform?usp=send_form"

# ============================================================
# Scraping — HTTP headers sent with requests
# ============================================================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# CSS selectors for Zillow Clone property cards
SELECTOR_LINKS = 'a[data-test="property-card-link"]'
SELECTOR_PRICES = 'span[data-test="property-card-price"]'
SELECTOR_ADDRESSES = 'address[data-test="property-card-addr"]'

# ============================================================
# Selenium
# ============================================================
# Check your Chrome version: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
CHROME_VERSION = 147

WAIT_TIMEOUT = 10  # seconds — for elements that MUST be present

# ============================================================
# Timing
# ============================================================
SUBMIT_DELAY = 1.0  # seconds to pause after each form submission

# ============================================================
# XPaths — Google Form inputs (absolute paths)
# If Google updates the form DOM, inspect with DevTools and update here.
# ============================================================
XPATH_ADDRESS_INPUT = (
    "/html/body/div/div[2]/form/div[2]/div/div[2]"
    "/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"
)
XPATH_PRICE_INPUT = (
    "/html/body/div/div[2]/form/div[2]/div/div[2]"
    "/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"
)
XPATH_LINK_INPUT = (
    "/html/body/div/div[2]/form/div[2]/div/div[2]"
    "/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"
)

# ============================================================
# XPaths — Google Form submit button
# ============================================================
XPATH_SUBMIT_BUTTON = (
    "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div"
)
