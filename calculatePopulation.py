import Zones
import Population
import Scenarios
import Printer
import os
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS




def check_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory +'/raw'):
        os.makedirs(directory +'/raw')
    if not os.path.exists(directory +'/image'):
        os.makedirs(directory +'/image')

total_populations = {}
for zone in Zones.get():
    print 'getting age pyramids of', zone
    total_populations[zone] = []
    pyramid = Population.zones_pyramids[str(zone)]
    for year in YEARS:
        directory = './Population/zone_'+ str(zone)
        check_directory_exists(directory)
        pyramid = Population.make_pyramid_older(pyramid, year - 1, year)
        path = './Population/zone_'+ str(zone) + '/raw/pyramid_year_' + str(year) + '.csv'
        Printer.pyramid_to_file(pyramid, path)
        Printer.pyramid_to_image(pyramid, './Population/zone_'+ str(zone) + '/image/pyramid_year_' + str(year) + '.png')
        total_populations[zone].append(Population.calculate_total_population(pyramid))
    Printer.print_total_population(total_populations[zone], './Population/zone_' + str(zone) + '/raw/total.csv')
    Printer.line_graph(YEARS, total_populations[zone], './Population/zone_' + str(zone) + '/image/total.png')

penalolen_population = []
for i in range(0,len(total_populations[1])):
    total = 0
    for zone in Zones.get():
        total += total_populations[zone][i]
    penalolen_population.append(total)
print str(zone)
Printer.print_total_population(penalolen_population, './Population/penalolen/raw/total_from_zones.csv')
Printer.line_graph(YEARS, penalolen_population, './Population/penalolen/image/total_from_zones.png')


#     print './Population/', zone
#     for year in YEARS:
#         print 'getting age pyramid of', year
#         pyramid = Population.make_pyramid_older(pyramid, year - 1, year)
#         path = './Population/penalolen/raw/pyramid_year_' + str(year) + '.csv'
#         Printer.pyramid_to_file(pyramid, path)
#         Printer.pyramid_to_image(pyramid, './Population/penalolen/image/pyramid_year_' + str(year) + '.png')
#         total_populations.append(Population.calculate_total_population(pyramid))
#         print 'age pyramid for year ', year, 'saved'
# print 'Calculating age pyramid for penalolen...'
# pyramid = Population.penalolen_age_pyramid
# for year in YEARS:
#     print 'getting age pyramid of', year
#     pyramid = Population.make_pyramid_older(pyramid, year - 1, year)
#     path = './Population/penalolen/raw/pyramid_year_' + str(year) + '.csv'
#     Printer.pyramid_to_file(pyramid, path)
#     Printer.pyramid_to_image(pyramid, './Population/penalolen/image/pyramid_year_' + str(year) + '.png')
#     total_populations.append(Population.calculate_total_population(pyramid))
#     print 'age pyramid for year ', year, 'saved'
#
# Printer.print_total_population(total_populations, './Population/penalolen/raw/total.csv')
# Printer.line_graph(YEARS, total_populations, './Population/penalolen/image/total.png')


# global zones
# CURRENT_YEAR = 2017
# END_YEAR = 2037
#
# SCENARIO  = 3;
#
# def setup():
#     global zones
#     pharmacies = Scenarios.get_pharmacies(SCENARIO)
#     init_probabilites()
#     print Population.TOTAL_POPULATION_OF_PENALOLEN, 'inicial'
#     iterate()
#
#
#
#
# def get_served_market_by_gender(gender, zone_id, pyramid, month):
#     gender_pyramid = pyramid[gender]
#     served_pyramid = {}
#     for age in range(0,101):
#         # served_pyramid[age] = gender_pyramid[age] * probability_will_go(gender, age, zone_id, month)
#         served_pyramid[age] = gender_pyramid[age] * calculate_probability_will_go(month, gender, zone_id, age, SCENARIO)
#     return served_pyramid
#
#
# def get_served_market(zone_id, pyramid, month):
#     served_market = {
#         "men": {},
#         "women": {}
#         }
#     served_market['men'] = get_served_market_by_gender('men', zone_id, pyramid, month)
#     served_market['women'] = get_served_market_by_gender('women', zone_id, pyramid, month)
#     return served_market
#
# def init_year_served_market():
#     served_market = {}
#     for month in range(0,12):
#         served_market[month] = {}
#     return served_market
#
# def iterate():
#     print('Running scenario: ', SCENARIO)
#     global zones
#     served_market = {}
#     for year in range(CURRENT_YEAR, END_YEAR):
#         print('calculating year', year, '...')
#         total_population_in_year = 0
#         served_market[year] = init_year_served_market()
#         for zone_id in zones:
#             zones[zone_id] = Population.make_pyramid_older(zones[zone_id], year - 1, year)
#             total_population_in_year += Population.calculate_total_population(zones[zone_id])
#             for month in range(0,12):
#                 passed_months = month + (year - CURRENT_YEAR) * 12 + 1
#                 served_market[year][month][zone_id] = get_served_market(zone_id, zones[zone_id], passed_months)
#         print 'population in', year, total_population_in_year
#     # print_served_market(zones, served_market)
#     print_summarry(zones, served_market)
#
#
# def init_divisions():
#     Time.init_travel_time();
#     Population.init_death_rates()
#     Population.init_fertility_rates()
#     Population.init_age_pyramid_to(CURRENT_YEAR);
#     return Population.init_zones_pyramid()
#
#
#
# def print_summarry(zones, served_market):
#     f = open('./results/raw/' + str(SCENARIO) + '.csv', 'w')
#     heading = "year"  + "," + "zone_id" + ","  + "age" + ","  + "gender" + "," + "total"
#     f.write(heading)
#     f.write('\n')
#     for year in range(CURRENT_YEAR, END_YEAR):
#         for zone_id in zones:
#                 for age in range(0, 101):
#                     for gender in ['men', 'women']:
#                         total_of_year = 0
#                         for month in range(0,12):
#                             total_of_year += served_market[year][month][zone_id][gender][age]
#                         line = str(year) + "," + str(zone_id) + "," + str(age) + "," + gender + ',' + str(total_of_year)
#                         f.write(line)
#                         f.write('\n')
#     f.close()
#
#
#
#
# def print_served_market(zones, served_market):
#     for year in range(CURRENT_YEAR, END_YEAR):
#         print('************************************', year, '************************************')
#         for zone_id in zones:
#             print('----------------- Zona', zone_id, ':')
#             for month in range(0,12):
#                 print("Mes", month)
#                 for age in range(0, 101):
#                     print("Hombres de ", age, " anos: ",served_market[year][month][zone_id]['men'][age])
#                     print("Mujeres de ", age, " anos: ",served_market[year][month][zone_id]['women'][age])
#
# setup()
