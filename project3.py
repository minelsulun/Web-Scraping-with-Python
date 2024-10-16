import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = 'https://www.hepsiemlak.com'
START_URL = f'{BASE_URL}/buca-kiralik'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

MAX_LISTINGS = 20  # Çekmek istediğimiz ilan sayısı

def get_house_details(house_url):
    """Her ilan detay sayfasından ilan bilgilerini alır."""
    try:
        response = requests.get(house_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        info_table = soup.find_all('li', class_='spec-item')
        details = {"URL": house_url}

        if not info_table:
            print(f"Veri yok: {house_url}")
            return None

        for item in info_table:
            key = item.find('span', class_='txt').text.strip()
            value = item.find_all('span')[-1].text.strip()
            details[key] = value

        # İstenmeyen özellikleri kaldır
        unwanted_keys = ['Ada No', 'Aidat', 'Parsel No', 'Site İçerisinde', 'Krediye Uygunluk']
        for key in unwanted_keys:
            details.pop(key, None)  # Eğer anahtar varsa kaldır

        return details

    except requests.RequestException as e:
        print(f"Error fetching {house_url}: {e}")
        return None

def scrape_links_and_fetch_data(url, collected_data):
    """Bir sayfadaki ilanların linklerini çekip, her link için detayları alır."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        link_divs = soup.find_all('div', class_='links')

        if not link_divs:
            print("Veri yok: Sayfa linkleri bulunamadı")
            return collected_data

        for div in link_divs:
            if len(collected_data) >= MAX_LISTINGS:
                break  # 20 ilan toplandıysa dur

            link_tag = div.find('a')
            if link_tag:
                full_url = BASE_URL + link_tag['href']
                print(f"\nProcessing link: {full_url}")

                details = get_house_details(full_url)
                if details:
                    collected_data.append(details)
                    print(f"Fetched data for: {full_url}")
                else:
                    print(f"Veri yok: {full_url}")

                time.sleep(2)  # Sunucuyu yormamak için bekleme

        return collected_data

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return collected_data

def main():
    """Tüm sayfalardaki ilanları toplar ve verileri anında işler."""
    all_house_data = []
    page = 1

    while len(all_house_data) < MAX_LISTINGS:
        print(f"\nScraping page {page}...")
        page_url = f"{START_URL}?page={page}"

        all_house_data = scrape_links_and_fetch_data(page_url, all_house_data)

        if len(all_house_data) >= MAX_LISTINGS:
            break  # İstenilen sayıya ulaşıldıysa dur

        page += 1

    print(f"Toplam {len(all_house_data)} ilan bilgisi toplandı.")

    # Excel dosyasına yazma işlemi
    df = pd.DataFrame(all_house_data)
    df.to_excel("ilanlar2.xlsx", index=False)

    print("İlan bilgileri 'ilanlar.xlsx' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
