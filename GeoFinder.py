import pandas as pd
import folium
from folium.plugins import MarkerCluster

map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',  
    zoom_start=13
)
map.add_child(folium.LatLngPopup())

df = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
schools = df[df['addr'].str.contains('г. Новокузнецк', na=False)]

school_cluster = MarkerCluster(name='Школы').add_to(map)

for _, row in schools.iterrows():
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

folium.LayerControl().add_to(map)

df1 = pd.read_csv('UDO.csv', encoding='windows-1251')
udo = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)]

udo_cluster = MarkerCluster(name='Учреждения доп. образования').add_to(map)

for _, row in udo.iterrows():
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

folium.LayerControl().add_to(map)

map.save('map.html')
