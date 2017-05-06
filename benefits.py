from main import SCENARIO, CURRENT_YEAR, END_YEAR
import Scenario
import Time
import csv


TIME_TO_PRIVATE_PHARMACY = 11
%_PRIVATE_PHARMACY = 0.5 #FIXME calculate from poll
COST_OF_TIME = 1 #FIXME calculate 


base_case_demand = get_demand(1);
scenario_demand =  get_demand(SCENARIO)
Time.init_travel_time()



def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}

def get_demand(scenario):
    demand = {}
    with open('results/raw/'+ str(scenario) + '.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            check_attr_exists_in_dictionary(row['year'], demand)
            check_attr_exists_in_dictionary(row['zone_id'], demand[row['year']])
            demand[row['year']][row['zone_id']] = row['total']
        return demand



for year in range(CURRENT_YEAR, END_YEAR):
    for zone_id in demand[year]:
        print year, zone_id
            total =  scenario_demand[year][zone_id]
            base_case_total = scenario_demand[year][zone_id]
            new_clients = total - base_case_total
            if( new_clients < 0):
                print 'should not print this'
                print total, base_case_total
                0/0 # Drop script
            used_to_go_to_private_pharmacy = %_PRIVATE_PHARMACY * new_clients
            did_not_buy_medicine = (1 - %_PRIVATE_PHARMACY) * new_clients
            used_to_go_to_comunal_pharmacy = base_case_total


def get_time(zone_id):
    time = 10000000
    for pharmacy in Scenario.get_pharmacies(SCENARIO):
        time = min(Time.get_time(zone_id, pharmacy), time)

def get_benefits_from_private_pharmacy( amount):



def get_benefits_from_no_pharmacy( amount):

def get_benefits_from_comunal_pharmacy(zone_id, amount):
    time = get_time(zone_id)
    return time * COST_OF_TIME * amount










# PSEUDO CODIGO:
for year
    for zones
        total = demanda[year][zones]
        total_caso_base = demanda_caso_base[year][zones]
        nuevos = max(total - total_caso_base, 0)
        iban_farmacia_privada = %_farmacia_priv * nuevos
        no_compraba = (1 - %_farmacia_priv) * nuevos
        ya_van_farmacia_comunal = total_caso_base
        b_zona += beneficio_ya_van_farmacia_comunal(ya_van_farmacia_comunal)
        b_zona += beneficio_no_compraba(no_compraba)
        b_zona += beneficio_compraba_privada(iban_farmacia_privada)




beneficio_ya_van_farmacia_comunal(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    tiempo_antes = tiempo_a(municipalidad)
    tiempo_ganado =  tiempo_antes - tiempo
    return tiempo_ganado * valor_del_tiempo * cantidad

beneficio_no_compraba(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    costo_en_tiempo = tiempo * valor_del_tiempo
    costo_en_dinero = gasto_promedio('Comunitaria')
    return cantidad * (ganancia_en_vida - costo_en_tiempo - costo_en_dinero)

beneficio_compraba_privada(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    delta_tiempo = tiempo_a('Privada') - tiempo
    ahorro = gasto_promedio('Privada') - gasto_promedio('Comunitaria')
    return (ahorro + delta_tiempo * valor_del_tiempo) * cantidad
