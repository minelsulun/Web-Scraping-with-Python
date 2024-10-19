import cloudscraper
from bs4 import BeautifulSoup
import time
import pandas as pd
from requests.exceptions import RequestException
import random

BASE_URL = 'https://www.hepsiemlak.com'
START_URL = f'{BASE_URL}/buca-kiralik'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

MAX_LISTINGS = 500
MAX_RETRIES = 5
RETRY_DELAY = 60  # Increased delay
RATE_LIMIT_DELAY = 300  # 5 minutes wait when hit by rate limit

scraper = cloudscraper.create_scraper()

def get_house_details(house_url):
    """Fetch details from each listing page."""
    for attempt in range(MAX_RETRIES):
        try:
            response = scraper.get(house_url, headers=HEADERS, timeout=30)
            if response.status_code == 429:
                print(f"Rate limit hit. Waiting for {RATE_LIMIT_DELAY} seconds...")
                time.sleep(RATE_LIMIT_DELAY)
                continue
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            info_table = soup.find_all('li', class_='spec-item')
            if not info_table:
                print(f"No data found: {house_url}")
                return None

            details = {"URL": house_url}
            for item in info_table:
                key = item.find('span', class_='txt').text.strip()
                value = item.find_all('span')[-1].text.strip()
                details[key] = value

            # Remove unwanted keys
            unwanted_keys = ['Ada No', 'Aidat', 'Parsel No', 'Site İçerisinde', 'Krediye Uygunluk']
            for key in unwanted_keys:
                details.pop(key, None)

            return details

        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for {house_url}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                sleep_time = RETRY_DELAY + random.uniform(1, 5)
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Max retries reached. Skipping {house_url}")
                return None

def scrape_links_and_fetch_data(url, collected_data):
    """Scrape links from a page and fetch details for each listing."""
    for attempt in range(MAX_RETRIES):
        try:
            response = scraper.get(url, headers=HEADERS, timeout=30)
            if response.status_code == 429:
                print(f"Rate limit hit. Waiting for {RATE_LIMIT_DELAY} seconds...")
                time.sleep(RATE_LIMIT_DELAY)
                continue
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            link_divs = soup.find_all('div', class_='links')
            if not link_divs:
                print("No data found: Page links not found")
                return collected_data

            for div in link_divs:
                if len(collected_data) >= MAX_LISTINGS:
                    return collected_data

                link_tag = div.find('a')
                if link_tag:
                    full_url = BASE_URL + link_tag['href']
                    print(f"\nProcessing link: {full_url}")

                    details = get_house_details(full_url)
                    if details:
                        collected_data.append(details)
                        print(f"Fetched data for: {full_url}")
                        print(f"Total listings scraped: {len(collected_data)}")
                    else:
                        print(f"No data: {full_url}")

                    sleep_time = random.uniform(3, 7)
                    print(f"Waiting for {sleep_time:.2f} seconds before next request...")
                    time.sleep(sleep_time)

            return collected_data

        except RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                sleep_time = RETRY_DELAY + random.uniform(1, 5)
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Max retries reached. Skipping page {url}")
                return collected_data

def main():
    """Collect listings from all pages and process data."""
    all_house_data = []
    page = 1

    while len(all_house_data) < MAX_LISTINGS:
        print(f"\nScraping page {page}...")
        page_url = f"{START_URL}?page={page}"

        new_data = scrape_links_and_fetch_data(page_url, [])
        if not new_data:
            print(f"No new data found on page {page}. Stopping.")
            break

        all_house_data.extend(new_data)
        print(f"Total listings scraped so far: {len(all_house_data)}")
        page += 1

        sleep_time = random.uniform(5, 10)
        print(f"Waiting for {sleep_time:.2f} seconds before next page...")
        time.sleep(sleep_time)

    print(f"\nScrape completed. Total {len(all_house_data)} listings collected.")

    if all_house_data:
        # Write to Excel file
        df = pd.DataFrame(all_house_data)
        df.to_excel("ilanlar3.xlsx", index=False)
        print("Listing information saved to 'ilanlar3.xlsx'.")
    else:
        print("No data was collected. Excel file was not created.")

if __name__ == "__main__":
    main()