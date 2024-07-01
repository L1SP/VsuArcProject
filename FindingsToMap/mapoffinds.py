import folium
import folium.plugins as plugins
import pandas as pd
import re
import os
import cv2
import sys

# Получение ширины       
def extract_geo_lat(text):
    match = re.search(r'geo_lat":"([0-9]+\.[0-9]+)', text)
    if match:
        return float(match.group(1))

# Получение долготы
def extract_geo_lon(text):
    match = re.search(r'geo_lon":"([0-9]+\.[0-9]+)', text)
    if match:
        return float(match.group(1))
        
def map_of_finds(csv_path, img_path, name_html):
    coord = [51.660, 39.200] # Начальные координаты
    my_map = folium.Map(location = coord, zoom_start = 9) # Создаем карту
    mcg = plugins.MarkerCluster(control=False) # Добавляем кластеры маркеров
    my_map.add_child(mcg)
    df = pd.read_csv(csv_path) # Открываем таблицу

    df['object_geodata'] = df['object_geodata'].astype(str)
    df['latitude'] = df['object_geodata'].apply(extract_geo_lat)
    df['longitude'] = df['object_geodata'].apply(extract_geo_lon)

    for index, row in df.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            name = row['object_name']
            size = row['object_size']
            obj_id = row['object_id']
            image = re.search(fr"{obj_id}\.jpg", str(row['object_media']))
            if image:
                img = cv2.imread(fr'{img_path}/{image.group(0)}')
                width, height, channels = img.shape
                if width > height: # Подбираем размер изображения
                    html = f"""<p>Наименование: {name}</p>
                <p>Размер: {size}</p>
                <img src='{img_path}/{image.group(0)}' alt='Изображение находки' width = '100' />"""
                else:
                    html = f"""<p>Наименование: {name}</p>
                <p>Размер: {size}</p>
                <img src='{img_path}/{image.group(0)}' alt='Изображение находки' height = '100' />"""
            else:
                html = f"""<p>Наименование: {name}</p>
            <p>Размер: {size}</p>"""
        
            marker = folium.Marker([row['latitude'], row['longitude']], tooltip=row['object_name'], popup=folium.Popup(html, max_width=500),  icon=folium.Icon(color="green"))
            marker.add_to(mcg)
			
    my_map.save(name_html)

if len(sys.argv) == 3:
    map_of_finds(sys.argv[1], sys.argv[2], "mapoffinds.html")
elif len(sys.argv) == 4:
    map_of_finds(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) > 4:
    map_of_finds(sys.argv[1], sys.argv[2], sys.argv[3], False)
else:
    print("python3 mapoffinds.py имя_таблицы_csv имя_папки_с_изображениями [имя карты знак заголовка]")
