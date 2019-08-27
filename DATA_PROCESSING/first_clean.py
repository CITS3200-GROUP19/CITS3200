import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil


PATH = "/USER/localadmin/Desktop/StalingEnergy/"
DATA = "proc0_raw_data/"
OUTPUT = "proc1_columns_checked/"

#clear existing files
shutil.rmtree(OUTPUT)
os.makedirs(OUTPUT)

column_set = ['SerialNumber', 'TimeStamp (UTC)', 'PV Power (W)', 'Main Load Power (W)', 'Backup Load Power (W)', 'Grid Power (W)', 'PV Day Total Energy (kWh)', 'Main Load Day Total Energy (kWh)', 'Backup Load Day Total Energy (kWh)', 'Load Day Total Energy (kWh)', 'PV1 Voltage (V)', 'PV2 Voltage (V)', 'Grid Voltage (V)', 'Battery Power (W) (negative = charging)', 'Battery Voltage (V)', 'Battery Current (A)', 'Battery SoC (%)', 'Battery Day Total Import Energy (kWh)', 'Battery Day Total Export Energy (kWh)', 'Battery Cabinet Temperature (Celsius)', 'Errors', 'Grid Export Day Total Energy (kWh)', 'Grid Import Day Total Energy (kWh)', 'Grid Status', 'ROSS version', 'OS version', 'Work Mode', 'Work Mode Power (W)', 'Inverter Work Mode']

filenames = sorted(glob.glob(DATA+'RB*.csv'))
print("Files to clean: {0}".format(filenames))
for file in filenames:
    print('>>> ' +str(file))
    data = pd.read_csv(file, low_memory=False)
    columns = data.columns.tolist()
