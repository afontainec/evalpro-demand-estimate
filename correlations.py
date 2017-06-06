import Zones
import Population
import Scenarios
import Printer
import csv
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, INTERVALS_LABELS


def check_attr_exists_in_dictionary(attr, dictionary):
    if not attr in dictionary:
        dictionary[attr] = {}

going_proportion = {}
for zone in Zones.get():
    patient_pyramid = Population.get_patient_pyramid(zone)
    shorten_patient_pyramid = Population.shorten_pyramid(patient_pyramid)
    pyramid = Population.get_pyramid(zone, 2017)
    shorten_pyramid = Population.shorten_pyramid(pyramid)
    going_proportion[zone] = {
        'men': {},
        'women': {}
    }
    for label in INTERVALS_LABELS:
        going_proportion[zone]['men'][label] =  shorten_patient_pyramid['men'][label]/ shorten_pyramid['men'][label] if shorten_pyramid['men'][label] else 0
        going_proportion[zone]['women'][label] =  shorten_patient_pyramid['women'][label]/ shorten_pyramid['women'][label] if shorten_pyramid['women'][label] else 0

private_travel = {}
actual_travel = {}

with open('data/travel_time.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        private_travel[row['Unidad Vecinal']] = row['Private']
        actual_travel[row['Unidad Vecinal']] = row['Actual']

walking_time = {}
with open('data/walking_time.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        walking_time[row['Unidad Vecinal']] = row['Actual']

quintiles = {}

with open('data/quintiles.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for q in range(1,6):
            check_attr_exists_in_dictionary(row['zone_id'], quintiles)
            check_attr_exists_in_dictionary(q, quintiles[row['zone_id']])
            quintiles[row['zone_id']][q] = row[str(q)]



##GET TIME correlations
print 'Time correlations...'
for gender in ['men', 'women']:
    for label in INTERVALS_LABELS:
        y_axis = []
        for zone in Zones.get():
            if( zone < 41):
                y_axis.append(going_proportion[zone][gender][label])
        x_axis_private = []
        x_axis_actual = []
        for zone in Zones.get():
            z = str(zone)
            if( zone < 41):
                x_axis_private.append(float(private_travel[z]))
                x_axis_actual.append(float(actual_travel[z]))
        Printer.line_graph(x_axis_private, y_axis, './correlations/time_to_private_pharmacy/'+ gender + '_' + label + '_tendency' + '.png', True)
        Printer.line_graph(x_axis_actual, y_axis, './correlations/time_to_actual_pharmacy/'+ gender + '_' + label + '_tendency' +  '.png', True)
        Printer.line_graph(x_axis_private, y_axis, './correlations/time_to_private_pharmacy/'+ gender + '_' + label + '.png', False)
        Printer.line_graph(x_axis_actual, y_axis, './correlations/time_to_actual_pharmacy/'+ gender + '_' + label + '.png', False)

print 'Time (walking) correlations...'
for gender in ['men', 'women']:
    for label in INTERVALS_LABELS:
        y_axis = []
        for zone in Zones.get():
            if( zone < 41):
                y_axis.append(going_proportion[zone][gender][label])
        x_axis = []
        for zone in Zones.get():
            z = str(zone)
            if( zone < 41):
                x_axis.append(float(walking_time[z]))
        Printer.line_graph(x_axis, y_axis, './correlations/walking_time/'+ gender + '_' + label + '_tendency' + '.png', True)
        Printer.line_graph(x_axis, y_axis, './correlations/walking_time/'+ gender + '_' + label + '.png', False)

## GET QUINTILE CORRELATIONS
print 'Quintile correlations...'
for gender in ['men', 'women']:
    for label in INTERVALS_LABELS:
        y_axis = []
        for zone in Zones.get():
            if( zone < 41):
                y_axis.append(going_proportion[zone][gender][label])
        x_axis = [[],[],[],[],[]]
        x_average = []
        i = -1
        for zone in Zones.get():
            if( zone < 41):
                i += 1
                x_average.append(0)
                z = str(zone)
                for q in range(1,6):
                    x_axis[q - 1].append(float(quintiles[z][q]))
                    x_average[i] += float(quintiles[z][q]) * q
                x_average[i] = x_average[i] / 100
        for q in range(1,6):
            Printer.line_graph(x_axis[q - 1], y_axis, './correlations/quintile_' + str(q) + '/'+ gender + '_' + label + '.png', True)
            Printer.line_graph(x_axis[q - 1], y_axis, './correlations/quintile_' + str(q) + '/'+ gender + '_' + label + '_tendency_' + '.png', False)
        Printer.line_graph(x_average, y_axis, './correlations/quintile_average/'+ gender + '_' + label + '.png', True)
        Printer.line_graph(x_average, y_axis, './correlations/quintile_average/'+ gender + '_' + label + '_tendency_' + '.png', False)


        #             x_axis_.append(private_travel[z])
        #             x_axis_actual.append(actual_travel[z])
        # Printer.line_graph(x_axis_private, y_axis, './correlations/time_to_private_pharmacy/'+ gender + '_' + label + '.png')
        # Printer.line_graph(x_axis_actual, y_axis, './correlations/time_to_actual_pharmacy/'+ gender + '_' + label + '.png')

# porcentage = {}
# with open('patients/raw/total.csv', 'rU') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         porcentage[row['zone']] = row['porcentage']
#
# private_travel = {}
# actual_travel = {}
#
# with open('data/travel_time.csv', 'rU') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         private_travel[row['Unidad Vecinal']] = row['Private']
#         actual_travel[row['Unidad Vecinal']] = row['Actual']
#
# poberty = {}
# with open('data/poberty.csv', 'rU') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         poberty[row['zone']] = row['poberty_level']
#
#
# y_axis = []
# x_axis_private = []
# x_axis_actual = []
# x_axis_poberty = []
#
#
# for zone in Zones.get():
#     z = str(zone)
#     y_axis.append(porcentage[z])
#     x_axis_private.append(private_travel[z])
#     x_axis_actual.append(actual_travel[z])
#     x_axis_poberty.append(poberty[z])
#
#
# Printer.line_graph(x_axis_private, y_axis, './correlations/time_to_private_pharmacy.png')
# Printer.line_graph(x_axis_actual, y_axis, './correlations/time_to_actual_pharmacy.png')
# Printer.line_graph(x_axis_poberty, y_axis, './correlations/poberty.png')
