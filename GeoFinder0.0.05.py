import District_Coords
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
from branca.element import Template, MacroElement  # нужно для вставки HTML в карту


def calculate_distance(row, udo_location):  # функция для подсчёта дистанции между школой и УДО
    return geodesic((row['lat'], row['lon']), udo_location).kilometers


# Создание карты
map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',
    zoom_start=10.5
)
map.add_child(folium.LatLngPopup())

# Загрузка данных
df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)].copy()

# Кластеры
udo_cluster = MarkerCluster(name="Учреждения доп. образования").add_to(map)
schools_near_cluster = MarkerCluster(name="Школы в радиусе 3 км от УДО").add_to(map)
schools_far_cluster = MarkerCluster(name="Школы вне радиуса 3 км от УДО").add_to(map)

added_nearby_schools = set()
far_schools = set()

# Маркеры УДО
for _, udo_row in udo.iterrows():
    folium.Marker(
        location=[udo_row['lat'], udo_row['lon']],
        popup=f"<b>{udo_row['name']}</b>",
        icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa')
    ).add_to(udo_cluster)

# Расчёт расстояний
for _, udo_row in udo.iterrows():
    udo_location = (udo_row['lat'], udo_row['lon'])
    schools_temp = schools.copy()
    schools_temp['distance'] = schools_temp.apply(
        lambda row: calculate_distance(row, udo_location), axis=1
    )
    nearby_schools = schools_temp[schools_temp['distance'] <= 3]

    for _, school_row in nearby_schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}"
        if school_id not in added_nearby_schools:
            added_nearby_schools.add(school_id)
            folium.Marker(
                location=[school_row['lat'], school_row['lon']],
                popup=f"<b>{school_row['name']}</b>",
                icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')
            ).add_to(schools_near_cluster)

# Школы вне радиуса
for _, school_row in schools.iterrows():
    school_id = f"{school_row['lat']}_{school_row['lon']}"
    if school_id not in added_nearby_schools:
        far_schools.add(school_id)
        folium.Marker(
            location=[school_row['lat'], school_row['lon']],
            popup=f"<b>{school_row['name']}</b>",
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(schools_far_cluster)

# Добавление полигонов районов
folium.Polygon(
    locations=District_Coords.polygon1,
    popup="Новоильинский район: Плотность населения - 3450 человек/км². Рейтинг доступности УДО: 4.4★",
    fill=True, fill_color="green", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon2,
    popup="Заводский район: Плотность населения - 848 человек/км². Рейтинг доступности УДО: 3.8★",
    fill=True, fill_color="purple", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon3,
    popup="Кузнецкий район: Плотность населения - 1299 человек/км². Рейтинг доступности УДО: 3.5★",
    fill=True, fill_color="red", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon4,
    popup="Центральный район: Плотность населения - 2504 человек/км². Рейтинг доступности УДО: 4.9★",
    fill=True, fill_color="orange", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon5,
    popup="Орджоникидзевский район: Плотность населения - 821 человек/км². Рейтинг доступности УДО: 3.0★",
    fill=True, fill_color="yellow", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.Polygon(
    locations=District_Coords.polygon6,
    popup="Куйбышевский район: Плотность населения - 812 человек/км². Рейтинг доступности УДО: 4.1★",
    fill=True, fill_color="darkblue", fill_opacity=0.3,
    tooltip="Нажмите для подробной информации"
).add_to(map)

folium.LayerControl().add_to(map)

# --- 💡 ДОБАВЛЕНИЕ ЛЕГЕНДЫ ---
legend_html = """
{% macro html(this, kwargs) %}

<div style="
    position: fixed; 
    bottom: 30px; left: 30px; width: 250px; 
    background-color: white;
    border: 2px solid #666;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    z-index: 9999;
    font-size: 14px;
">
    <h4 style="margin-top: 0; text-align: center;">Легенда карты</h4>
    <p style="margin:4px 0;">
        <i class="fa fa-graduation-cap" style="color:green"></i>
        &nbsp;Школы в радиусе 3 км от УДО
    </p>
    <p style="margin:4px 0;">
        <i class="fa fa-graduation-cap" style="color:blue"></i>
        &nbsp;Учреждения доп. образования
    </p>
    <p style="margin:4px 0;">
        <i class="fa fa-graduation-cap" style="color:red"></i>
        &nbsp;Школы вне радиуса 3 км от УДО
    </p>
</div>

{% endmacro %}
"""

legend = MacroElement()
legend._template = Template(legend_html)
map.get_root().add_child(legend)
# --- конец вставки легенды ---

# Сохранение карты
map.save('map.html')

# Статистика в консоль
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
