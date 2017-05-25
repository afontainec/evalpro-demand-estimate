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
            age = int(row['age'])
            pyramid['men'][age] = row['men']
            pyramid['women'][age] = row['women']
        return pyramid


def get_patient_pyramid(zone):
    pyramid = {
               'men': {},
               'women': {}
               }
    with open('patients/raw/pyramid_zone_' + str(zone) + '.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            age = int(row['age'])
            pyramid['men'][age] = row['men']
            pyramid['women'][age] = row['women']
        return pyramid


def shorten_pyramid(pyramid):
    shorten_pyramid = {
            'men': {
                '0-14': 0,
                '15-29': 0,
                '30-64': 0,
                '65-100': 0,
            },
            'women': {
                '0-14': 0,
                '15-29': 0,
                '30-64': 0,
                '65-100': 0,
            }
    }
    for age in range(0,15):
        shorten_pyramid['men']['0-14'] += float(pyramid['men'][age])
        shorten_pyramid['women']['0-14'] += float(pyramid['women'][age])
    for age in range(15,30):
        shorten_pyramid['men']['15-29'] += float(pyramid['men'][age])
        shorten_pyramid['women']['15-29'] += float(pyramid['women'][age])
    for age in range(30,65):
        shorten_pyramid['men']['30-64'] += float(pyramid['men'][age])
        shorten_pyramid['women']['30-64'] += float(pyramid['women'][age])
    for age in range(65,100):
        shorten_pyramid['men']['65-100'] += float(pyramid['men'][age])
        shorten_pyramid['women']['65-100'] += float(pyramid['women'][age])
    return shorten_pyramid
