from geopy.geocoders import GeocodeFarm
import yaml
from location_data import datafiles


def choose(elements, prompt='> '):
    try:
        while True:
            for i, element in enumerate(elements):
                print(f'{i}) {element}')
            choice = input(prompt)
            try:
                index = int(choice)
                return elements[index]
            except (ValueError, IndexError):
                pass
    except (KeyboardInterrupt, EOFError):
        exit(0)


if __name__ == '__main__':
    entry = {}

    entry['name'] = input('Name> ')

    entry['type'] = choose(['school', 'company', 'research institute', 'other'], 'Type> ')

    address = input('Address> ')

    geolocator = GeocodeFarm()
    location = geolocator.geocode(address, timeout=15)
    if location is None:
        print('Geocoder failed')
        exit()

    entry['lat'] = location.latitude
    entry['long'] = location.longitude

    if location.longitude < 0:
        datafile = 'america'
    else:
        datafile = choose(datafiles, 'Chose a datafile> ')

    include_address = choose(['yes', 'no'], 'Include address in entry?> ')
    if include_address == 'yes':
        entry['address'] = location.raw['formatted_address']

    link = input('URL Link (optional)> ')
    if link:
        entry['link'] = link

    full_filename = f'data/{datafile}.yaml'
    data = yaml.load(open(full_filename))
    data.append(entry)
    data = sorted(data, key=lambda d: d['name'])
    yaml.dump(data, open(full_filename, 'w'), allow_unicode=True, default_flow_style=False)
