import csv
import pandas as pd
import numpy as np

probability_will_go = {}

max_interval = [15, 25, 40,60, 1000]





def init_probabilites(pharmacies):
    global probability_will_go
    probability_will_go = pd.read_csv('data_probabilities').set_index(['sexo','unidad','rango'])




# def probabilities(pharmacy):
#     global probability_will_go
#     probability_will_go[pharmacy] = {}
#     with open('data/probability_will_go_' + pharmacy + '.csv', 'rU') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             check_attr_exists_in_dictionary(row['year'], probability_will_go[pharmacy])
#             check_attr_exists_in_dictionary(row['gender'], probability_will_go[pharmacy][row['year']])
#             for age in range(int(row['min_age']), int(row['max_age']) + 1):
#                 check_attr_exists_in_dictionary(age, probability_will_go[pharmacy][row['year']][row['gender']])
#                 probability_will_go[pharmacy][row['year']][row['gender']][age][max_interval[0]] = row['between_0_and_15']
#                 probability_will_go[pharmacy][row['year']][row['gender']][age][max_interval[1]] = row['between_15_and_25']
#                 probability_will_go[pharmacy][row['year']][row['gender']][age][max_interval[2]] = row['between_25_and_40']
#                 probability_will_go[pharmacy][row['year']][row['gender']][age][max_interval[3]] = row['between_40_and_60']
#                 probability_will_go[pharmacy][row['year']][row['gender']][age][max_interval[4]] = row['between_60_and_1000']



def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}


def get_time_key(minutes):
    global max_interval
    max_interval = sorted(max_interval)
    for value in max_interval:
        if( minutes < value):
            return value


def calculate_probability_will_go(month, gender, age, zone_id, pharmacy):
    return 0.5




# coding: utf-8

# In[1]:




# In[2]:



# In[2]:

_all_ranges = np.array([
                np.arange(0, 9+1),
               np.arange(10, 19+1),
               np.arange(20, 44+1),
               np.arange(45, 64+1),
               np.arange(65, 79+1),
               np.arange(80, 200+1)
              ])

def select_range(x, r):
    for i, _ in enumerate(r):
        if x in _:
            return i
    return i

string_all_ranges = ['[0, 9]',
               '[10, 19]',
               '[20, 44]',
               '[45, 64]',
               '[65, 79]',
               '[80, 200]'
              ]


# In[5]:

_unidades_san_luis = {25:41, 28:40, 24:42, 22:43}

def prob(meses_desde_apertura, sexo, unidad, edad, farmacia = 'Municipalidad'):
    _unidad = unidad

    if farmacia == 'San_Luis' and unidad in _unidades:
        _unidad = _unidades_san_luis[unidad]

    _range = string_all_ranges[select_range(edad, _all_ranges)]
    ponderador, a, b, c, d, prob, tiempo =  data_ponderadores.loc[(sexo,int(_unidad),_range)]

    div = 972
    _nx = meses_desde_apertura
    _ret = (a*_nx + b*_nx**2 + c*np.log(_nx)/np.log(d))/div

    return _ret


# In[6]:

prob(40, 'masculino', 25, 50, 'san_luis')


# In[ ]:
