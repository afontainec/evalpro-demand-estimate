import csv
import pandas as pd
import numpy as np

probability_will_go = {}


_all_ranges = np.array([
                np.arange(0, 9+1),
               np.arange(10, 19+1),
               np.arange(20, 44+1),
               np.arange(45, 64+1),
               np.arange(65, 79+1),
               np.arange(80, 200+1)
              ])





def init_probabilites(pharmacies = None):
    global probability_will_go
    probability_will_go = pd.read_csv('./data/data_probabilities').set_index(['sexo','unidad','rango'])



def select_range(x, r):

    for i, _ in enumerate(r):
        if int(x) in _:
            return i
    return i

string_all_ranges = ['[0, 9]',
               '[10, 19]',
               '[20, 44]',
               '[45, 64]',
               '[65, 79]',
               '[80, 200]'
              ]



# _zones_san_luis = {25:41, 28:40, 24:42, 22:43, }
_zones_san_luis ={23:43, 25:42, 28:43, 24:43, 22:43, 20:6}

def calculate_probability_will_go(month, gender, zone_id, age, scenario = 1):
    _zone_id = zone_id

    if scenario == 2 and int(zone_id) in _zones_san_luis:
        _zone_id = _zones_san_luis[int(zone_id)]

    _range = string_all_ranges[select_range(age, _all_ranges)]

    if not (gender,int(_zone_id),_range) in probability_will_go.index:
        return 0.000774

    old_index, ponderador, a, b, c, d, prob, tiempo =  probability_will_go.loc[(gender,int(_zone_id),_range)]

    div = 972/1.5
    _nx = month
    _ret = (a*_nx + b*_nx**2 + c*np.log(_nx)/np.log(d))/div

    if _ret == -1 *np.infty:
        print ' fin calcular p', _ret, _nx, np.log(_nx), a, b, c, d, np.log(d), div
        print 'QUEDDOOOO LLA PATADAAA\n\n\n\n\n\n\n\n\n\n\n'
        0/0

    return _ret
