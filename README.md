# zillow-scraper-form-bot

![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?logo=selenium&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-scraping-orange)
![undetected-chromedriver](https://img.shields.io/badge/undetected--chromedriver-bot--bypass-lightgrey)

Scrapes rental listings from a Zillow clone and auto-submits address, price, and link to a Google Form via Selenium. **Submits all 30 listings in ~35 seconds.**

Given the Zillow Clone page at `https://appbrewery.github.io/Zillow-Clone/`, the bot fetches every property card and extracts three pieces of data per listing — for example: `"250 Water St APT 4H, New York, NY 10038"`, `"$2,150"`, and the property detail URL. It then opens Google Chrome, navigates to a pre-configured Google Form, fills in the three short-answer fields for each listing, and clicks Submit — repeating until every listing has been recorded.

Two builds are included. The **original build** (`original/main.py`) is the course solution kept verbatim: one file, global constants, and functions. The **advanced build** (`advanced/`) refactors the same logic into separate classes (`ZillowScraper`, `FormBot`) with all constants centralised in `config.py` and undetected-chromedriver used in place of standard ChromeDriver to avoid bot-detection fingerprinting.

No external API accounts or credentials are required. The project uses only public URLs: the Zillow Clone is a static site hosted by the course, and the Google Form is a publicly accessible form that accepts anonymous submissions.

---

## Table of Contents

0. [Prerequisites](#0-prerequisites)
1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Usage & example output](#3-usage--example-output)
4. [Data flow](#4-data-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Data schema](#10-data-schema)
11. [Design decisions](#11-design-decisions)
12. [Course context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 0. Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.9+ | f-strings and `list[...]` type hints |
| Google Chrome | Must be installed; version noted in `config.py` |
| Internet access | To fetch the Zillow Clone page and open Google Form |

No API keys, accounts, or `.env` file needed.

---

## 1. Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the menu
python menu.py

# Or run a build directly
python original/main.py
python advanced/main.py
```

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---------|----------|----------|
| Scraping library | requests + BeautifulSoup | requests + BeautifulSoup |
| Browser automation | `selenium.webdriver.Chrome` | `undetected_chromedriver` |
| Code structure | Functions in one file | Classes, separate modules |
| Constants location | Inline in file | `advanced/config.py` |
| XPaths location | Inline in function | `advanced/config.py` |
| Click strategy | `element.click()` | JS click with normal-click fallback |
| Driver teardown | `detach=True` (keep open) | `bot.quit()` in `finally` block |

---

## 3. Usage & example output

```
$ python advanced/main.py

Fetching Zillow Clone listings...
Found 30 listings.
Submitting listing 1/30: 250 Water St APT 4H, New York, NY 10038 | $2,150
Submitting listing 2/30: 117 W 112th St APT 7, New York, NY 10026 | $1,800
...
Submitting listing 30/30: 94 Christopher St APT 2C, New York, NY 10014 | $3,500
Done. All listings submitted to Google Form.
```

---

## 4. Data flow

```
Zillow Clone page (HTML)
        │
        ▼
  ZillowScraper._fetch_html()   — requests.get with headers
        │
        ▼
  ZillowScraper._parse()        — BeautifulSoup CSS selectors
        │                         extracts links, prices, addresses
        ▼
  list of (address, price, link) tuples
        │
        ▼
  FormBot.submit()              — Chrome navigates to Google Form
        │                         fills 3 inputs, clicks Submit
        ▼
  Google Form response recorded  (repeat for each listing)
```

---

## 5. Features

### Both builds
- Scrapes address, price, and property link from every card on the Zillow Clone
- Cleans raw text: strips trailing `/mo`, `+`, and `|`-prefixed noise
- Submits each listing to a Google Form via an automated browser
- Pauses 1 second between submissions to avoid rate-limiting the form

### Advanced only
- Uses `undetected_chromedriver` to bypass Chromium bot-detection fingerprinting
- All constants and XPaths centralised in `config.py` — one change fixes a broken selector
- `_js_click()` helper handles intercepted elements (overlapping divs, disabled states)
- `bot.quit()` in a `finally` block ensures clean browser teardown on error
- CSS selectors for scraping are named constants — swap them in one place if the DOM changes

### Error handling

| Error | Cause | Message |
|-------|-------|---------|
| `requests.Timeout` | Zillow Clone page didn't respond within 15s | `"Timed out connecting to ... check your internet connection"` |
| `requests.ConnectionError` | No network when fetching listings | `"Could not reach ... check your internet connection"` |
| `urllib.URLError` | UC ChromeDriver download timed out on first run | `"Could not download ChromeDriver — check your internet connection"` |
| `NoSuchWindowException` | Chrome window closed while bot is running | `"Chrome window was closed. Don't close the browser while the bot is running."` |

### Builds at a glance

| | Original | Advanced |
|---|---|---|
| Scraping | requests + BeautifulSoup | requests + BeautifulSoup |
| Browser automation | `selenium.webdriver.Chrome` | `undetected_chromedriver` |
| Structure | Functions, one file | Classes, separate modules |
| Bot detection bypass | No | Yes |

---

## 6. Navigation flow

```
python menu.py
│
├── [1] original/main.py
│       └── fetch_page_html()
│           parse_listings()
│           setup_webdriver()
│           submit_listing_via_form()  ← repeated per listing
│
├── [2] advanced/main.py
│       ├── ZillowScraper.fetch()
│       │       ├── _fetch_html()
│       │       └── _parse()
│       │             ├── _extract_links()
│       │             ├── _extract_prices()
│       │             └── _extract_addresses()
│       └── FormBot.submit()  ← repeated per listing
│               ├── _fill_input()
│               └── _js_click()
│
└── [q] Quit
```

---

## 7. Architecture

```
zillow-scraper-form-bot/
│
├── menu.py                 # Interactive launcher
├── art.py                  # LOGO constant (ASCII art)
├── requirements.txt        # pip dependencies + Python version note
├── .gitignore
│
├── original/
│   └── main.py             # Course solution — verbatim, one file
│
├── advanced/
│   ├── config.py           # ALL constants: URLs, selectors, XPaths, timing
│   ├── scraper.py          # ZillowScraper — requests + BeautifulSoup
│   ├── bot.py              # FormBot — undetected-chromedriver + Selenium
│   └── main.py             # Orchestrator — wires scraper → bot
│
└── docs/
    └── COURSE_NOTES.md     # Original exercise description
```

---

## 8. Module reference

### `advanced/scraper.py` — `ZillowScraper`

| Method | Returns | Description |
|--------|---------|-------------|
| `fetch()` | `list[tuple[str, str, str]]` | Fetches page and returns `(address, price, link)` tuples |
| `_fetch_html()` | `str` | GET request to `ZILLOW_CLONE_URL` with headers |
| `_parse(html)` | `list[tuple[str, str, str]]` | Runs BeautifulSoup selectors and zips results |
| `_extract_links(elements)` | `list[str]` | Resolves relative hrefs to full URLs |
| `_extract_prices(elements)` | `list[str]` | Strips `/mo`, `+`, and trailing noise |
| `_extract_addresses(elements)` | `list[str]` | Strips `|`-prefixed label, collapses whitespace |

### `advanced/bot.py` — `FormBot`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__()` | — | Starts undetected-chromedriver Chrome instance |
| `submit(address, price, link)` | `None` | Navigates to form, fills inputs, submits |
| `quit()` | `None` | Closes the browser cleanly |
| `_fill_input(xpath, value)` | `None` | Waits for input, clears it, types value |
| `_js_click(element)` | `None` | Tries normal click; falls back to `execute_script` |

---

## 9. Configuration reference

All in `advanced/config.py`.

| Constant | Default | Description |
|----------|---------|-------------|
| `ZILLOW_CLONE_URL` | `https://appbrewery.github.io/Zillow-Clone/` | Static Zillow replica to scrape |
| `GOOGLE_FORM_URL` | `https://docs.google.com/forms/...` | Target Google Form (direct URL) |
| `HEADERS` | Chrome/macOS User-Agent | HTTP headers for the scraping request |
| `SELECTOR_LINKS` | `a[data-test="property-card-link"]` | CSS selector for property card links |
| `SELECTOR_PRICES` | `span[data-test="property-card-price"]` | CSS selector for price elements |
| `SELECTOR_ADDRESSES` | `address[data-test="property-card-addr"]` | CSS selector for address elements |
| `CHROME_VERSION` | `147` | Must match installed Chrome major version |
| `WAIT_TIMEOUT` | `10` | Selenium WebDriverWait timeout in seconds |
| `SUBMIT_DELAY` | `1.0` | Pause (seconds) between form submissions |
| `XPATH_ADDRESS_INPUT` | *(absolute XPath)* | Google Form address field |
| `XPATH_PRICE_INPUT` | *(absolute XPath)* | Google Form price field |
| `XPATH_LINK_INPUT` | *(absolute XPath)* | Google Form link field |
| `XPATH_SUBMIT_BUTTON` | *(absolute XPath)* | Google Form submit button |

**Updating `CHROME_VERSION`**: run `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version` and set the major version number.

---

## 10. Data schema

Each listing is represented as a plain tuple `(address, price, link)`:

| Field | Example | Source |
|-------|---------|--------|
| `address` | `"250 Water St APT 4H, New York, NY 10038"` | `<address data-test="property-card-addr">` |
| `price` | `"$2,150"` | `<span data-test="property-card-price">` — stripped of `/mo`, `+` |
| `link` | `"https://www.zillow.com/homedetails/..."` | `<a data-test="property-card-link">` — relative hrefs resolved |

---

## 11. Design decisions

**`undetected_chromedriver` over `selenium.webdriver.Chrome`**
Standard ChromeDriver injects automation flags into the browser binary that sites like Google can detect. `undetected_chromedriver` patches the binary to remove those signatures, giving more reliable form interaction.

**`CHROME_VERSION` pinned in `config.py`**
`undetected_chromedriver` needs the exact installed Chrome major version to download the matching ChromeDriver binary. A mismatch causes a startup error; centralising the pin means a single-line fix after a Chrome update.

**ChromeOptions prefs for permissions**
Chrome's native notification and geolocation dialogs are OS-level popups that Selenium XPaths cannot reach. Suppressing them at driver init (`notifications: 2`, `geolocation: 1`) prevents silent hangs where `send_keys` does nothing because a dialog is blocking the page.

**JS click with normal-click fallback**
`element.click()` raises `ElementClickInterceptedException` when another element overlaps the target (e.g. a floating cookie banner or a Google Form overlay). The `_js_click()` helper tries the normal click first and silently falls back to `execute_script("arguments[0].click()", el)`.

**`presence_of_element_located` for the submit button**
Google Forms' submit button starts in an interactable state but can be briefly covered during page load. Using `presence_of_element_located` then JS-clicking sidesteps `element_to_be_clickable` timeouts when the element is visually obscured.

**All XPaths in `config.py`**
Absolute XPaths for Google Form inputs are inherently fragile — if Google regenerates the form, every path changes. Keeping all of them in one place means a single file update restores the bot without touching any class or function.

**`finally: bot.quit()`**
The original build uses `detach=True` so the browser stays open after the script ends. The advanced build closes the browser cleanly in a `finally` block so the Chrome process does not leak on error.

---

## 12. Course context

**Course**: 100 Days of Code — The Complete Python Pro Bootcamp (Dr. Angela Yu, App Brewery)
**Day**: 53 — Web Scraping & Data Entry Capstone
**Topics**: requests, BeautifulSoup CSS selectors, Selenium WebDriverWait, automated form submission

---

## 13. Dependencies

| Module | Used in | Purpose |
|--------|---------|---------|
| `requests` | `scraper.py`, `original/main.py` | HTTP GET to fetch Zillow Clone HTML |
| `beautifulsoup4` | `scraper.py`, `original/main.py` | Parse HTML and extract listing elements |
| `selenium` | `bot.py`, `original/main.py` | WebDriverWait, expected conditions, By |
| `undetected-chromedriver` | `bot.py` | Patched ChromeDriver without automation fingerprint |
| `python-dotenv` | `advanced/main.py` | Load `.env` variables (future credential use) |
| `os`, `sys`, `subprocess` | `menu.py` | Console clear, Python path, run subprocesses |
| `time` | `bot.py`, `original/main.py` | `sleep()` delay between form submissions |
| `pathlib` | `menu.py`, `advanced/main.py` | Cross-platform file paths |
