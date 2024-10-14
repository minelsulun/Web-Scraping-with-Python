from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

BASE_URL = 'https://www.hepsiemlak.com'
START_URL = f'{BASE_URL}/buca-kiralik'
HOUSE_LIMIT = 100  # Çekilecek toplam ilan sayısı

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}


def get_house_details(house_url):
    """Her ilan detay sayfasından başlık, fiyat, ilan no, metrekare ve oda sayısı gibi bilgileri alır."""
    try:
        response = requests.get(house_url, headers=HEADERS)
        response.raise_for_status()  # Hata durumunu yakala
        soup = BeautifulSoup(response.text, 'lxml')

        # İlan başlığı
        title = soup.find('h1', class_='fontRB').text.strip() if soup.find('h1', class_='fontRB') else 'N/A'

        # Fiyat bilgisi
        price = soup.find('p', class_='fontRB fz24 price').text.strip() if soup.find('p',
                                                                                     class_='fontRB fz24 price') else 'N/A'

        # İlan detayları (Metrekare, Oda Sayısı vb.)
        info_table = soup.find_all('li', class_='spec-item')
        details = {}

        for item in info_table:
            span = item.find('span')
            b = item.find('b')
            # span ve b öğelerinin olup olmadığını kontrol et
            if span and b:
                details[span.text.strip()] = b.text.strip()
            else:
                print("Some details are missing for an item.")

        area = details.get('Brüt Metrekare', 'N/A')
        rooms = details.get('Oda + Salon', 'N/A')
        listing_id = details.get('İlan No', 'N/A')

        return {
            'Title': title,
            'Price': price,
            'Area': area,
            'Rooms': rooms,
            'Listing ID': listing_id
        }
    except requests.RequestException as e:
        print(f"Error fetching {house_url}: {e}")
        return None


def scrape_houses_from_page(url):
    """Bir sayfadaki tüm ilanların bilgilerini alır."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Burayı kendi sayfanızın HTML yapısına göre güncelleyin
        houses = soup.find_all('a', class_='card-link')  # Doğru sınıf adını kullanın

        house_data = []
        for house in houses:
            relative_url = house['href']
            house_url = f"{BASE_URL}{relative_url}"

            # İlan bilgilerini al ve listeye ekle
            details = get_house_details(house_url)
            if details:
                house_data.append(details)
                print(f"Fetched data for: {details['Title']}")

            # Sunucuyu fazla yormamak için bekleme
            time.sleep(2)  # Daha kısa bir süre deneyebilirsiniz

        return house_data
    except requests.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return []


def main():
    """Tüm sayfalardaki ilanları toplar ve CSV'ye kaydeder."""
    all_house_data = []
    page = 1

    while len(all_house_data) < HOUSE_LIMIT:
        print(f"Scraping page {page}...")
        page_url = f"{START_URL}?page={page}"
        houses = scrape_houses_from_page(page_url)

        if not houses:
            print("No more listings found or an error occurred.")
            break

        all_house_data.extend(houses)

        if len(houses) == 0:
            break  # Eğer sayfa boşsa çık

        page += 1

    # Verileri DataFrame'e dönüştürüp Excel olarak kaydetme
    df = pd.DataFrame(all_house_data)
    # Excel dosyasına kaydetme
    df.to_excel('hepsiemlak_listings.xlsx', index=False)
    print(f"Saved {len(all_house_data)} listings to 'hepsiemlak_listings.xlsx'.")


if __name__ == "__main__":
    main()
