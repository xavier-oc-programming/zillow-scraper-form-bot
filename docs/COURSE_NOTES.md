# Course Notes — Day 53: Web Scraping & Data Entry Capstone

## Exercise description

Build an automated data-entry pipeline in two stages:

**Stage 1 — Web scraping (requests + BeautifulSoup)**

Scrape the App Brewery Zillow Clone page:
`https://appbrewery.github.io/Zillow-Clone/`

From each property card, extract:
- **Address** — the full street address of the listing
- **Price** — the monthly rent (e.g. `$1,500`)
- **Link** — the property detail URL

**Stage 2 — Automated form submission (Selenium)**

Open a Google Form for each listing and fill in three short-answer fields:
1. Address
2. Price
3. Link

Then submit the form and repeat for every listing found.

## Key techniques practised

- `requests.get()` with custom `User-Agent` headers to avoid 403 responses
- `BeautifulSoup.select()` with CSS attribute selectors (`data-test="..."`)
- Stripping and normalising scraped text (splitting on `/`, `+`, `|`)
- Selenium `WebDriverWait` + `EC.element_to_be_clickable` for stable form interaction
- Iterating over parallel lists with `zip()`

## Files provided by the course

| File | Contents |
|------|----------|
| `0_day_53_goals_what_you_will_make_by_the_end_of_the_day.py` | Goal stub with the Google Form link constant |
| `1_web_scraping_and_data_entry_capstone_project_requirements.py` | Full working solution |
| `2_hints_and_solution.py` | Empty hints file |

## Notes

- The Zillow Clone page is a static replica — it does not change, so the CSS
  selectors are stable.
- The Google Form XPaths are absolute and may break if the form is regenerated.
  If submissions stop working, open DevTools on the form and update the paths
  in `advanced/config.py`.
- `detach=True` in `original/main.py` keeps the browser open after the script
  ends so you can inspect the last submitted response. The advanced build uses
  `bot.quit()` in a `finally` block instead.
