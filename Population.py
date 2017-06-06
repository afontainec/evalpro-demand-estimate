import csv
from Global import AGE_RANGE, INTERVALS, INTERVALS_LABELS, GENDER


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
    shorten_pyramid = {}
    for gender in GENDER:
        shorten_pyramid[gender] = {}
        for label in INTERVALS_LABELS:
            shorten_pyramid[gender][label] = 0

    for index, interval in enumerate(INTERVALS):
        label = INTERVALS_LABELS[index]
        for age in interval:
            for gender in GENDER:
                shorten_pyramid[gender][label] += float(pyramid['men'][age])
    return shorten_pyramid
