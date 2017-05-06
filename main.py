import area
import Population
import Time
import ProbabilityCalculator
import Escenarios


global zones
CURRENT_YEAR = 2017
END_YEAR = 2037

ESCENARIO  = 2;

def setup():
    global zones
    zones = init_divisions()
    pharmacies = Escenarios.get_pharmacies(ESCENARIO)
    ProbabilityCalculator.init_probabilites(pharmacies)
    for pharmacy in pharmacies:
        iterate(pharmacy)


def get_served_market_by_gender(gender, zone_id, pharmacy, piramid, month):
    gender_piramid = piramid[gender]
    served_piramid = {}
    for age in range(0,101):
        served_piramid[age] = gender_piramid[age] * probability_will_go(gender, age, zone_id, month)
        gender_piramid[age] * ProbabilityCalculator.calculate_probability_will_go(month, gender, age, zone_id, pharmacy)
    return served_piramid


def get_served_market(zone_id, pharmacy, piramid, month):
    served_market = {
        "men": {},
        "women": {}
        }
    served_market['men'] = get_served_market_by_gender('men', zone_id, pharmacy, piramid, month)
    served_market['women'] = get_served_market_by_gender('women', zone_id, pharmacy, piramid, month)
    return served_market

def init_year_served_market():
    served_market = {}
    for month in range(0,12):
        served_market[month] = {}
    return served_market

def iterate(pharmacy):
    print 'Getting demand of pharmacy: ', pharmacy
    global zones
    served_market = {}
    for year in range(CURRENT_YEAR, END_YEAR):
        print 'calculating year', year, '...'
        served_market[year] = init_year_served_market()
        for zone_id in zones:
            zones[zone_id] = Population.make_piramid_older(zones[zone_id], year - 1, year)
            for month in range(0,12):
                passed_months = month + (year - CURRENT_YEAR) * 12
                served_market[year][month][zone_id] = get_served_market(zone_id, pharmacy, zones[zone_id], passed_months)
    # print_served_market(zones, served_market)
    print_summarry(zones, served_market, pharmacy)


def init_divisions():
    Time.init_travel_time();
    Population.init_death_rates()
    Population.init_fertility_rates()
    Population.init_age_piramid_to(CURRENT_YEAR);
    return Population.init_zones_piramid()



# FIXME: should return a data strcture with the probability that someone will take t minutes to get to the pharmacy
def probability_will_go(gender, age, zone_id, year):
    return 0.5


def print_summarry(zones, served_market, pharmacy):
    f = open('./results/raw/' + pharmacy + '.csv', 'w')
    heading = "year"  + "," + "zone_id"  + "," + "total"
    f.write(heading)
    f.write('\n')
    for year in range(CURRENT_YEAR, END_YEAR):
        for zone_id in zones:
            total_of_zone = 0
            for month in range(0,12):
                for age in range(0, 101):
                    total_of_zone += served_market[year][month][zone_id]['men'][age] + served_market[year][month][zone_id]['women'][age]
            line =  str(year)  + "," + str(zone_id)  + "," + str(total_of_zone)
            f.write(line)
            f.write('\n')
    f.close()




def print_served_market(zones, served_market):
    for year in range(CURRENT_YEAR, END_YEAR):
        print '************************************', year, '************************************'
        for zone_id in zones:
            print '----------------- Zona', zone_id, ':'
            for month in range(0,12):
                print "Mes", month
                for age in range(0, 101):
                    print "Hombres de ", age, " anos: ",served_market[year][month][zone_id]['men'][age]
                    print "Mujeres de ", age, " anos: ",served_market[year][month][zone_id]['women'][age]

setup()
