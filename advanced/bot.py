from __future__ import annotations

import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


class FormBot:
    """Submits Zillow listing data to a Google Form via an automated browser."""

    def __init__(self) -> None:
        options = uc.ChromeOptions()
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 1,
        })
        self.driver = uc.Chrome(options=options, version_main=config.CHROME_VERSION)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, config.WAIT_TIMEOUT)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def submit(self, address: str, price: str, link: str) -> None:
        """Open the Google Form and submit one listing entry."""
        self.driver.get(config.GOOGLE_FORM_URL)

        self._fill_input(config.XPATH_ADDRESS_INPUT, address)
        self._fill_input(config.XPATH_PRICE_INPUT, price)
        self._fill_input(config.XPATH_LINK_INPUT, link)

        submit_btn = self.wait.until(
            EC.presence_of_element_located((By.XPATH, config.XPATH_SUBMIT_BUTTON))
        )
        self._js_click(submit_btn)

        time.sleep(config.SUBMIT_DELAY)

    def quit(self) -> None:
        self.driver.quit()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fill_input(self, xpath: str, value: str) -> None:
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.clear()
        element.send_keys(value)

    def _js_click(self, element) -> None:
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
