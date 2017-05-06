import csv

travel_time = {}





def init_travel_time():
    with open('data/travel_time.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            travel_time[row['Unidad Vecinal']] = row['Tiempo medio']
