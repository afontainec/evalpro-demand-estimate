import csv

death_rates = { 'men': {},
                'women': {},
                }
birth_rates = {}

age_piramid = { 'men': {},
                'women': {},
                }

TOTAL_POPULATION_OF_PENALOLEN = 10; #needed to get the amount of newborns

masculinity_rates = {}

INITIAL_YEAR = 2002

# ------------------------------- SECTION read files:

def init_birth_rates():
    with open('data/birth_rate.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            birth_rates[row['year']] = row['rate']

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
        count += age_piramid[gender][i]
    count_of_age = age_piramid[gender][age]
    portion_of_age = count_of_age / count
    return amount_of_gender * portion_of_age


def generate_age_piramid_for_range(z,min_v, max_v, total_in_range, portion_of_men):
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
            generate_age_piramid_for_range(z,0, 15, int(row['0-14']), portion_of_men)
            generate_age_piramid_for_range(z,15, 30, int(row['15-29']), portion_of_men)
            generate_age_piramid_for_range(z,30, 60, int(row['30-59']), portion_of_men)
            generate_age_piramid_for_range(z,60, 101, int(row['60-100']), portion_of_men)
            total += int(row['0-14']) + int(row['15-29']) + int(row['30-59']) + int(row['60-100'])
            zones[z_id] = z
    return {'zones':zones,
            'total': total
            }

def get_piramid_by_zone(zones, density):
    total = 0
    for key in zones:
        for age in range(0,101):
            zones[key]['men'][age] = zones[key]['men'][age] * density
            zones[key]['women'][age] = zones[key]['women'][age] * density
            total += zones[key]['men'][age] + zones[key]['women'][age]


def init_zones_piramid():
    data = read_zones_age_range()
    total_pixels = data['total']
    pixel_population_density = TOTAL_POPULATION_OF_PENALOLEN / total_pixels
    get_piramid_by_zone(data['zones'], pixel_population_density)
    return zones


# ------------------------------- SECTION rread and generate age piramid:

def init_age_piramid(year):
    with open('data/2002_piramid.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            range_min = int(row['range_min'])
            range_max = int(row['range_max'])
            diff = range_max - range_min + 1; # the plus one is because we count the first elem
            for age in range(range_min, range_max + 1):
                age_piramid['men'][age] = int(row['men']) / diff
                age_piramid['women'][age] = int(row['women']) / diff
    calculate_total_population()
    make_piramid_older(age_piramid,INITIAL_YEAR, year)


def calculate_total_population():
    global TOTAL_POPULATION_OF_PENALOLEN
    TOTAL_POPULATION_OF_PENALOLEN = 0
    males = age_piramid['men']
    females = age_piramid['women']
    for key in males:
        TOTAL_POPULATION_OF_PENALOLEN += males[key]
    for key in females:
        TOTAL_POPULATION_OF_PENALOLEN += females[key]


def survived_year(gender, age):
    mortality = death_rates[gender][age]
    survival_rate = (1000 - float(mortality)) / 1000

    return age_piramid[gender][age] * survival_rate


def make_piramid_older(piramid, init_year, end_year):
    global age_piramid
    global CURRENT_YEAR
    for year in range(init_year, end_year):
        temp = {'men': {},
                'women': {}}
        for age in range(0,100):
            temp['men'][age + 1] = survived_year('men', age)
            temp['women'][age + 1] = survived_year('women', age)
        newborns = TOTAL_POPULATION_OF_PENALOLEN * (float(birth_rates[str(year)]) / 1000)
        temp['men'][0] = newborns / 2
        temp['women'][0] = newborns / 2
        age_piramid = temp
        calculate_total_population()


def init_age_piramid_to(year):
    init_masculinity_by_zone()
    init_age_piramid(year)


def print_age_piramid():
    print_gender_age_piramid('men')
    print_gender_age_piramid('women')


def print_gender_age_piramid(gender):
    star_equivalent = 25
    print gender
    for age in range(0,101):
        stars_to_print = age_piramid[gender][age] / star_equivalent
        stars = str(age) + ': '
        for i in range(0, int(stars_to_print)):
            stars += '*'
        print stars + '(' + str(age_piramid[gender][age]) + ')'
