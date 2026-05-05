from __future__ import annotations

import requests
from bs4 import BeautifulSoup

import config


class ZillowScraper:
    """Fetches and parses rental listings from the Zillow Clone page."""

    def fetch(self) -> list[tuple[str, str, str]]:
        """Return a list of (address, price, link) tuples from the Zillow Clone."""
        html = self._fetch_html()
        return self._parse(html)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fetch_html(self) -> str:
        try:
            response = requests.get(config.ZILLOW_CLONE_URL, headers=config.HEADERS, timeout=15)
        except requests.exceptions.Timeout:
            raise SystemExit(f"Timed out connecting to {config.ZILLOW_CLONE_URL}\nCheck your internet connection or try again later.")
        except requests.exceptions.ConnectionError:
            raise SystemExit(f"Could not reach {config.ZILLOW_CLONE_URL}\nCheck your internet connection or try again later.")
        response.raise_for_status()
        return response.text

    def _parse(self, html: str) -> list[tuple[str, str, str]]:
        soup = BeautifulSoup(html, "html.parser")

        link_elements = soup.select(config.SELECTOR_LINKS)
        price_elements = soup.select(config.SELECTOR_PRICES)
        address_elements = soup.select(config.SELECTOR_ADDRESSES)

        links = self._extract_links(link_elements)
        prices = self._extract_prices(price_elements)
        addresses = self._extract_addresses(address_elements)

        count = min(len(links), len(prices), len(addresses))
        return list(zip(addresses[:count], prices[:count], links[:count]))

    @staticmethod
    def _extract_links(elements) -> list[str]:
        links = []
        for tag in elements:
            href = tag.get("href")
            if not href:
                continue
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(f"https://www.zillow.com{href}")
        return links

    @staticmethod
    def _extract_prices(elements) -> list[str]:
        prices = []
        for tag in elements:
            raw = tag.get_text(strip=True)
            cleaned = raw.split("+")[0].split("/")[0]
            prices.append(cleaned)
        return prices

    @staticmethod
    def _extract_addresses(elements) -> list[str]:
        addresses = []
        for tag in elements:
            raw = tag.get_text(separator=" ", strip=True)
            if "|" in raw:
                cleaned = raw.split("|")[-1].strip()
            else:
                cleaned = raw.strip()
            addresses.append(" ".join(cleaned.split()))
        return addresses
