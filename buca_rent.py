import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Hedef URL (İzmir, Buca için filtrelenmiş URL'yi buraya yapıştır)
base_url = "https://www.hepsiemlak.com/izmir-buca-kiralik"

# Veriyi saklamak için boş bir liste oluştur
data = []

# 500 ilan çekmek için sayfa sayfa gez
for page in range(1, 11):  # 10 sayfa boyunca gez
    url = f"{base_url}?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # İlanları bul
    ilanlar = soup.find_all("div", class_="listing-item")

    for ilan in ilanlar:
        try:
            ilan_metni = ilan.find("h2", class_="listing-title").text.strip()
            mahalle = ilan.find("span", class_="listing-mahalle").text.strip()
            kira_bedeli = ilan.find("span", class_="listing-price").text.strip()

            # Veriyi listeye ekle
            data.append([ilan_metni, mahalle, kira_bedeli])
        except AttributeError:
            # Eğer bir bilgi bulunamazsa atla
            continue

    time.sleep(2)  # Sitenin engellememesi için bekleme süresi ekle

# Veriyi DataFrame'e çevir
df = pd.DataFrame(data, columns=["İlan Metni", "Mahalle", "Kira Bedeli (TL)"])

# Excel dosyasına kaydet
df.to_excel("buca_kiralik.xlsx", index=False)
print("Veri çekme işlemi tamamlandı ve Excel'e kaydedildi.")
print(f"{len(ilanlar)} adet ilan bulundu.")

