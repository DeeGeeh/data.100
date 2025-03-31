import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen, Request
from io import BytesIO


zoom = 4
fromX = 2
toX = 4
fromY = 5
toY = 6 

def getTile(zoom, x, y):
    endpoint = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    imgbytes = urlopen(Request(endpoint, 
                                headers={"User-Agent": "DATA.100 v1.0"})).read()
    return plt.imread(BytesIO(imgbytes))
    


def makeMap(zoom, fromX, toX, fromY, toY):
    rows = []
    
    for y in range(fromY, toY + 1):
        row = []
        for x in range(fromX, toX + 1):
            tile = getTile(zoom, x, y)
            row.append(tile)

        if row:
            rows.append(np.hstack(row))
    
    if rows:
        full_map = np.vstack(rows)
        return full_map
    
    return None

if __name__ == "__main__":
    makeMap(zoom, fromX, toX, fromY, toY)
