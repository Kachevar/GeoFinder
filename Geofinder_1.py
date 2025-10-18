# импортируем необходимые для работы программы модули
import District_Coords
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def calculate_distance(row, udo_location): # функция для подсчёта дистанции между школой и УДО
    return geodesic((row['lat'], row['lon']), udo_location).kilometers

map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',  
    zoom_start=10.5
) # сама карта
map.add_child(folium.LatLngPopup())

# содание дата-фреймов обязательных файлов
df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)].copy()

# создание MarkerCluster'ов для объединения одинаковых объектов в группы
udo_cluster = MarkerCluster(name="Учреждения доп. образования").add_to(map)
schools_near_cluster = MarkerCluster(name="Школы в радиусе 3 км от УДО").add_to(map)
schools_far_cluster = MarkerCluster(name="Школы вне радиуса 3 км от УДО").add_to(map)

added_nearby_schools = set() # список для школ подходящих по условию
far_schools = set() # список для школ неподходящих по условию

for _, udo_row in udo.iterrows():
    folium.Marker(
        location=[udo_row['lat'], udo_row['lon']],
        popup=f"<b>{udo_row['name']}</b>",
        icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa')
    ).add_to(udo_cluster) # создание Marker'ов УДО

 # перебор координат всех УДО и подсчет расстояния от УДО до школ
for _, udo_row in udo.iterrows():
    udo_location = (udo_row['lat'], udo_row['lon'])
    
    schools_temp = schools.copy()
    schools_temp['distance'] = schools_temp.apply(
        lambda row: calculate_distance(row, udo_location), 
        axis=1
    )
    
    nearby_schools = schools_temp[schools_temp['distance'] <= 3] # нахождение школ входящих в радиус 3км
    
    for _, school_row in nearby_schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}" # перебираем координаты всех школ

        # добавляем ближайшую школу в список школ в радиусе 3км от УДО если ее там нет
        if school_id not in added_nearby_schools:
            added_nearby_schools.add(school_id) 
            
            folium.Marker(
                location=[school_row['lat'], school_row['lon']],
                popup=f"<b>{school_row['name']}</b>",
                icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')
            ).add_to(schools_near_cluster) # создание Marker'ов школ, входящих в радиус 3км от УДО

for _, school_row in schools.iterrows():
    school_id = f"{school_row['lat']}_{school_row['lon']}" # перебираем координаты всех школ
    
    #добавляем школу, находящуюся дальше 3км от УДО, в список школ, невходящих в радиус 3км от УДО, если ее там нету
    if school_id not in added_nearby_schools:
        far_schools.add(school_id)
        
        folium.Marker(
            location=[school_row['lat'], school_row['lon']],
            popup=f"<b>{school_row['name']}</b>",
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(schools_far_cluster) # создание Marker'ов школ, не входящих в радиус 3км от УДО

folium.Polygon(
    locations=District_Coords.polygon1,
    popup="Новоильинский район: Плотность населения - 3450 человек на км².\tРейтинг доступности УДО: 4.4/5★",
    color="",
    fill=True,
    fill_color="green",
    fill_opacity=0.3,
    tooltip = "Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon2,
    popup="Заводский район: Плотность населения - 848 человек на км².\tРейтинг доступности УДО: 3.8/5★",
    color="",
    fill=True,
    fill_color="purple",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map)

folium.Polygon(
    locations=District_Coords.polygon3,
    popup="Кузнецкий район: Плотность населения - 1299 человек на км².\tРейтинг доступности УДО: 3.5/5★",
    color="",
    fill=True,
    fill_color="red",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации",
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon4,
    popup="Центральный район: Плотность населения - 2504 человек на км².\tРейтинг доступности УДО: 4.9/5★",
    color="",
    fill=True,
    fill_color="orange",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon5,
    popup="Орджоникидзевский район: Плотность населения - 821 человек на км².\tРейтинг доступности УДО: 3.0/5★",
    color="",
    fill=True,
    fill_color="yellow",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon6,
    popup="Куйбышевский район: Плотность населения - 812 человек на км².\tРейтинг доступности УДО: 4.1/5★",
    color="",
    fill=True,
    fill_color="darkblue",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map) # выводи все объекты на карту
map.save('map.html') # сохраняем карту со всеми объектами

# вывод определений количества всех школ, количества школ в радиусе 3км, количества школ вне радиуса 3км от УДО, вывод всех школ в радиусе 3км от УДО, и вывод всех школ вне радиуса 3км от УДО
print("СТАТИСТИКА ШКОЛ:")
print("=" * 50)
print(f"Всего школ в Новокузнецке: {len(schools)}")
print(f"Школ в радиусе 3 км от УДО: {len(added_nearby_schools)}")
print(f"Школ вне радиуса 3 км от УДО: {len(far_schools)}")
print("=" * 50)
print("\nШколы в радиусе 3 км от УДО (зеленые):")
for school_id in added_nearby_schools:
    lat, lon = school_id.split('_')
    school_info = schools[(schools['lat'] == float(lat)) & (schools['lon'] == float(lon))].iloc[0]
    print(f"  - {school_info['name']}")

print("\nШколы вне радиуса 3 км от УДО (красные):")
for school_id in far_schools:
    lat, lon = school_id.split('_')
    school_info = schools[(schools['lat'] == float(lat)) & (schools['lon'] == float(lon))].iloc[0]
    print(f"  - {school_info['name']}")
