import Zones
import Population
import Scenarios
import Printer
import os
import csv
import Global
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, GENDER, AGE_RANGE, INTERVALS_LABELS, INTERVALS, ANNUAL_THROUGHPUT

ESCENARIO = 'san_luis'
MONTHS = range(0,12)
print ESCENARIO

def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}
proportions = {}

for gender in GENDER:
    proportions[gender] = {}
    for label in INTERVALS_LABELS:
            proportions[gender][label] = {}
            path = 'data/proportion/' + gender + '_' + label +'.csv'
            with open(path, 'rU') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    zone = row['Unidad']
                    check_attr_exists_in_dictionary(zone, proportions[gender][label])
                    proportions[gender][label][zone]['base_case'] = float(row['proporcion'])
                    proportions[gender][label][zone]['san_luis'] = float(row['proporcion San Luis'])
                    proportions[gender][label][zone]['lo_hermida'] = float(row['Prop Lo Hermida'])


factor = {}

path = 'data/proportion/ponderadores_media.csv'
with open(path, 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        month = row['meses']
        factor[month] = float(row['ponderador'])

hour_extended_factor = {}
path = 'data/proportion/extension.csv'
with open(path, 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        label = row['rango']
        hour_extended_factor[label] = float(row['ponderador'])




def probability_will_go(month, year, zone, gender, age, escenario):
    m = (year - INITIAL_YEAR) * 12 + month
    idx = Global.get_interval(age)
    label = INTERVALS_LABELS[idx]
    return proportions[gender][label][str(zone)][escenario] * factor[str(m)] * hour_extended_factor[label]

def init_demand_by_segment():
    demand_by_segment = {}
    for year in YEARS:
        demand_by_segment[year] = {}
        for gender in GENDER:
            demand_by_segment[year][gender] = {}
            for label in INTERVALS_LABELS:
                demand_by_segment[year][gender][label] = 0
    return demand_by_segment




demand_by_zone = {}
demand_by_segment = init_demand_by_segment()
total2 = 0

def add_to_demand_by_segment(year, gender, age, amount):
    global demand_by_segment
    global total2
    for idx, interval in enumerate(INTERVALS):
        if age in interval:
            label = INTERVALS_LABELS[idx]
            demand_by_segment[year][gender][label] += amount
            total2 += amount
            return

# TOTAL DEMAND
for year in YEARS:
    print 'calculating', year, '.....'
    demand_by_zone[year] = {}
    total = 0
    for zone in Zones.get():
        demand_by_zone[year][zone] = 0
        for month in MONTHS:
            pyramid = Population.get_pyramid(zone, year)
            for gender in GENDER:
                for age in AGE_RANGE:
                    prob = probability_will_go(month, year, zone, gender, age, ESCENARIO)
                    will_go = float(pyramid[gender][age]) * prob
                    demand_by_zone[year][zone] += will_go
                    total += will_go
                    add_to_demand_by_segment(year, gender, age, will_go)

# CUT DEMAND BY THROUGHPUT
for year in YEARS:
    total_of_year = 0
    for gender in GENDER:
        for label in INTERVALS_LABELS:
            total_of_year += demand_by_segment[year][gender][label]
    if total_of_year > ANNUAL_THROUGHPUT[ESCENARIO]:
        for gender in GENDER:
            for label in INTERVALS_LABELS:
                demand_by_segment[year][gender][label] = (demand_by_segment[year][gender][label] / total_of_year) * ANNUAL_THROUGHPUT[ESCENARIO]
        for zone in Zones.get():
            demand_by_zone[year][zone] = demand_by_zone[year][zone] / total_of_year * ANNUAL_THROUGHPUT[ESCENARIO]

for year in YEARS:
    for zone in Zones.get():
        Printer.demand_by_zone(demand_by_zone, 'demand/' + ESCENARIO + '/by_zone' + '.csv')
        Printer.demand_by_segment(demand_by_segment, 'demand/'  + ESCENARIO +  '/by_segment' + '.csv')
