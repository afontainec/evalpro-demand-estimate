import csv
from Global import INITIAL_YEAR, FINAL_YEAR

death_rates = { 'men': {},
                'women': {},
                }
fertility_rates = {}

penalolen_age_pyramid = { 'men': {},
                        'women': {},
                        }

TOTAL_POPULATION_OF_PENALOLEN = 0;

masculinity_rates = {}

AGE_PIRAMID_YEAR = 2015

# ------------------------------- SECTION read files:


def read_fertility_rate_by_age(min_age, max_age, total, year):
    global fertility_rates
    diff = (max_age + 1 - min_age)
    for age in range(min_age, max_age + 1):
        fertility_rates[year][age] = total

def init_fertility_rates():
    global fertility_rates
    with open('data/fertility_rate_by_age.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fertility_rates[row['year']] = {}
            read_fertility_rate_by_age(15, 19, float(row['15-19']),row['year'])
            read_fertility_rate_by_age(20, 24, float(row['20-24']),row['year'])
            read_fertility_rate_by_age(25, 29, float(row['25-29']),row['year'])
            read_fertility_rate_by_age(30, 34, float(row['30-34']),row['year'])
            read_fertility_rate_by_age(35, 39, float(row['35-39']),row['year'])
            read_fertility_rate_by_age(40, 44, float(row['40-44']),row['year'])
            read_fertility_rate_by_age(45, 49, float(row['45-49']),row['year'])


def init_death_rates():
    with open('data/death_rate.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for age in range(int(row['range_min']), int(row['range_max']) + 1):
                death_rates['men'][age] = row['men_rate']
                death_rates['women'][age] = row['women_rate']

def init_masculinity_by_zone():
    with open('data/masculinity_rate_by_zone.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            masculinity_rates[row['zone_id']] = row['masculinity_rate']



# -------------------------- SECTION read zones age and sex population


def ponderate_population(age, gender, age_range, total, portion_of_gender):
    amount_of_gender = portion_of_gender * total
    count = 0
    for i in age_range:
        count += age_pyramid[gender][i]
    count_of_age = age_pyramid[gender][age]
    portion_of_age = count_of_age / count
    return amount_of_gender * portion_of_age


def generate_age_pyramid_for_range(z,min_v, max_v, total_in_range, portion_of_men):
    portion_of_women = 1 - portion_of_men
    range_v = range(min_v, max_v)
    total = 0
    for age in range_v:
        z['men'][age] = ponderate_population(age, 'men', range_v, total_in_range, portion_of_men)
        z['women'][age] = ponderate_population(age, 'women', range_v, total_in_range, portion_of_women)
        total +=  z['men'][age] + z['women'][age]

def read_zones_age_range():
    zones = {}
    total = 0
    with open('data/age_range_by_zone.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            z = {'men': {},
                 'women': {}}
            z_id = row['zone_id']
            masculinity_rate_of_z = float(masculinity_rates[z_id])
            portion_of_men = masculinity_rate_of_z / (masculinity_rate_of_z + 100)
            portion_of_women = 1 - portion_of_men
            generate_age_pyramid_for_range(z,0, 15, float(row['0-14']), portion_of_men)
            generate_age_pyramid_for_range(z,15, 30, float(row['15-29']), portion_of_men)
            generate_age_pyramid_for_range(z,30, 60, float(row['30-59']), portion_of_men)
            generate_age_pyramid_for_range(z,60, 101, float(row['60-100']), portion_of_men)
            total += float(row['0-14']) + float(row['15-29']) + float(row['30-59']) + float(row['60-100'])
            zones[z_id] = z
    return {'zones':zones,
            'total': total
            }

def get_pyramid_by_zone(zones, density):
    total = 0
    for key in zones:
        for age in range(0,101):
            zones[key]['men'][age] = zones[key]['men'][age] * density
            zones[key]['women'][age] = zones[key]['women'][age] * density
            total += zones[key]['men'][age] + zones[key]['women'][age]



def init_zones_pyramid():
    data = read_zones_age_range()
    total_pixels = data['total']
    pixel_population_density = TOTAL_POPULATION_OF_PENALOLEN / total_pixels
    get_pyramid_by_zone(data['zones'], pixel_population_density)
    return data['zones']


# ------------------------------- SECTION rread and generate age pyramid:

def init_penalolen_age_pyramid(year):
    global penalolen_age_pyramid
    global TOTAL_POPULATION_OF_PENALOLEN

    with open('data/2015_pyramid.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            range_min = int(row['range_min'])
            range_max = int(row['range_max'])
            diff = range_max - range_min + 1; # the plus one is because we count the first elem
            for age in range(range_min, range_max + 1):
                penalolen_age_pyramid['men'][age] = int(row['men']) / diff
                penalolen_age_pyramid['women'][age] = int(row['women']) / diff
    TOTAL_POPULATION_OF_PENALOLEN = calculate_total_population(penalolen_age_pyramid)
    penalolen_age_pyramid = make_pyramid_older(penalolen_age_pyramid,AGE_PIRAMID_YEAR, year)


def calculate_total_population(pyramid):
    total = 0
    males = pyramid['men']
    females = pyramid['women']
    for key in males:
        total += males[key]
    for key in females:
        total += females[key]
    return total


def survived_year(gender, age, pyramid):
    mortality = death_rates[gender][age]
    survival_rate = (1000 - float(mortality)) / 1000
    return pyramid[gender][age] * survival_rate


def get_new_born(year, pyramid):
    new_borns = 0
    for age in range(15, 50):
        new_borns += fertility_rates[str(year)][age] * pyramid['women'][age]
    return new_borns


def make_pyramid_older(pyramid, init_year, end_year):
    for year in range(init_year, end_year):
        temp = {'men': {},
                'women': {}}
        for age in range(0,100):
            temp['men'][age + 1] = survived_year('men', age, pyramid)
            temp['women'][age + 1] = survived_year('women', age, pyramid)
        newborns = get_new_born(year, pyramid)
        temp['men'][0] = newborns / 2
        temp['women'][0] = newborns / 2
        pyramid = temp
    return pyramid


def init_age_pyramid_to(year):
    init_masculinity_by_zone()
    init_age_pyramid(year)



def print_age_pyramid():
    print_gender_age_pyramid('men')
    print_gender_age_pyramid('women')


def print_gender_age_pyramid(gender):
    star_equivalent = 25
    print gender
    for age in range(0,101):
        stars_to_print = age_pyramid[gender][age] / star_equivalent
        stars = str(age) + ': '
        for i in range(0, int(stars_to_print)):
            stars += '*'
        print stars + '(' + str(age_pyramid[gender][age]) + ')'

#--------------------------SETUP-------------------------------

init_masculinity_by_zone()
init_fertility_rates()
init_death_rates()
init_penalolen_age_pyramid(INITIAL_YEAR - 1)
