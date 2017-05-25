import Zones
import Population
import patientsPyramids
import Scenarios
import Printer
import csv
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS



for zone in Zones.get():
    pyramid = patientsPyramids.get_current_pyramid(zone)

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
