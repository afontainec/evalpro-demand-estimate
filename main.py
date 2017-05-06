import area
import Population
import Time
import ProbabilityCalculator

global zones
CURRENT_YEAR = 2017
END_YEAR = 2037

def setup():
    global zones
    zones = init_divisions()
    ProbabilityCalculator.init_probabilites()
    print ProbabilityCalculator.calculate_probability_will_go(2017, 'men', 18, 130)
    iterate()


def get_served_market_by_gender(gender, travel_time, piramid, year):
    gender_piramid = piramid[gender]
    served_piramid = {}
    for age in range(0,101):
        served_piramid[age] = gender_piramid[age] * probability_will_go(gender, age, travel_time, year)
        # served_piramid[age] = gender_piramid[age] * ProbabilityCalculator.calculate_probability_will_go(year, gender, age, travel_time)
    return served_piramid


def get_served_market(travel_time, piramid, year):
    served_market = {
        "men": {},
        "women": {}
        }
    served_market['men'] = get_served_market_by_gender('men', travel_time, piramid, year)
    served_market['women'] = get_served_market_by_gender('women', travel_time, piramid, year)
    return served_market

def init_year_served_market():
    served_market = {}
    for month in range(0,12):
        served_market[month] = {}
    return served_market

def iterate():
    global zones
    served_market = {}
    for year in range(CURRENT_YEAR, END_YEAR):
        served_market[year] = init_year_served_market()
        for zone_id in zones:
            zones[zone_id] = Population.make_piramid_older(zones[zone_id], year - 1, year)
            for month in range(0,12):
                served_market[year][month][zone_id] = get_served_market(Time.travel_time[zone_id], zones[zone_id], year)
    # print_served_market(zones, served_market)
    print_summarry(zones, served_market)


def init_divisions():
    Time.init_travel_time();
    Population.init_death_rates()
    Population.init_fertility_rates()
    Population.init_age_piramid_to(CURRENT_YEAR);
    return Population.init_zones_piramid()



# FIXME: should return a data strcture with the probability that someone will take t minutes to get to the pharmacy
def probability_will_go(gender, age, zone_id, year):
    return 0.5


def print_summarry(zones, served_market):
    print "year" , ",", "month" , ",", "zone_id" , ",", "total"
    for year in range(CURRENT_YEAR, END_YEAR):
        for month in range(0,12):
            for zone_id in zones:
                total_of_zone = 0
                for age in range(0, 101):
                    total_of_zone += served_market[year][month][zone_id]['men'][age] + served_market[year][month][zone_id]['women'][age]
                print year , ",", month , ",", zone_id , ",", total_of_zone



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
