import csv
from Global import AGE_RANGE


def get_pyramid(zone, year):
    pyramid = {
            'men': {},
            'women': {}
    }
    with open('population/zone_' + str(zone) + '/raw/pyramid_year_' + str(year) +  '.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            age = row['age']
            pyramid['men'][age] = row['men']
            pyramid['women'][age] = row['women']
        return pyramid
