from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://books.toscrape.com/'
START_URL = f'{BASE_URL}catalogue/page-1.html'

def get_book_details(book_url):
    """Kitap detay sayfasındaki ismi, fiyatı, UPC ve Product Type bilgilerini alır."""
    html_text = requests.get(book_url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # Kitap ismini sayfa başlığından al
    title = soup.h1.text.strip()

    # Fiyat, UPC ve Product Type bilgilerini tablo üzerinden al
    product_info = soup.find('table', class_='table table-striped')
    details = {row.th.text.strip(): row.td.text.strip() for row in product_info.find_all('tr')}

    price = details.get('Price (incl. tax)', 'N/A')
    upc = details.get('UPC', 'N/A')
    product_type = details.get('Product Type', 'N/A')

    return title, price, upc, product_type

def scrape_books_from_page(url):
    """Bir sayfadaki tüm kitapların bilgilerini çeker."""
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for book in books:
        relative_url = book.h3.a['href'].replace('../../../', '')
        book_url = f"{BASE_URL}catalogue/{relative_url}"

        # Kitap bilgilerini al
        title, price, upc, product_type = get_book_details(book_url)

        # Bilgileri ekrana yazdır
        print(f"\nKitap: {title}")
        print(f"Fiyat: {price}")
        print(f"UPC: {upc}")
        print(f"Product Type: {product_type}")

def scrape_all_pages():
    """Tüm sayfalardaki kitapları tarar."""
    page_num = 1
    while True:
        url = f'{BASE_URL}catalogue/page-{page_num}.html'
        response = requests.get(url)

        if response.status_code != 200:
            print("Tüm sayfalar tarandı.")
            break

        print(f"\n=== Sayfa {page_num} Tarandı ===")
        scrape_books_from_page(url)
        page_num += 1

# Tüm kitapları çek
scrape_all_pages()
