import Distrcit_Coords
import pandas as pd
import folium
from folium.plugins import MarkerCluster

map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',
    zoom_start=10.5
)
map.add_child(folium.LatLngPopup())

df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
df2 = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)]

school_cluster = MarkerCluster(name='Школы').add_to(map)
udo_cluster = MarkerCluster(name="Учереждения доп. образования").add_to(map)

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

for _, row in df2.iterrows():
    lat = row['lat']
    lon = row['lon']
    name = row.get('name', 'Учереждения доп. образования')
    address = row.get('addr', '')

    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="blue", icon="graduation-cap", prefix='fa')
    ).add_to(school_cluster)

folium.Polygon(
    locations=Distrcit_Coords.polygon4,
    popup="Центральный район: Плотность населения - 2504 человек на км².\tРейтинг уровня доступности УДО: 4.9/5★",
    color="",
    fill=True,
    fill_color="orange",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon1,
    popup="Новоильинский район: Плотность населения - 3450 человек на км².\tРейтинг уровня доступности УДО: 4.4/5★",
    color="",
    fill=True,
    fill_color="green",
    fill_opacity=0.3,
    tooltip = "Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon6,
    popup="Куйбышевский район: Плотность населения - 812 человек на км².\tРейтинг уровня доступности УДО: 4.1/5★",
    color="",
    fill=True,
    fill_color="darkblue",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon2,
    popup="Заводский район: Плотность населения - 848 человек на км².\tРейтинг уровня доступности УДО: 3.8/5★",
    color="",
    fill=True,
    fill_color="purple",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon3,
    popup="Кузнецкий район: Плотность населения - 1299 человек на км².\tРейтинг уровня доступности УДО: 3.5/5★",
    color="",
    fill=True,
    fill_color="red",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации",
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon5,
    popup="Орджоникидзевский район: Плотность населения - 821 человек на км².\tРейтинг уровня доступности УДО: 3.0/5★",
    color="",
    fill=True,
    fill_color="yellow",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

map.save('map.html')
