import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def calculate_distance(row, udo_location):
    """Calculate distance between school and UDO location"""
    return geodesic((row['lat'], row['lon']), udo_location).kilometers

# Create map
map = folium.Map(
    location=[53.7578, 87.1361],
    control_scale=True,
    tiles='OpenStreetMap',  
    zoom_start=10.5
)
map.add_child(folium.LatLngPopup())

# Load data
df1 = pd.read_csv('Rus_schools_final.csv', encoding='windows-1251')
udo = pd.read_csv('UDO.csv', encoding="utf-8", sep=';')
schools = df1[df1['addr'].str.contains('г. Новокузнецк', na=False)].copy()

# Create clusters
udo_cluster = MarkerCluster(name="Учреждения доп. образования").add_to(map)
schools_near_cluster = MarkerCluster(name="Школы в радиусе 3 км от УДО").add_to(map)
schools_far_cluster = MarkerCluster(name="Школы вне радиуса 3 км от УДО").add_to(map)

# Store all unique schools within 3km of any UDO
added_nearby_schools = set()
far_schools = set()

# First, add all UDO markers
for _, udo_row in udo.iterrows():
    folium.Marker(
        location=[udo_row['lat'], udo_row['lon']],
        popup=f"<b>{udo_row['name']}</b>",
        icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa')
    ).add_to(udo_cluster)

# Find schools within 3km of any UDO
for _, udo_row in udo.iterrows():
    udo_location = (udo_row['lat'], udo_row['lon'])
    
    # Calculate distances to all schools for this UDO
    schools_temp = schools.copy()
    schools_temp['distance'] = schools_temp.apply(
        lambda row: calculate_distance(row, udo_location), 
        axis=1
    )
    
    # Filter schools within 3km
    nearby_schools = schools_temp[schools_temp['distance'] <= 3]
    
    # Add only unique schools that haven't been added yet
    for _, school_row in nearby_schools.iterrows():
        school_id = f"{school_row['lat']}_{school_row['lon']}"
        
        if school_id not in added_nearby_schools:
            added_nearby_schools.add(school_id)
            
            folium.Marker(
                location=[school_row['lat'], school_row['lon']],
                popup=f"<b>{school_row['name']}</b>",
                icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')
            ).add_to(schools_near_cluster)

# Add schools that are NOT within 3km of any UDO
for _, school_row in schools.iterrows():
    school_id = f"{school_row['lat']}_{school_row['lon']}"
    
    if school_id not in added_nearby_schools:
        far_schools.add(school_id)
        
        folium.Marker(
            location=[school_row['lat'], school_row['lon']],
            popup=f"<b>{school_row['name']}</b>",
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(schools_far_cluster)

# Add layer control
folium.LayerControl().add_to(map)

# Save map
map.save('map.html')

# Print statistics
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
