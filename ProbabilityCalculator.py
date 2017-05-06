import csv

probability_will_go = {}

max_interval = [15, 25, 40,60, 1000]





def init_probabilites():
    global probability_will_go
    with open('data/probability_will_go.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            check_attr_exists_in_dictionary(row['year'], probability_will_go)
            check_attr_exists_in_dictionary(row['gender'], probability_will_go[row['year']])
            for age in range(int(row['min_age']), int(row['max_age'])): # FIXME Check if its max_age + 1 or just max_age
                check_attr_exists_in_dictionary(age, probability_will_go[row['year']][row['gender']])
                probability_will_go[row['year']][row['gender']][age][max_interval[0]] = row['between_0_and_15']
                probability_will_go[row['year']][row['gender']][age][max_interval[1]] = row['between_15_and_25']
                probability_will_go[row['year']][row['gender']][age][max_interval[2]] = row['between_25_and_40']
                probability_will_go[row['year']][row['gender']][age][max_interval[3]] = row['between_40_and_60']
                probability_will_go[row['year']][row['gender']][age][max_interval[4]] = row['between_60_and_1000']



def check_attr_exists_in_dictionary(attr, dictionary):

    if not attr in dictionary:
        dictionary[attr] = {}


def get_time_key(minutes):
    global max_interval
    print 'min', minutes
    max_interval = sorted(max_interval)
    print 'max', max_interval
    for value in max_interval:
        print 'the value is', value
        if( minutes < value):
            return value


def calculate_probability_will_go(year, gender, age, minutes):
    time_key = get_time_key(minutes);
    return probability_will_go[str(year)][gender][age][time_key]
