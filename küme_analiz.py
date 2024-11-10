import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_excel('/Users/minel/PycharmProjects/WEBKAZIMA/temizlenmis_ilanlar_temiz.xlsx')

# Select the "Kira Ücreti" column for clustering
prices = df[['Kira Ücreti']]

# Apply KMeans clustering to categorize into 3 clusters: cheap, medium, expensive
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(prices)

# Map the cluster labels to meaningful categories
cluster_map = {0: 'Ucuz', 1: 'Pahalı', 2: 'Orta'}
df['Kategori'] = df['Cluster'].map(cluster_map)

# Get statistics for each cluster
cluster_summary = df.groupby('Kategori')['Kira Ücreti'].agg(['count', 'min', 'max', 'mean', 'std'])

# Print the summary statistics for each category
print("Kümeleme Sonuçları:")
print(cluster_summary)

# Plot histograms for each cluster
plt.figure(figsize=(15, 5))
for i, (label, color) in enumerate(zip(['Ucuz', 'Orta', 'Pahalı'], ['blue', 'green', 'red'])):
    plt.subplot(1, 3, i + 1)
    sns.histplot(df[df['Kategori'] == label]['Kira Ücreti'], kde=True, color=color, bins=15)
    plt.title(f'{label} Kategorisi')
    plt.xlabel('Kira Ücreti')
    plt.ylabel('Frekans')

plt.tight_layout()
plt.show()

# Generate a report summary
print("\nPiyasa Analizi Raporu:")
for category in cluster_summary.index:
    count = cluster_summary.loc[category, 'count']
    min_price = cluster_summary.loc[category, 'min']
    max_price = cluster_summary.loc[category, 'max']
    mean_price = cluster_summary.loc[category, 'mean']
    std_dev = cluster_summary.loc[category, 'std']

    print(f"\n{category} Kategorisi:")
    print(f"- Nesne Sayısı: {count}")
    print(f"- En Düşük Kira Ücreti: {min_price}")
    print(f"- En Yüksek Kira Ücreti: {max_price}")
    print(f"- Ortalama Kira Ücreti: {mean_price:.2f}")
    print(f"- Standart Sapma: {std_dev:.2f}")
    print(f"- {category} Kira Ücreti aralığına göre toplam {count} ilan bulunmaktadır.")
