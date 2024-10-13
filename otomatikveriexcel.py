from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = 'https://books.toscrape.com/'
START_URL = f'{BASE_URL}catalogue/page-1.html'
BOOK_LIMIT = 500  # Alınacak toplam kitap sayısı


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

    return {
        'Title': title,
        'Price': price,
        'UPC': upc,
        'Product Type': product_type
    }


def scrape_books_from_page(url):
    """Bir sayfadaki tüm kitapların bilgilerini alır."""
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    book_data = []
    for book in books:
        relative_url = book.h3.a['href'].replace('../../../', '')
        book_url = f"{BASE_URL}catalogue/{relative_url}"

        # Kitap bilgilerini al ve listeye ekle
        book_details = get_book_details(book_url)
        book_data.append(book_details)

    return book_data


def scrape_all_pages():
    """Tüm sayfalardaki kitap bilgilerini tarar ve bir Excel dosyasına kaydeder."""
    all_books = []
    page_num = 1

    while True:
        url = f'{BASE_URL}catalogue/page-{page_num}.html'
        response = requests.get(url)

        if response.status_code != 200:
            print("Tüm sayfalar tarandı.")
            break

        print(f"=== Sayfa {page_num} Tarandı ===")
        books = scrape_books_from_page(url)
        all_books.extend(books)

        # Toplam kitap sayısını kontrol et
        if len(all_books) >= BOOK_LIMIT:
            print(f"Toplam {BOOK_LIMIT} kitap alındı.")
            all_books = all_books[:BOOK_LIMIT]  # Sadece 500 kitaba kadar kısıtla
            break

        page_num += 1

    # Verileri Excel'e kaydet
    df = pd.DataFrame(all_books)
    df.to_excel('books_data.xlsx', index=False)
    print("Kitap bilgileri 'books_data.xlsx' dosyasına kaydedildi.")


# Tüm kitapları çek ve kaydet
scrape_all_pages()
