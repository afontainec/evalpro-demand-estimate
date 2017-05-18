import Zones
import PopulationGenerator
import Scenarios
import Printer
import csv
import os
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, AGE_RANGE

for z in Zones.get():
    for year in YEARS:
        content = 'year,total\n'
        with open('./population/zone_' + str(z) + '/raw/pyramid_year_' + str(year) +'.csv', 'rU') as f:
            for l in f:
                content += l
        ff = open('./population/zone_' + str(z) + '/raw/pyramid_year_' + str(year) +'.csv', 'w')

        ff.write(content)
