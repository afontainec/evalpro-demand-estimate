import area
import Population
import Time
from ProbabilityCalculator import calculate_probability_will_go, init_probabilites
import Scenarios

s = {}


global zones
CURRENT_YEAR = 2017
END_YEAR = 2037

SCENARIO  = 1;

def setup():
    global zones
    pharmacies = Scenarios.get_pharmacies(SCENARIO)
    init_probabilites()
    zones = init_divisions()
    print Population.TOTAL_POPULATION_OF_PENALOLEN, 'inicial'
    iterate()




def get_served_market_by_gender(gender, zone_id, piramid, month):
    gender_piramid = piramid[gender]
    served_piramid = {}
    for age in range(0,101):
        # served_piramid[age] = gender_piramid[age] * probability_will_go(gender, age, zone_id, month)
        served_piramid[age] = gender_piramid[age] * calculate_probability_will_go(month, gender, zone_id, age, SCENARIO)
    return served_piramid


def get_served_market(zone_id, piramid, month):
    served_market = {
        "men": {},
        "women": {}
        }
    served_market['men'] = get_served_market_by_gender('men', zone_id, piramid, month)
    served_market['women'] = get_served_market_by_gender('women', zone_id, piramid, month)
    return served_market

def init_year_served_market():
    served_market = {}
    for month in range(0,12):
        served_market[month] = {}
    return served_market

def iterate():
    print('Running scenario: ', SCENARIO)
    global zones
    served_market = {}
    for year in range(CURRENT_YEAR, END_YEAR):
        print('calculating year', year, '...')
        total_population_in_year = 0
        served_market[year] = init_year_served_market()
        for zone_id in zones:
            zones[zone_id] = Population.make_piramid_older(zones[zone_id], year - 1, year)
            total_population_in_year += Population.calculate_total_population(zones[zone_id])
            for month in range(0,12):
                passed_months = month + (year - CURRENT_YEAR) * 12 + 1
                served_market[year][month][zone_id] = get_served_market(zone_id, zones[zone_id], passed_months)
        print 'population in', year, total_population_in_year
    # print_served_market(zones, served_market)
    print_summarry(zones, served_market)


def init_divisions():
    Time.init_travel_time();
    Population.init_death_rates()
    Population.init_fertility_rates()
    Population.init_age_piramid_to(CURRENT_YEAR);
    return Population.init_zones_piramid()



def print_summarry(zones, served_market):
    f = open('./results/raw/' + str(SCENARIO) + '.csv', 'w')
    heading = "year"  + "," + "zone_id" + ","  + "age" + ","  + "gender" + "," + "total"
    f.write(heading)
    f.write('\n')
    for year in range(CURRENT_YEAR, END_YEAR):
        for zone_id in zones:
                for age in range(0, 101):
                    for gender in ['men', 'women']:
                        total_of_year = 0
                        for month in range(0,12):
                            total_of_year += served_market[year][month][zone_id][gender][age]
                        line = str(year) + "," + str(zone_id) + "," + str(age) + "," + gender + ',' + str(total_of_year)
                        f.write(line)
                        f.write('\n')
    f.close()




def print_served_market(zones, served_market):
    for year in range(CURRENT_YEAR, END_YEAR):
        print('************************************', year, '************************************')
        for zone_id in zones:
            print('----------------- Zona', zone_id, ':')
            for month in range(0,12):
                print("Mes", month)
                for age in range(0, 101):
                    print("Hombres de ", age, " anos: ",served_market[year][month][zone_id]['men'][age])
                    print("Mujeres de ", age, " anos: ",served_market[year][month][zone_id]['women'][age])

setup()
