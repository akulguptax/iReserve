from calendar import c
from flask import render_template, make_response
from .utils import is_logged_in, get_user
from sqlalchemy import text
import folium
from IPython.display import HTML 
import pandas as pd

def create_map(db):
    # Make an empty map
    m = folium.Map(location=[40.104, -88.228], tiles="OpenStreetMap", zoom_start=15.4)

    reservations = db.engine.execute("SELECT `BuildingName`, COUNT(`BuildingName`) AS res_count FROM `reservation` NATURAL JOIN `room` NATURAL JOIN `building` GROUP BY `BuildingName` ORDER BY `BuildingName`;")
    buildings = []
    counts = []

    for r in reservations:
        counts.append(r.res_count)
        buildings.append(r.BuildingName)
    
    print(counts)
    print(buildings)

    print(len(counts), len(buildings))
    
    data = pd.DataFrame({

        
   'lon':[-88.22109242320069, -88.23794140241456, -88.22091966008513, -88.23807960980253, -88.23700284474393, -88.22156030241462, -88.21975670241463, -88.23672557542628, -88.22097176008491, -88.2203734177558, -88.22170149985071, -88.23820096008505, -88.23523598707338],
   'lat':[40.09974605333407, 40.10197021567408, 40.10046314622389, 40.10261431404243, 40.10408160408148, 40.099138743373366, 40.099819894094225, 40.10199850531534, 40.11026515619361, 40.09913563653867, 40.10958999761764, 40.10399018569615, 40.103306624966976],
   'name': buildings,
   'value': counts
    }, dtype=str)

    # add marker one by one on the map
    for i in range(0,len(data)):

        name_of_building = data.iloc[i]['name']

        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup="{}: {}".format(name_of_building, data.iloc[i]['value']),
            radius=float(data.iloc[i]['value'])/85,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)

    # Save map  
    m.save('templates/map.html')