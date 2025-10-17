import pandas as pd
import folium
from folium.plugins import MarkerCluster

def find_column(df, candidates):
    """Вернуть первое имя столбца из candidates, которое есть в df, иначе None."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

def load_csv(path):
    try:
        df = pd.read_csv(path, encoding='windows-1251')
    except Exception as e:
        
        try:
            df = pd.read_csv(path, encoding='utf-8')
        except Exception:
            raise e
    return df

df_schools = load_csv('Rus_schools_final.csv')
df_udo = load_csv('UDO.csv')

print("Колонки schools:", list(df_schools.columns))
print("Колонки УДО:", list(df_udo.columns))

addr_candidates = ['addr', 'address', 'Адрес', 'ADDRESS', 'addr.']
addr_col_schools = find_column(df_schools, addr_candidates)
addr_col_udo = find_column(df_udo, addr_candidates)

if not addr_col_schools:
    print("В schools не найден столбец адреса. Доступные колонки:", df_schools.columns.tolist())
else:
    print("Использую колонку адреса для schools:", addr_col_schools)

if not addr_col_udo:
    print("В УДО не найден столбец адреса. Доступные колонки:", df_udo.columns.tolist())
else:
    print("Использую колонку адреса для УДО:", addr_col_udo)

lat_candidates = ['lat', 'latitude', 'LAT', 'y', 'широта', 'Latitude']
lon_candidates = ['lon', 'lng', 'long', 'LON', 'x', 'долгота', 'Longitude']

lat_col_schools = find_column(df_schools, lat_candidates)
lon_col_schools = find_column(df_schools, lon_candidates)

lat_col_udo = find_column(df_udo, lat_candidates)
lon_col_udo = find_column(df_udo, lon_candidates)

print("Широта/долгота schools:", lat_col_schools, lon_col_schools)
print("Широта/долгота УДО:", lat_col_udo, lon_col_udo)

def prepare_df(df, addr_col, lat_col, lon_col, name_fallback):
    if addr_col is None:
        df['__addr__'] = ''
        addr_col = '__addr__'

    if lat_col is None or lon_col is None:
        for col in df.columns:
            if any(x in col.lower() for x in ['coord', 'geom', 'point']):
                def parse_coord(val):
                    try:
                        s = str(val)
                        s = s.replace('(', ' ').replace(')', ' ').replace(';', ',')
                        parts = [p.strip() for p in s.replace(',', ' ').split() if p.strip()]
                        if len(parts) >= 2:
                            return float(parts[0]), float(parts[1])
                    except:
                        return None
                coords = df[col].apply(parse_coord)
                
                if coords.dropna().shape[0] > 0:
                    df['_parsed_lat'] = coords.apply(lambda x: x[0] if x else None)
                    df['_parsed_lon'] = coords.apply(lambda x: x[1] if x else None)
                    lat_col = '_parsed_lat'
                    lon_col = '_parsed_lon'
                    print(f"Парсим координаты из колонки {col}")
                    break

    if lat_col in df.columns:
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    if lon_col in df.columns:
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    if lat_col in df.columns and lon_col in df.columns:
        df = df.dropna(subset=[lat_col, lon_col])
    else:
        print(f"Внимание: не удалось найти обе колонки координат для {name_fallback}. Будет пустой набор.")
        df = df.iloc[0:0]
        
    if addr_col in df.columns and df.shape[0] > 0:
        try:
            df = df[df[addr_col].astype(str).str.contains('г. Новокузнецк', na=False)]
        except Exception as e:
            print("Ошибка при фильтрации по адресу:", e)
    return df, addr_col, lat_col, lon_col

schools_nk, addr_col_schools, lat_col_schools, lon_col_schools = prepare_df(
    df_schools, addr_col_schools, lat_col_schools, lon_col_schools, 'schools'
)
udo_nk, addr_col_udo, lat_col_udo, lon_col_udo = prepare_df(
    df_udo, addr_col_udo, lat_col_udo, lon_col_udo, 'УДО'
)

print("После подготовки: школы:", len(schools_nk), "записей; УДО:", len(udo_nk), "записей")

m = folium.Map(location=[53.7578, 87.1361], control_scale=True, tiles='OpenStreetMap', zoom_start=13)
m.add_child(folium.LatLngPopup())

school_cluster = MarkerCluster(name='Школы').add_to(m)
udo_cluster = MarkerCluster(name='УДО').add_to(m)

for _, row in schools_nk.iterrows():
    lat = row[lat_col_schools]
    lon = row[lon_col_schools]
    name = row.get('name') if 'name' in row.index else row.get('название', 'Школа')
    address = row.get(addr_col_schools, '')
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="green")
    ).add_to(school_cluster)

for _, row in udo_nk.iterrows():
    lat = row[lat_col_udo]
    lon = row[lon_col_udo]
    name = row.get('name') if 'name' in row.index else row.get('название', 'УДО')
    address = row.get(addr_col_udo, '')
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>{address}",
        tooltip=name,
        icon=folium.Icon(color="blue")
    ).add_to(udo_cluster)

folium.LayerControl().add_to(m)
m.save('map_udo_schools_fixed.html')

