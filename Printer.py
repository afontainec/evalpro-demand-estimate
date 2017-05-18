import matplotlib.pyplot as plt
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, AGE_RANGE


def pyramid_to_file(obj, path):
    f = open(path, 'w')
    line = 'age,men,women,total\n'
    f.write(line)
    for age in AGE_RANGE:
        line = str(age) + "," + str(obj['men'][age]) + "," + str(obj['women'][age])  + "," + str((obj['men'][age] + obj['women'][age]))
        f.write(line)
        f.write('\n')

def age_to_array(obj):
    array = []
    for age in AGE_RANGE:
        array.append(obj[age])
    return array

def print_total_population(obj, path):
    f = open(path, 'w')
    line = 'year,total\n'
    f.write(line)
    i = INITIAL_YEAR
    for value in obj:
        line = str(i) + ',' + str(value)
        f.write(line)
        f.write('\n')
        i += 1

def served_market(zones, total, porcentage, path):
    f = open(path, 'w')
    line = 'zone,total,porcentage\n'
    f.write(line)
    for zone in zones:
        z = str(zone)
        line = z + ',' + str(total[z]) + ',' + str(porcentage[z])
        f.write(line)
        f.write('\n')







def pyramid_to_image(obj, path):
    y = AGE_RANGE
    x1 = age_to_array(obj['men'])
    x2 = age_to_array(obj['women'])
    fig, axes = plt.subplots(ncols=2, sharey=True)
    plt.xlabel('Hombres (Rojo), Mujeres (Azul)', fontsize=18)
    axes[0].barh(y, x1, align='center', color='red')
    axes[1].barh(y, x2, align='center', color='blue')
    axes[0].invert_xaxis()
    plt.savefig(path)
    plt.close(fig)


def line_graph(xAxis, yAxis, path):
    plt.plot(xAxis, yAxis, 'ro')
    # plt.axis([0, 6, 0, 20])
    plt.savefig(path)
    plt.close()
