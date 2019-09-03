import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from fuzzywuzzy import fuzz

from get_data import data, SCHEMA_OUTPUT_FILE_PATH

'''get relevant fields from BIG_DATA_FILE (Id, birthdate, fullname)'''
defect_data = data.iloc[:, [0,73,74,75]].copy() #data.iloc[:, [0,2,5]].copy()
reliability_data.columns = ['TestID','ReliabilityScore', 'ReliabilityDesc', 'ReliabilityColour']

print(reliability_data.head())


'''IDs to be added to the FACT_TABLE!!!'''
defects_IDs = reliability_data['ReliabilityID'].tolist()
print(len(reliability_IDs))

reliability_data = reliability_data.drop(['TestID'], axis=1).drop_duplicates().sort_values(['ReliabilityScore'])


'''create new normalised patient table'''
TABLE_NAME = "DEFECTS_TABLE.csv"
#Columns: DefectID, DefectExists (1 means atleast 1 defect, 0 means no defects), DefectString (0001100011)



reliability_table.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')

print(reliability_table)
