import json
import sys


class Receiver():
    def _init__(self, data_source):
        self.data_source

    def get_data_from_file(self, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
            return data
        except IOError:
            print(f"File {filename} not found!\n")
            return {}


def _main():
    receiver = Receiver()
    json_data = receiver.get_data_from_file(sys.argv[1])
    print(json_data)


if __name__ == "__main__":
    _main()
