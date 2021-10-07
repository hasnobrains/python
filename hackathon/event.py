import sys
from geopy.geocoders import Nominatim
from receiver import Receiver


class Event():
    def __init__(self, event_json):
        self.json = event_json
        self.geolocator = Nominatim(user_agent='russia_explorer')
        self.create_event()

    def __str__(self):
        name = f'id = {self.id}\n'
        name += f'type = {self.type}\n'
        name += f'source = {self.source}\n'
        name += f'date = {self.date}\n'
        name += f'title = {self.title}\n'
        name += f'text = {self.text}\n'
        name += f'special = {self.special}\n'
        name += f'address = {self.address}\n'
        name += f'coordinates = {self.coordinates}\n'
        name += f'importance = = {self.importance}\n'
        name += f'links = {self.links}\n'
        return name

    def create_event(self):
        self.id = self.json['id']
        self.type = self.json['type']
        self.source = self.json['source']
        self.date = self.json['date']
        self.title = self.json['title']
        self.text = self.json['text']
        self.special = self.json['special']
        self.address = self.set_address()
        self.coordinates = self.set_coordinates()
        self.importance = self.json['importance']
        self.links = self.json['links']

    def set_address(self):
        self.address = {}
        if 'region' in self.json['address'] and \
           'city' in self.json['address']:
            self.address = {'region': self.json['address']['region'],
                            'city': self.json['address']['city']}

    def set_coordinates(self):
        if 'coordinates' in self.json and \
           'x' in self.json['coordinates'] and \
           'y' in self.json['coordinates']:
            return {'latitude': self.json['coordinates']['x'],
                    'longitude': self.json['coordinates']['y']}
        if 'region' in self.json['address'] and \
           'city' in self.json['address']:
            location = self.geolocator.geocode(
                self.json['address']['city']
                + ', '
                + self.json['address']['region'])
            return {'latitude': location.latitude,
                    'longitude': location.longitude}


def _main():
    receiver = Receiver()
    json_data = receiver.get_data_from_file(sys.argv[1])
    events = []
    for json_event in json_data['events']:
        events.append(Event(json_event))

    for event in events:
        print(event)


if __name__ == "__main__":
    _main()
