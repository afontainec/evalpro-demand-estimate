import csv

travel_time = {}

def init_travel_time():
    global travel_time
    with open('data/travel_time.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            check_attr_exists_in_dictionary(row['Unidad Vecinal'], travel_time)
            travel_time[row['Unidad Vecinal']]['Private'] = row['Private']
            travel_time[row['Unidad Vecinal']]['Municipalidad'] = row['Actual']
            travel_time[row['Unidad Vecinal']]['San_Luis'] = row['San Luis']
            travel_time[row['Unidad Vecinal']]['Lo_Hermida'] = row['Lo Hermida']

def get_time(zone_id, pharmacy):
    return float(travel_time[zone_id][pharmacy])


def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}
