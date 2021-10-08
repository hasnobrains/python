import json
import sys
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster

#  from datetime import date, timedelta
from pywebio.output import put_button, put_html, use_scope, \
        put_tabs, put_scrollable, put_table, put_row
#  from pywebio.input import input
from pywebio.pin import pin_wait_change, put_select
from pywebio import start_server
from functools import partial

dates_list = []
rep_dt = '1900-01-01'


def fill_dataframe():
    geolocator = Nominatim(user_agent='russia_explorer')
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            data = json.load(f)
    except IOError:
        print(f"File {filename} not found!\n")
        return

    df = pd.json_normalize(data['events'])

    # shrink whitespaces
    df.replace(np.nan, '', inplace=True)
    for index, row in df.iterrows():
        if row['address.region'] == '' and \
           row['address.place'] == '' and \
           row['coordinates.x'] == '' and \
           row['coordinates.y'] == '':
            continue

        row['address.region'] = ' '.join((row['address.region']
                                          .split()))
        row['address.place'] = ' '.join((row['address.place']
                                         .split()))
        address = ''
        if row['address.place'] != '':
            address += f"{row['address.place']}"
        if row['address.region'] != '':
            address += f", {row['address.region']}"
        print(address)
        if address == '':
            continue
        location = geolocator.geocode(address)
        if location is not None:
            df.loc[df['id'] == row['id'],
                   'coordinates.x'] = location.longitude
            df.loc[df['id'] == row['id'],
                   'coordinates.y'] = location.latitude
    return df

    #  try:
    #      geo_filename = \
    #          '/Volumes/Second/Downloads/russia_geojson/admin_level_4.geojson'
    #      with open(geo_filename) as f:
    #          data = json.load(f)
    #  except IOError:
    #      print(f"File {filename} not found!\n")
    #      return
    #


def unused_list():
    ddf = df.loc[df['date'] == rep_dt]
    ddf['coordinates.y'].replace('', np.nan, inplace=True)
    ddf['coordinates.x'].replace('', np.nan, inplace=True)
    titles = ddf.loc[ddf['date'] == rep_dt, 'title'].tolist()
    texts = ddf.loc[ddf['date'] == rep_dt, 'text'].tolist()
    out = [['Title', 'Text']]
    for title, text in zip(titles, texts):
        out.append([title, ' '.join(text.split())])
    return out


def used_list():
    ddf = df.loc[df['date'] == rep_dt]
    ddf['coordinates.y'].replace('', np.nan, inplace=True)
    ddf['coordinates.x'].replace('', np.nan, inplace=True)
    ddf.dropna(subset=['coordinates.x'], axis=0, inplace=True)
    titles = ddf.loc[ddf['date'] == rep_dt, 'title'].tolist()
    texts = ddf.loc[ddf['date'] == rep_dt, 'text'].tolist()
    ids = ddf.loc[ddf['date'] == rep_dt, 'id'].tolist()
    out = [['Title', 'Text', '']]
    for title, text, id in zip(titles, texts, ids):
        out.append([title, ' '.join(text.split()),
                    put_button("Show", onclick=partial(ButtonClickFind,
                                                       id=id))])
    return out


def ButtonClickUpdate():
    #   Сюда надо скармливать html карты на опред. дату
    #  file = 'Яндекс.html'
    #  with open(file, 'r', encoding='UTF-8') as f:
    #      html = f.read()
    #  with use_scope('map', clear=True):
    #      put_html(html)
    global folium_map
    ddf = df.loc[df['date'] == rep_dt]
    ddf['coordinates.y'].replace('', np.nan, inplace=True)
    ddf['coordinates.x'].replace('', np.nan, inplace=True)
    ddf.dropna(subset=['coordinates.x'], axis=0, inplace=True)

    center_y = ddf['coordinates.y'].sum()/ddf['coordinates.y'].count()
    center_x = ddf['coordinates.x'].sum()/ddf['coordinates.x'].count()
    folium_map = folium.Map(location=[center_y, center_x], zoom_start=4)
    #  folium.GeoJson(
    #      '/Volumes/Second/Downloads/russia_geojson/admin_level_4.geojson',
    #      name="geojson").add_to(folium_map)
    # adding layers
    layer = {}
    for type in ddf['type'].drop_duplicates():
        layer[type] = folium.FeatureGroup(name=type)
        folium_map.add_child(layer[type])

    for latitude, longitude, title, type, special in zip(ddf['coordinates.y'],
                                                         ddf['coordinates.x'],
                                                         ddf['title'],
                                                         ddf['type'],
                                                         ddf['special']):
        if latitude == '' and longitude == '':
            continue
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
    Main_Table()


def ButtonClickFind(id):
    #  Тут должно быть взаимодействие с картой
    #  по подсветке нужной точки
    global folium_map
    #  put_text("You click button with id: %s" % (id))
    row = df.loc[df['id'] == id]

    if row['coordinates.y'].item() == '' and \
       row['coordinates.x'].item() == '':
        return

    address = ''
    if row['address.place'].item() != '':
        address += f"{row['address.place'].item()}"
    if row['address.region'].item() != '':
        address += f", {row['address.region'].item()}"
    folium_map = folium.Map(location=[row['coordinates.y'],
                                      row['coordinates.x']], zoom_start=11)
    label = folium.Popup(address, parse_html=True)
    icon = folium.Icon(color="blue")
    if row['special'].item() is True:
        icon = folium.Icon(color="red", icon="info-sign")
    folium.Marker([row['coordinates.y'], row['coordinates.x']],
                  icon=icon,
                  popup=label).add_to(folium_map)
    #  with use_scope('map', clear=True):
    #      put_html(folium_map._repr_html_())
    #
    Main_Table()


@use_scope('mainTbl', clear=True)
def Main_Table():
    put_tabs([
            {'title': 'Geo Events', 'content':
             [put_row([put_select("date",
                                  options=dates_list,
                                  value=rep_dt),
                       None,
                       put_button("Show",
                                  onclick=ButtonClickUpdate,
                                  color='success',
                                  outline=True)]),
              put_scrollable(
                     put_table(used_list()),
                     height=250,
                     keep_bottom=True),
              put_html(folium_map._repr_html_())]},
            {'title': 'No Geo Events',
             'content': put_table(unused_list())}])


def get_dates(dates):
    global dates_list
    #  Сюда надо скармливать список доступных исторических дат
    dates_list = sorted(dates.values.tolist(), reverse=True)
    return dates_list


def app():

    global df
    df = fill_dataframe()
    global rep_dt
    get_dates(df['date'].drop_duplicates())
    #    Здесь надо вставить максимальную дату из входных данных
    rep_dt = dates_list[0]
    ButtonClickUpdate()
    Main_Table()

    #   Сюда надо скармливать html карты
    #  with open(r"./127.0.0.1.html", 'r', encoding='UTF-8') as f:
    #      html = f.read()
    #
    #  with use_scope('map', clear=True):
    #      put_html(folium_map._repr_html_())
    #
    while True:
        new_date = pin_wait_change(['date'])
        if new_date['name'] == 'date':
            #   Сюда мы сохраняем выбранную дату
            rep_dt = new_date['value']


if __name__ == '__main__':
    start_server(app, debug=True, port='44315')
