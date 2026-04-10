"""
original/main.py
Day 53 – Web Scraping & Data Entry Capstone

This script:
1. Scrapes listings from the Zillow Clone website.
2. Extracts addresses, prices, and links.
3. Fills your Google Form automatically using Selenium.
"""

from __future__ import annotations

import time
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ========================================================
# CONFIGURATION
# ========================================================

ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"

GOOGLE_FORM_URL = "https://forms.gle/MHjwDFDMrhHGm2iW6"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ========================================================
# BEAUTIFUL SOUP SCRAPING
# ========================================================

def fetch_page_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def parse_listings(html: str) -> Tuple[List[str], List[str], List[str]]:
    soup = BeautifulSoup(html, "html.parser")

    link_elements = soup.select('a[data-test="property-card-link"]')
    price_elements = soup.select('span[data-test="property-card-price"]')
    address_elements = soup.select('address[data-test="property-card-addr"]')

    links: List[str] = []
    prices: List[str] = []
    addresses: List[str] = []

    # LINKS
    for tag in link_elements:
        href = tag.get("href")
        if not href:
            continue
        if href.startswith("http"):
            full_url = href
        else:
            full_url = f"https://www.zillow.com{href}"
        links.append(full_url)

    # PRICES
    for tag in price_elements:
        raw = tag.get_text(strip=True)
        cleaned = raw.split("+")[0].split("/")[0]
        prices.append(cleaned)

    # ADDRESSES
    for tag in address_elements:
        raw = tag.get_text(separator=" ", strip=True)
        if "|" in raw:
            cleaned = raw.split("|")[-1].strip()
        else:
            cleaned = raw.strip()
        cleaned = " ".join(cleaned.split())
        addresses.append(cleaned)

    min_len = min(len(links), len(prices), len(addresses))
    return links[:min_len], prices[:min_len], addresses[:min_len]


# ========================================================
# SELENIUM FORM SUBMISSION — ABSOLUTE XPATH VERSION
# ========================================================

def setup_webdriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def submit_listing_via_form(driver, address: str, price: str, link: str) -> None:
    """
    Submit a single form entry using the absolute XPaths provided
    for each of the three short-answer inputs and the Enviar button.
    """
    driver.get(GOOGLE_FORM_URL)

    # Your FULL absolute XPaths for each question:
    ADDRESS_XPATH = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    PRICE_XPATH   = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    LINK_XPATH    = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

    # FULL XPath for Enviar button:
    SUBMIT_XPATH  = '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div'

    # Wait and select each input
    address_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ADDRESS_XPATH))
    )
    price_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, PRICE_XPATH))
    )
    link_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, LINK_XPATH))
    )

    # Fill out form
    address_input.send_keys(address)
    price_input.send_keys(price)
    link_input.send_keys(link)

    # Submit the form
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, SUBMIT_XPATH))
    )
    submit_button.click()

    time.sleep(1)


# ========================================================
# MAIN
# ========================================================

def main() -> None:
    print("Fetching Zillow Clone page...")
    html = fetch_page_html(ZILLOW_CLONE_URL)

    print("Extracting listing data...")
    links, prices, addresses = parse_listings(html)
    print(f"Found {len(links)} listings.")

    if not links:
        print("No listings found. Check selectors.")
        return

    driver = setup_webdriver()

    try:
        for i, (addr, price, lnk) in enumerate(
            zip(addresses, prices, links), start=1
        ):
            print(f"Submitting listing {i}: {addr} | {price}")
            submit_listing_via_form(driver, addr, price, lnk)

        print("All form submissions complete. Check your Google Form responses.")

    finally:
        # detach=True keeps browser open for review
        pass


if __name__ == "__main__":
    main()
