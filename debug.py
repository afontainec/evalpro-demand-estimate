import Zones
import Printer
import csv
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, GENDER, AGE_RANGE, INTERVALS_LABELS, INTERVALS


cycle_time = 17


total_time = 249 * (8 - 0.75 * 2) * 60


throughput = total_time/ cycle_time
