import area
import Population

zones = []

CURRENT_YEAR = 2015

def setup():
    zones = init_divisions()
    potential_client_prob = calculate_potential_client()
    iterate()



def iterate():
    print 'iterar'
    for zone in zones:
        zone.adjust_parameters()
        zone.calculate_customers()

def init_divisions():
    Population.init_death_rates()
    Population.init_birth_rates()
    Population.init_age_piramid_to(CURRENT_YEAR);
    zones_piramids = Population.init_zones_piramid()


# NOT IMPLEMENTED: should return a data strcture with the probability that someone will take t minutes to get to the pharmacy
def calculate_potential_client():
    return 0.5








setup()
