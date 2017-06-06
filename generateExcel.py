import xlsxwriter
from Global import INITIAL_YEAR, FINAL_YEAR, YEARS, GENDER, AGE_RANGE, INTERVALS_LABELS, INTERVALS, ANNUAL_THROUGHPUT



add_years()

# Create a workbook and add a worksheet.
def add_flujos(workbook):
    worksheet = workbook.add_worksheet('flujos')

    # Some data we want to write to the worksheet.
    non_social_titles = ['Ingresos por Ventas', 'Costos por Ventas', 'Margen Bruto',
    'Gasto por arriendo',
    'Gasto en Sueldos',
    'Gasto otros (electricidad, agua, etc)',
    'Utilidad Operacional',
    'Costos de instalación',
    'R. del Ejercicio']

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    worksheet = workbook.add_worksheet('segunda')

    # Some data we want to write to the worksheet.
    expenses = (
        ['Raent', 1000],
        ['Gaasdfs',   -100],
        ['Foddddod',  00],
        ['Gymi',    500],
    )

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1


#-------------------------------------------------------------------------- CODE -----------------------------------------------------------
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
add_flujos(workbook)
workbook.close()
