from bs4 import BeautifulSoup
import requests

# Web sayfasını al ve HTML içeriğini ayrıştır
html_text = requests.get('https://books.toscrape.com/').text
soup = BeautifulSoup(html_text, 'lxml')

# Kitapları seç ve her bir kitap için bilgileri al
books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

print(f"{len(books)} adet kitap bulundu.\n")

for index, book in enumerate(books, 1):
    # Kitap adı
    title = book.h3.a['title']

    # Fiyat
    price = book.find('p', class_='price_color').text.strip()

    # Stok durumu
    availability = book.find('p', class_='instock availability').text.strip()

    # Kitap sayfasının URL'si
    relative_url = book.h3.a['href']
    full_url = f"https://books.toscrape.com/{relative_url}"

    # Sonuçları ekrana yazdır
    print(f"{index}. Kitap: {title}")
    print(f"   Fiyat: {price}")
    print(f"   Stok Durumu: {availability}")
    print(f"   URL: {full_url}\n")
