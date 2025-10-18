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
    locations=Distrcit_Coords.polygon1,
    popup="Новоильинский район: Плотность населения - 3450 человек на км².\tРейтинг доступности УДО: 4.4/5★",
    color="",
    fill=True,
    fill_color="green",
    fill_opacity=0.3,
    tooltip = "Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon2,
    popup="Заводский район: Плотность населения - 848 человек на км².\tРейтинг доступности УДО: 3.8/5★",
    color="",
    fill=True,
    fill_color="purple",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon3,
    popup="Кузнецкий район: Плотность населения - 1299 человек на км².\tРейтинг доступности УДО: 3.5/5★",
    color="",
    fill=True,
    fill_color="red",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации",
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon4,
    popup="Центральный район: Плотность населения - 2504 человек на км².\tРейтинг доступности УДО: 4.9/5★",
    color="",
    fill=True,
    fill_color="orange",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon5,
    popup="Орджоникидзевский район: Плотность населения - 821 человек на км².\tРейтинг доступности УДО: 3.0/5★",
    color="",
    fill=True,
    fill_color="yellow",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=Distrcit_Coords.polygon6,
    popup="Куйбышевский район: Плотность населения - 812 человек на км².\tРейтинг доступности УДО: 4.1/5★",
    color="",
    fill=True,
    fill_color="darkblue",
    fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map) # выводи все объекты на карту
map.save('map.html')

with open('map.html', 'r+', encoding='utf-8') as file:
    content = file.read()
    
    font_awesome = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
    content = content.replace('</head>', font_awesome + '</head>')
    
    far_schools_count = len(schools) - len(added_nearby_schools)
    
    legend_html = """
    <div style="position: absolute; bottom: 20px; left: 20px; background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.3); z-index: 1000; max-width: 350px;">
        <h4 style="margin-top: 0;">Легенда карты:</h4>
        <p><i class="fa fa-graduation-cap" style="color: green; margin-right: 8px;"></i> Школы в радиусе 3 км от УДО</p>
        <p><i class="fa fa-graduation-cap" style="color: red; margin-right: 8px;"></i> Школы вне радиуса 3 км от УДО</p>
        <p><i class="fa fa-graduation-cap" style="color: blue; margin-right: 8px;"></i> Учреждения дополнительного образования</p>
    </div>
    """
    
    stats_html = f"""
    <div id="statistics" style="width: 100%; background: white; padding: 30px; box-sizing: border-box; border-top: 2px solid #ddd; margin-top: 20px;">
        <h3 style="text-align: center; margin-top: 0;">СТАТИСТИКА ШКОЛ НОВОКУЗНЕЦКА</h3>
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 25px;">
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #2c3e50;">110</div>
                <div style="font-size: 14px;">Всего школ</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #27ae60;">{len(added_nearby_schools)}</div>
                <div style="font-size: 14px;">В радиусе 3 км от УДО</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #e74c3c;">9</div>
                <div style="font-size: 14px;">Вне радиуса 3 км от УДО</div>
            </div>
        </div>
        
        <div style="display: flex; gap: 40px; justify-content: center;">
            <div style="flex: 1; max-width: 500px;">
                <h4 style="color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 8px;">
                    <i class="fa fa-check-circle" style="margin-right: 10px;"></i>
                    Школы в радиусе 3 км от УДО ({len(added_nearby_schools)})
                </h4>
                <div style="max-height: 400px; overflow-y: auto; padding: 10px;">
    """
    
    for school_id in added_nearby_schools:
        lat, lon = school_id.split('_')
        school_info = schools[(schools['lat'] == float(lat)) & (schools['lon'] == float(lon))].iloc[0]
        stats_html += f"<p style='margin: 8px 0; padding: 5px; background: #f8fff8; border-left: 3px solid #27ae60;'><i class='fa fa-school' style='color: #27ae60; margin-right: 10px;'></i>{school_info['name']}</p>"
    
    stats_html += """
                </div>
            </div>
            <div style="flex: 1; max-width: 500px;">
                <h4 style="color: #e74c3c; border-bottom: 2px solid #e74c3c; padding-bottom: 8px;">
                    <i class="fa fa-exclamation-triangle" style="margin-right: 10px;"></i>
                    Школы вне радиуса 3 км от УДО (9)
                </h4>
                <div style="max-height: 400px; overflow-y: auto; padding: 10px;">
    """
    
    for _, school_row in schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}"
        if school_id not in added_nearby_schools:
            stats_html += f"<p style='margin: 8px 0; padding: 5px; background: #fff8f8; border-left: 3px solid #e74c3c;'><i class='fa fa-school' style='color: #e74c3c; margin-right: 10px;'></i>{school_row['name']}</p>"
    
    stats_html += """
                </div>
            </div>
        </div>
    </div>
    """
    
    content = content.replace('</body>', legend_html + '</body>')
    
    if '</body>' in content:
        body_end = content.find('</body>')
        content = content[:body_end] + stats_html + content[body_end:]
    
    file.seek(0)
    file.write(content)
    file.truncate()
