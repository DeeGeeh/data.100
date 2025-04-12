import numpy as np
import matplotlib.pyplot as plt
import csv
import math

def deg2num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    return x, y

def busLines(busfn, mapfn, zoom, ulX, ulY):
    # Lue karttatiedosto numpy-taulukkoon
    map_img = plt.imread(mapfn)
    
    # Lue linja-autojen paikkatiedot
    bus_data = {}
    with open(busfn, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            line = row['line']
            lat, lon = float(row['lat']), float(row['lon'])
            if line not in bus_data:
                bus_data[line] = []
            bus_data[line].append((lat, lon))
    
    # Käytä vain ensimmäistä kahta linjaa
    lines = list(bus_data.keys())[:2]
    colors = [(1, 0, 0, 1), (0, 0, 1, 1)]  # Punainen ja sininen
    
    for i, line in enumerate(lines):
        color = colors[i]
        for lat, lon in bus_data[line]:
            x_tile, y_tile = deg2num(lat, lon, zoom)
            x_pixel = round((x_tile - ulX) * 256)
            y_pixel = round((y_tile - ulY) * 256)
            
            # Piirretään 5x5 ruutu
            if 0 <= y_pixel < map_img.shape[0] and 0 <= x_pixel < map_img.shape[1]:
                map_img[max(0, y_pixel-2):min(map_img.shape[0], y_pixel+3),
                        max(0, x_pixel-2):min(map_img.shape[1], x_pixel+3)] = color
    
    return map_img
