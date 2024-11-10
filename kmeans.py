import pandas as pd

# Veriyi yükleme
df = pd.read_excel('temizlenmis_ilanlar.xlsx')

# Kira Ücreti sütununu seçme
kira_ucreti = df['Kira Ücreti']

# IQR hesaplama
Q1 = kira_ucreti.quantile(0.25)
Q3 = kira_ucreti.quantile(0.75)
IQR = Q3 - Q1

# Aykırı değerleri belirleme
alt_sinir = Q1 - 1.5 * IQR
ust_sinir = Q3 + 1.5 * IQR

# Aykırı değerleri temizleme
df_temiz = df[(kira_ucreti >= alt_sinir) & (kira_ucreti <= ust_sinir)]

# Temizlenmiş veriyi kaydetme
df_temiz.to_excel('temizlenmis_ilanlar_temiz.xlsx', index=False)

# Sonuçları kontrol etme
print(f"Temizlenmiş veri sayısı: {df_temiz.shape[0]}")
print(f"Aykırı değer sayısı: {df.shape[0] - df_temiz.shape[0]}")


