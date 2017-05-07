# from main import CURRENT_YEAR, END_YEAR
import Scenarios
import Time
import csv
CURRENT_YEAR = 2017
END_YEAR = 2037
SCENARIO = 2

PORCENTAGE_PRIVATE_PHARMACY = 0.953
COST_OF_TIME = 1688/60
VALUE_OF_GOOD_LIFE = {} #FIXME calculate

AVERAGE_SPENDING_PRIVATE_PHARMACY = {}
AVERAGE_SPENDING_COMUNAL_PHARMACY = {}

def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}

with open('data/value_of_good_life.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for age in range(int(row['range_min']), int(row['range_max']) + 1):
            VALUE_OF_GOOD_LIFE[age] = float(row['value'])

with open('data/average_basket_cost.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for gender in ['men', 'women']:
            check_attr_exists_in_dictionary(gender, AVERAGE_SPENDING_COMUNAL_PHARMACY)
            check_attr_exists_in_dictionary(gender, AVERAGE_SPENDING_PRIVATE_PHARMACY)
            for age in range(int(row['range_min']), int(row['range_max']) + 1):
                AVERAGE_SPENDING_PRIVATE_PHARMACY[gender][age] = row['private_pharmacy']
                AVERAGE_SPENDING_COMUNAL_PHARMACY[gender][age] = row['comunal_pharmacy']






def get_demand(scenario):
    demand = {}
    with open('results/raw/'+ str(scenario) + '.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            check_attr_exists_in_dictionary(row['year'], demand)
            check_attr_exists_in_dictionary(row['zone_id'], demand[row['year']])
            check_attr_exists_in_dictionary(row['age'], demand[row['year']][row['zone_id']])
            check_attr_exists_in_dictionary(row['gender'], demand[row['year']][row['zone_id']][row['age']])
            demand[row['year']][row['zone_id']][row['age']][row['gender']] = row['total']
        return demand

def get_time(zone_id):
    time = 10000000
    for pharmacy in Scenarios.get_pharmacies(SCENARIO):
        time = min(Time.get_time(zone_id, pharmacy), time)
    return time

def get_benefits_and_costs_from_private_pharmacy(zone_id, age, gender, amount):
    time = get_time(zone_id)
    delta_time = float(Time.get_time(zone_id, 'Private')) - float(time)
    saving = float(AVERAGE_SPENDING_PRIVATE_PHARMACY[gender][age]) - float(AVERAGE_SPENDING_COMUNAL_PHARMACY[gender][age])
    return [(saving + delta_time * COST_OF_TIME) * amount, 0]


def get_benefits_and_costs_from_no_pharmacy(zone_id, age, gender, amount):
    time = get_time(zone_id)
    spending =  float(AVERAGE_SPENDING_COMUNAL_PHARMACY[gender][age])
    return [amount * VALUE_OF_GOOD_LIFE[age] / 12, amount * (spending + time * COST_OF_TIME)]

def get_benefits_and_costs_from_comunal_pharmacy(zone_id, amount):
    time = get_time(zone_id)
    return [time * COST_OF_TIME * amount, 0]


base_case_demand = get_demand(1)
scenario_demand =  get_demand(SCENARIO)
Time.init_travel_time()

yearly_benefits = {}
yearly_costs = {}


def get_new_clients(year,zone,age,gender,SCENARIO):
    base_case_total_last_year = 0
    base_case_total_now = float(base_case_demand[year][zone_id][str(age)][gender])
    if(int(year) != CURRENT_YEAR):
        base_case_total_last_year = float(base_case_demand[str(int(year) - 1)][zone_id][str(age)][gender])
    if(SCENARIO == 1):
        return max(base_case_total_now - base_case_total_last_year, 0)
    else:
        total =  scenario_demand[year][zone_id][str(age)][gender]
        base_case_total = base_case_demand[year][zone_id][str(age)][gender]
        return max(float(total) -  float(base_case_total_last_year), 0)

def get_used_to_go_to_comunal_pharmacy(year,zone,age,gender,SCENARIO, new_clients):
    total = scenario_demand[year][zone_id][str(age)][gender]
    return float(total) - new_clients

print 'BENEFITS FOR SCENARIO', str(SCENARIO)
for year in range(CURRENT_YEAR, END_YEAR):
    print 'calculating benefits and costs of ', year
    benefits = 0
    costs = 0
    year = str(year)
    for zone_id in scenario_demand[year]:
        for age in range(0,101):
            for gender in ['men', 'women']:
                # total =  scenario_demand[year][zone_id][str(age)][gender]
                # base_case_total = base_case_demand[year][zone_id][str(age)][gender]
                # new_clients = float(total) - float(base_case_total)
                new_clients = get_new_clients(year, zone_id, age, gender, SCENARIO)
                if( new_clients < 0):
                    print 'should not print this'
                    print total, base_case_total
                    0/0 # Drop script
                used_to_go_to_private_pharmacy = PORCENTAGE_PRIVATE_PHARMACY * new_clients
                did_not_buy_medicine = (1 - PORCENTAGE_PRIVATE_PHARMACY) * new_clients
                used_to_go_to_comunal_pharmacy = get_used_to_go_to_comunal_pharmacy(year,zone_id,age,gender,SCENARIO, new_clients)
                b_and_c_i = get_benefits_and_costs_from_private_pharmacy(zone_id, age, gender, used_to_go_to_private_pharmacy)
                b_and_c_ii = get_benefits_and_costs_from_no_pharmacy(zone_id, age, gender, did_not_buy_medicine)
                b_and_c_iii = get_benefits_and_costs_from_comunal_pharmacy(zone_id, used_to_go_to_comunal_pharmacy)
                benefits += b_and_c_i[0]
                benefits += b_and_c_ii[0]
                benefits += b_and_c_iii[0]
                costs += b_and_c_i[1]
                costs += b_and_c_ii[1]
                costs += b_and_c_iii[1]
    yearly_benefits[str(year)] = benefits
    yearly_costs[str(year)] = costs


f = open('./results/benefits/' + str(SCENARIO) + '.csv', 'w')
line = 'year,benefit,cost\n'
f.write(line)
for year in range(CURRENT_YEAR, END_YEAR):
    line = str(year) + "," + str(yearly_benefits[str(year)]) + "," + str(yearly_costs[str(year)])
    f.write(line)
    f.write('\n')














# # PSEUDO CODIGO:
# for year
#     for zones
#         total = demanda[year][zones]
#         total_caso_base = demanda_caso_base[year][zones]
#         nuevos = max(total - total_caso_base, 0)
#         iban_farmacia_privada = %_farmacia_priv * nuevos
#         no_compraba = (1 - %_farmacia_priv) * nuevos
#         ya_van_farmacia_comunal = total_caso_base
#         b_zona += beneficio_ya_van_farmacia_comunal(ya_van_farmacia_comunal)
#         b_zona += beneficio_no_compraba(no_compraba)
#         b_zona += beneficio_compraba_privada(iban_farmacia_privada)

#
#
#
# beneficio_ya_van_farmacia_comunal(cantidad):
#     tiempo = max_tiempo
#     for farmacia in escenario.farmacias:
#         tiempo = min(tiempo_a(farmacia), tiempo)
#     tiempo_antes = tiempo_a(municipalidad)
#     tiempo_ganado =  tiempo_antes - tiempo
#     return tiempo_ganado * valor_del_tiempo * cantidad
#
# beneficio_no_compraba(cantidad):
#     tiempo = max_tiempo
#     for farmacia in escenario.farmacias:
#         tiempo = min(tiempo_a(farmacia), tiempo)
#     costo_en_tiempo = tiempo * valor_del_tiempo
#     costo_en_dinero = gasto_promedio('Comunitaria')
#     return cantidad * (ganancia_en_vida - costo_en_tiempo - costo_en_dinero)
#
# beneficio_compraba_privada(cantidad):
#     tiempo = max_tiempo
#     for farmacia in escenario.farmacias:
#         tiempo = min(tiempo_a(farmacia), tiempo)
#     delta_tiempo = tiempo_a('Privada') - tiempo
#     ahorro = gasto_promedio('Privada') - gasto_promedio('Comunitaria')
#     return (ahorro + delta_tiempo * valor_del_tiempo) * cantidad
