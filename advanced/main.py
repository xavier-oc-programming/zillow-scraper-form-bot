import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scraper import ZillowScraper
from bot import FormBot


def main() -> None:
    print("Fetching Zillow Clone listings...")
    scraper = ZillowScraper()
    listings = scraper.fetch()
    print(f"Found {len(listings)} listings.")

    if not listings:
        print("No listings found. Check CSS selectors in config.py.")
        return

    bot = FormBot()
    try:
        for i, (address, price, link) in enumerate(listings, start=1):
            print(f"Submitting listing {i}/{len(listings)}: {address} | {price}")
            bot.submit(address, price, link)

        print("Done. All listings submitted to Google Form.")
    finally:
        bot.quit()


if __name__ == "__main__":
    main()
