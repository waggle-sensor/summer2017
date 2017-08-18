# Analyzes and Plots Chemical data from SpecSensors (to be used in conjunction with Chemsense_Spec_Data.xlsx
import dataset
import xlrd
import math
import numpy as np
import matplotlib.pyplot as plt

# Instance Variables
BOARDNAME = '04A3E2BD29' # name of the board
CHEMICAL = 'NO2' # chemical (either IRR, IAQ, SO2, H2S, OZO, NO2, or CMO)
INSTANTTEMP = 26.0 # the temperature at the moment of measurement
INSTANTCURRENT = 2492 # the current at the moment of measurement
# Calibration Parameters
directory = "./Chemsense_Spec_Data.xlsx" # directory of the sensor data
ZEROTEMP = 25.0 # initial temperature

# creates a dataset and opens the excel sensor data
db = dataset.connect()
table = db.create_table('stats')
xl = xlrd.open_workbook(directory, "rb")
sheet = xl.sheet_by_name('Sheet1')

# inserts every column of the excel workbook into the dataset
# column names: board, IRR_baseline,IAQ_baseline, SO2_baseline, H2S_baseline,
#               OZO_baseline, NO2_baseline, CMO_baseline, IRR_M, IAQ_M, SO2_M,
#               H2S_M, OZO_M, NO2_M,CMO_M, IRR_Sensitivity, IAQ_Sensitivity,
#               SO2_Sensitivity, H2S_Sensitivity, OZO_Sensitivity,
#               NO2_Sensitivity, and CMO_Sensitivity

for rownum in range(sheet.nrows):
    rowValues = sheet.row_values(rownum)
    table.insert(dict(board = rowValues[0], IRR_baseline = rowValues[1],
        IAQ_baseline = rowValues[2], SO2_baseline = rowValues[3],
        H2S_baseline = rowValues[4], OZO_baseline = rowValues[5],
        NO2_baseline = rowValues[6], CMO_baseline = rowValues[7],
        IRR_M = rowValues[8], IAQ_M = rowValues[9], SO2_M = rowValues[10],
        H2S_M = rowValues[11], OZO_M = rowValues[12], NO2_M = rowValues[13],
        CMO_M = rowValues[14], IRR_Sensitivity = rowValues[15],
        IAQ_Sensitivity = rowValues[16], SO2_Sensitivity = rowValues[17],
        H2S_Sensitivity = rowValues[18], OZO_Sensitivity = rowValues[19],
        NO2_Sensitivity = rowValues[20], CMO_Sensitivity = rowValues[21]))

# finds the baseline current and m time-constant based on the name of the board
# and the given chemical
results = table.find(board = BOARDNAME)
for row in results:
    baseline = (row[CHEMICAL + '_baseline'])
    MValue = (row[CHEMICAL + '_M'])
    sensitivity = (row[CHEMICAL + '_Sensitivity'])

baseline = float(baseline)
MValue = float(MValue)
sensitivity = float(sensitivity)

# calculates the value of the corrected current
# ICORRECTED = INSTANTCURRENT - baseline * math.exp((INSTANTTEMP - ZEROTEMP)/MValue)

ICorrectedList = []
for i in range(-40, 45):
    INSTANTTEMP = i
    if MValue == 'INFINITY':
        ICORRECTED = INSTANTCURRENT - baseline #if the M value is infinity, the exponent dissapears
    else:
        ICORRECTED = INSTANTCURRENT - baseline * math.exp((INSTANTTEMP - ZEROTEMP)/MValue)
    toAppend = ICORRECTED/sensitivity
    ICorrectedList.append(toAppend)

ICorrectedArray = np.array(ICorrectedList)
TempArray = np.array(range(-40,45))

plt.xlabel('Temperature')
plt.ylabel('ICorrected')
plt.title('Temperature vs ICorrected')
plt.grid(True)
plt.plot(TempArray, ICorrectedArray)
# plt.savefig("testGraph.png")
plt.show()
