import Zones
import PopulationGenerator
import Scenarios
import Printer
import csv
import os
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, AGE_RANGE


def get_current_pyramid(zone):
    pyramid = {
               'men': {},
               'women'; {}
               }
    with open('patients/raw/pyramid_zone_' + str(zone) + '.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pyramid['men'][int(row['age'])] = int(row['men'])
            pyramid['women'][int(row['age'])] = int(row['women'])


def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}

def translate_gender(gender):
    if gender == 'MASCULINO':
        return 'men'
    if gender == 'FEMENINO':
        return 'women'
    return

pyramids = {}
served = {}
for zone in Zones.get():
    served[str(zone)] = 0
    pyramids[str(zone)] = {
        'men': {},
        'women': {}
    }
    for age in AGE_RANGE:
        pyramids[str(zone)]['men'][age] = 0
        pyramids[str(zone)]['women'][age] = 0

not_ = 0

with open('data/patients.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        zone_id = row['unidad']
        gender = translate_gender(row['ATRIBUTO'])
        age = int(row['edad_lr'])

        if  gender != None and age in AGE_RANGE and int(zone_id) in Zones.get():
            served[zone_id] = served[zone_id] + 1
            pyramids[zone_id][gender][age] = pyramids[zone_id][gender][age] + 1
        else:
            #FIXME SEE WHAT TO DO WITH ENTRIES WITH MISSING INFO
            x = 'yes'

porcentage = {}

for zone in Zones.get():
    print zone
    # Print the pyramid of the zone
    path = './patients/raw/pyramid_zone_' + str(zone) + '.csv'
    Printer.pyramid_to_file(pyramids[str(zone)], path)
    Printer.pyramid_to_image(pyramids[str(zone)], './patients/image/pyramid_zone_' + str(zone) + '.png')
    # calculate the serve market of the population
    with open('population/zone_' + str(zone) + '/raw/total.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['year'] == str(INITIAL_YEAR):
                if float(row['total']) > 0:
                    porcentage[str(zone)] =  served[str(zone)] / float(row['total']) * 100
                else:
                    porcentage[str(zone)] = 0
path = './patients/raw/total.csv'
Printer.served_market(Zones.get(), served, porcentage, path)
