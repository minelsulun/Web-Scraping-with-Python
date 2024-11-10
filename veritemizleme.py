import pandas as pd

# Örnek dosyanızı yükleyin
df = pd.read_excel("ilanlar4.xlsx")

# "Kira Ücreti" sütununu temizleme işlemi: "TL" kısmını çıkar ve nokta olmadan sayıya çevir
df['Kira Ücreti'] = df['Kira Ücreti'].str.replace(' TL', '').str.replace('.', '', regex=False).astype(float)

# "Depozito" sütunundaki boş (NaN) değerleri "Yok" olarak doldur
df['Depozito'] = df['Depozito'].fillna('Yok')

# "Takas" sütununu veri setinden çıkart
df = df.drop(columns=['Takas'])

# Diğer tüm sütunlardaki boş (NaN) değerleri "Belirtilmemiş" olarak doldur
df = df.fillna('Belirtilmemiş')

# Sonuçları gözden geçirmek için veriyi kontrol edin
print(df.head())

# Temizlenmiş veriyi kaydedin
df.to_excel("temizlenmis_ilanlar.xlsx", index=False)
