import Zones
import PopulationGenerator
import Scenarios
import Printer
import csv
import os
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, AGE_RANGE


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
for zone in Zones.get():
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
            pyramids[zone_id][gender][age] = pyramids[zone_id][gender][age] + 1
        else:
            #FIXME SEE WHAT TO DO WITH ENTRIES WITH MISSING INFO

print "NO FUERON", not_

for zone in Zones.get():
    path = './patients/raw/pyramid_zone_' + str(zone) + '.csv'
    Printer.pyramid_to_file(pyramids[str(zone)], path)
    Printer.pyramid_to_image(pyramids[str(zone)], './patients/image/pyramid_zone_' + str(zone) + '.png')
