import Distrcit_Coords
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
) # генерируем саму карту с обложкой "OpenStreetMap"
map.add_child(folium.LatLngPopup())

# принимаем нужные нам .csv файлы как дата-фреймы для дальнейшей работы с ними
schools_data = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = schools_data[schools_data['addr'].str.contains('г. Новокузнецк', na=False)] # ищем школы только в городе Новокузнецк

# генерируем маркер-кластеры для каждой группы объектов (учреждения доп. образования, школы подходящие по условию и школы неподходящие по условию)
udo_cluster = MarkerCluster(name="Учреждения доп. образования").add_to(map)
schools_near_cluster = MarkerCluster(name="Школы в радиусе 3 км от УДО").add_to(map)
schools_far_cluster = MarkerCluster(name="Школы вне радиуса 3 км от УДО").add_to(map)

# генерируем списки школ подходящих и неподходящих по условию
added_nearby_schools = set() # подходящие
far_schools = set() # неподходящие

# перебираем список учреждений доп. образования для их последующего вывода на карту
for _, udo_row in udo.iterrows():
    udo_location = (udo_row['lat'], udo_row['lon'])

    # содаём переменную для нахождения дистанции от школы до УДО
    schools_temp = schools.copy()
    schools_temp['distance'] = schools_temp.apply(
        lambda row: calculate_distance(row, udo_location),
        axis=1
    )

    nearby_schools = schools_temp[schools_temp['distance'] <= 3]  # нахождение школ входящих в радиус 3км

    for _, school_row in nearby_schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}"  # перебираем координаты всех школ

        # добавляем ближайшую школу в список школ в радиусе 3км от УДО если ее там нет
        if school_id not in added_nearby_schools:
            added_nearby_schools.add(school_id)

            folium.Marker(
                location=[school_row['lat'], school_row['lon']],
                popup=f"<b>{school_row['name']}</b>",
                icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')
            ).add_to(schools_near_cluster)  # создание Marker'ов школ, входящих в радиус 3км от УДО

for _, school_row in schools.iterrows():
    school_id = f"{school_row['lat']}_{school_row['lon']}"  # перебираем координаты всех школ

    # добавляем школу, находящуюся дальше 3км от УДО, в список школ, невходящих в радиус 3км от УДО, если ее там нету
    if school_id not in added_nearby_schools:
        far_schools.add(school_id)

        folium.Marker(
            location=[school_row['lat'], school_row['lon']],
            popup=f"<b>{school_row['name']}</b>",
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(schools_far_cluster)  # создание Marker'ов школ, не входящих в радиус 3км от УДО

    # генерация каждого района на карте с помощью полигонов
    folium.Polygon(
    locations=Distrcit_Coords.polygon1,
    popup="Новоильинский район: Плотность населения - 3450 человек на км²\tрейтинг доступности УДО: 4.4/5",
    color="",
    fill=True,
    fill_color="grey",
    fill_opacity=0.009,
    tooltip = "Нажмите для подробной информации"
).add_to(map) # Новоильинский район

folium.Polygon(
    locations=Distrcit_Coords.polygon2,
    popup="Заводской район: Плотность населения - 848 человек на км²\tрейтинг доступности УДО: 3.8/5",
    color="",
    fill=True,
    fill_color="purple",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map) # Заводской район

folium.Polygon(
    locations=Distrcit_Coords.polygon3,
    popup="Кузнецкий район: Плотность населения - 1299 человек на км²\tрейтинг доступности УДО: 3.5/5",
    color="",
    fill=True,
    fill_color="red",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации",
).add_to(map) # Кузнецкий район

folium.Polygon(
    locations=Distrcit_Coords.polygon4,
    popup="Центральный район: Плотность населения - 2504 человек на км²\tрейтинг доступности УДО: 4.9/5",
    color="",
    fill=True,
    fill_color="orange",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map) # Центральный район

folium.Polygon(
    locations=Distrcit_Coords.polygon5,
    popup="Орджоникидзевский район: Плотность населения - 821 человек на км²\tрейтинг доступности УДО: 3.0/5",
    color="",
    fill=True,
    fill_color="yellow",
    fill_opacity=0.2,
    tooltip="Нажмите для подробной информации"
).add_to(map) # Орджоникидзевский район

folium.Polygon(
    locations=Distrcit_Coords.polygon6,
    popup="Куйбышевский район: Плотность населения - 812 человек на км²\tрейтинг доступности УДО: 4.1/5",
    color="",
    fill=True,
    fill_color="darkblue",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map) # Куйбышевский район

folium.LayerControl().add_to(map) # добавление на карту интерактивных элементов управления, которые позволяют пользователям переключать видимость различных слоев данных

map.save('map.html')
