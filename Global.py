INITIAL_YEAR = 2017
FINAL_YEAR = 2037
MAX_AGE = 100

AGE_RANGE = range(0, MAX_AGE)
YEARS = range(INITIAL_YEAR, FINAL_YEAR)

INTERVALS_LABELS = ['0-9', '10-19', '20-44', '45-64', '65-79', '80-100']

INTERVALS = [range(0,10), range(10,20), range(20,45), range(45,65), range(65,80), range(80,MAX_AGE)]

GENDER = ['men', 'women']

ESCENARIO = 1

NO_SENSIBILITY = 'NO_SENSIBILITY'
LIFE_SENSIBILITY = 'LIFE_SENSIBILITY'
TIME_SENSIBILITY = 'TIME_SENSIBILITY'
SAVING_SENSIBILITY = 'SAVING_SENSIBILITY'

ANNUAL_THROUGHPUT = {'base_case': 102988,
                     'lo_hermida': 102988 * 2,
                     'san_luis': 102988 * 2
                     } 

SENSIBILITY = NO_SENSIBILITY


def get_interval(age):
    for idx, interval in enumerate(INTERVALS):
        if age in interval:
            return idx
