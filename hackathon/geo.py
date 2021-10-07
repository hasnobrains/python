import json
import sys
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from flask import Flask
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)


@app.route('/')
def index():

    geolocator = Nominatim(user_agent='russia_explorer')
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            data = json.load(f)
    except IOError:
        print(f"File {filename} not found!\n")
        return

    pretty = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty)

    df = pd.json_normalize(data['events'])
    #  print(df.info())

    # shrink whitespaces
    df.replace(np.nan, '', inplace=True)
    for index, row in df.iterrows():
        row['address.region'] = ' '.join((row['address.region']
                                          .split()))
        row['address.place'] = ' '.join((row['address.place']
                                         .split()))
        row['address.street'] = ' '.join((row['address.street']
                                          .split()))
        row['address.building'] = ' '.join((row['address.building']
                                            .split()))

        if row['coordinates.x'] == '' and row['coordinates.y'] == '':
            address = f"улица {row['address.street']} "
            address += f"{row['address.building']}, "
            address += f"{row['address.place']}, "
            address += f"{row['address.region']}"
            location = geolocator.geocode(address)
            df.loc[df['id'] == row['id'],
                   'coordinates.x'] = location.longitude
            df.loc[df['id'] == row['id'],
                   'coordinates.y'] = location.latitude

    folium_map = folium.Map(location=[55.0, 103.0], zoom_start=4)
    #  folium.GeoJson(
    #      '/Volumes/Second/Downloads/russia_geojson/admin_level_4.geojson',
    #      name="geojson").add_to(folium_map)
    # adding layers
    layer = {}
    for type in df['type'].drop_duplicates():
        layer[type] = folium.FeatureGroup(name=type)
        folium_map.add_child(layer[type])

    for latitude, longitude, title, type, special in zip(df['coordinates.y'],
                                                         df['coordinates.x'],
                                                         df['title'],
                                                         df['type'],
                                                         df['special']):
        label = folium.Popup(title, parse_html=True)
        #  print(f"{latitude}, {longitude}")
        icon = folium.Icon(color="blue")
        if special is True:
            icon = folium.Icon(color="red", icon="info-sign")
        marker_cluster = MarkerCluster().add_to(layer[type])
        folium.Marker([latitude, longitude],
                      icon=icon,
                      popup=label).add_to(marker_cluster)
    folium.LayerControl().add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    #  index()
    app.run(debug=True)
