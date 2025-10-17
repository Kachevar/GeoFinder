import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic       

def fromudo_to_distance(row):
  return geodesic((row['lat'], row['lon']), location).kilometers

map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',  
    zoom_start=10.5
)
map.add_child(folium.LatLngPopup())

df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)].copy()

school_cluster = MarkerCluster(name='Школы').add_to(map)
udo_cluster = MarkerCluster(name="Учереждения доп. образования").add_to(map)

for _, row in udo.iterrows():
    lat = row['lat']
    lon = row['lon']
    name = row.get('name', 'Учереждения доп. образования')
    address = row.get('addr', '')
    location=[lat, lon]

    folium.Marker(
        location=location,
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="blue", icon="graduation-cap", prefix='fa')
    ).add_to(school_cluster)

    for _, row in schools.iterrows():
      schools['distance'] = schools.apply(fromudo_to_distance, axis=1)
      filtered_schools = schools[schools['distance'] <= 3]
      name = filtered_schools.get('name', 'Школа')
      address = filtered_schools.get('addr', '')

      for _,row in filtered_schools.iterrows():
        folium.Marker(
          location=[lat, lon],
          popup=f"<b>{name}</b><br>{address}",
          tooltip=name,
          icon=folium.Icon(color="green", icon="graduation-cap", prefix='fa')
      ).add_to(school_cluster)

folium.LayerControl().add_to(map)

map.save('map.html')
