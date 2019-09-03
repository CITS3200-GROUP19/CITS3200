import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from fuzzywuzzy import fuzz

from get_data import data, SCHEMA_OUTPUT_FILE_PATH
#Columns: EyeID, EyeSide, EyeAcuity
'''get relevant fields from BIG_DATA_FILE (Id, birthdate, fullname)'''
eye_data = data.iloc[:, [0,3,52,54]].copy() #data.iloc[:, [0,2,5]].copy()
eye_data.columns = ['TestID','EyeTested', 'LeftAcuity', 'RightAcuity']

print(eye_data.head())

def get_side_and_acuity(row):
    if row['EyeTested'] == 0:
        side = "Left"
        acuity = row['LeftAcuity']
    elif row['EyeTested'] == 1:
        side = "Right"
        acuity = row['RightAcuity']
    else:
        print("Error",row)
    return pd.Series([side,acuity])

eye_data[['EyeSide','EyeAcuity']] = eye_data.apply(get_side_and_acuity ,axis=1)


'''IDs to be added to the FACT_TABLE!!!'''
eye_data['EyeID'] = eye_data.groupby(['EyeTested','EyeAcuity']).ngroup()
eye_IDs = eye_data['EyeID'].tolist()
print(len(eye_IDs))

eye_data = eye_data.drop(['TestID'], axis=1).drop_duplicates().sort_values(['EyeAcuity'])


'''create new normalised patient table'''
TABLE_NAME = "EYE_TABLE.csv"
#Columns: EyeID, EyeSide, EyeAcuity
eye_table = pd.DataFrame()
eye_table['EyeID'] = eye_data['EyeID']
eye_table['EyeSide'] = eye_data['EyeSide']
eye_table['EyeAcuity'] = eye_data['EyeAcuity']






eye_table.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')

print(eye_table)
