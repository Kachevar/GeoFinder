import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def calculate_distance(row, udo_location):
    return geodesic((row['lat'], row['lon']), udo_location).kilometers

map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',  
    zoom_start=10.5
) #создание карты
map.add_child(folium.LatLngPopup())

df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251') #создаем дата-фрейм df1
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';') #создаем дата-фрейм udo
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)].copy() #находим все школы в горде Новокузнецк, путем фильтрации дата-фрейма df1

udo_cluster = MarkerCluster(name="Учреждения доп. образования").add_to(map) #создаём MarkerCluster для Учереждений доп. образования
schools_cluster = MarkerCluster(name="Школы").add_to(map) #создаём MarkerCluster для школ

added_schools = set() #сюда сохраняются школы, находящиеся в радиусе 3км от каждого УДО

for _, udo_row in udo.iterrows(): #создаём Marker'ы Учереждений Доп. Образования для последующего вывода на карту
    folium.Marker(
        location=[udo_row['lat'], udo_row['lon']],
        popup=f"<b>{udo_row['name']}</b>",
        icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa')
    ).add_to(udo_cluster)

for _, udo_row in udo.iterrows(): #находим все школы в радиусе 3км от каждого УДО для их последующего сохранения в added_schools
    udo_location = (udo_row['lat'], udo_row['lon'])

    schools_temp = schools.copy() #считаем растояние каждой школы до каждого УДО для нахождения ближайших школ для каждого УДО
    schools_temp['distance'] = schools_temp.apply(
        lambda row: calculate_distance(row, udo_location), 
        axis=1
    )

    nearby_schools = schools_temp[schools_temp['distance'] <= 3] #сохраняем только школы в пределах 3км от их блежайшего УДО

    for _, school_row in nearby_schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}"
        
        if school_id not in added_schools: #создаём Marker'ы школ для последующего вывода на карту
            added_schools.add(school_id)
            
            folium.Marker(
                location=[school_row['lat'], school_row['lon']],
                popup=f"<b>{school_row['name']}</b>",
                icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')
            ).add_to(schools_cluster)

folium.LayerControl().add_to(map) #выводим все нужные объекты на карту

map.save('map.html') #сохранение итоговой карты
