import Zones
import Population
import Scenarios
import Printer
import os
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, GENDER, AGE_RANGE, INTERVALS_LABELS, INTERVALS


MONTHS = range(0,12)

def probability_will_go(month, travel_time, income, gender, age):
    return 0.1

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
            # print 'amount: ', amount
            return


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
                    # print '---------------------------------'
                    # print year, month, zone, gender, age
                    prob = probability_will_go(month, 0, 0, gender, age)
                    will_go = float(pyramid[gender][age]) * prob
                    demand_by_zone[year][zone] += will_go
                    # print 'will go:', will_go
                    total += will_go
                    add_to_demand_by_segment(year, gender, age, will_go)
                    # if total != total2:
                    #     print '********************************************************************************************************'
                    #     print total, total2, will_go



for year in YEARS:
    for zone in Zones.get():
        Printer.demand_by_zone(demand_by_zone, 'demand/by_zone' + '.csv')
        Printer.demand_by_segment(demand_by_segment, 'demand/by_segment' + '.csv')
