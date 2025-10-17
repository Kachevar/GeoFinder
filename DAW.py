import pandas as pd
import folium
from folium.plugins import MarkerCluster

# === 1. Создание карты с центром в Новокузнецке ===
map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',   # ← теперь используем OpenStreetMap
    zoom_start=13
)
map.add_child(folium.LatLngPopup())

# === 2. Загрузка данных ===
df_schools = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
df_udo = pd.read_csv('/mnt/data/УДО.csv', encoding='windows-1251')

# === 3. Фильтрация только по Новокузнецку ===
schools_nk = df_schools[df_schools['addr'].str.contains('г. Новокузнецк', na=False)]
udo_nk = df_udo[df_udo['addr'].str.contains('г. Новокузнецк', na=False)]

# === 4. Проверка данных (опционально) ===
print("Школы:\n", schools_nk.head(5))
print("\nУчреждения дополнительного образования (УДО):\n", udo_nk.head(5))

# === 5. Создание кластеров для разных типов учреждений ===
school_cluster = MarkerCluster(name='Школы').add_to(map)
udo_cluster = MarkerCluster(name='Учреждения доп. образования').add_to(map)

# === 6. Добавление школ ===
for _, row in schools_nk.iterrows():
    lat = row['lat']
    lon = row['lon']
    name = row.get('name', 'Школа')
    address = row.get('addr', '')

    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="green", icon="graduation-cap", prefix='fa')
    ).add_to(school_cluster)

# === 7. Добавление УДО ===
for _, row in udo_nk.iterrows():
    lat = row['lat']
    lon = row['lon']
    name = row.get('name', 'УДО')
    address = row.get('addr', '')

    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="blue", icon="book", prefix='fa')
    ).add_to(udo_cluster)

# === 8. Добавление панели слоёв ===
folium.LayerControl().add_to(map)

# === 9. Сохранение карты ===
map.save('map_udo_schools.html')
print("✅ Карта сохранена как map_udo_schools.html")
