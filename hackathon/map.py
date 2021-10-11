"""
    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser
    to see the map displayed

"""

import sys
from receiver import Receiver
from event import Event
from flask import Flask

import folium

app = Flask(__name__)


@app.route('/')
def index():
    receiver = Receiver()
    json_data = receiver.get_data_from_file(sys.argv[1])
    events = []
    for json_event in json_data['events']:
        events.append(Event(json_event))

    folium_map = folium.Map(location=[55.0, 103.0], zoom_start=4)

    for event in events:
        label = folium.Popup(event.title, parse_html=True)
        folium.Marker(
            [event.coordinates['latitude'],
             event.coordinates['longitude']],
            popup=label).add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
