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
reliability_data = data.iloc[:, [0,73,74,75]].copy() #data.iloc[:, [0,2,5]].copy()
reliability_data.columns = ['TestID','ReliabilityScore', 'ReliabilityDesc', 'ReliabilityColour']
'''
patient_data["count"] = patient_data.groupby(patient_data.columns.tolist(),as_index=False).size()
patient_data = patient_data.drop_duplicates().head(100)
'''
#patient_data = patient_data.groupby(patient_data.columns.tolist()).size().reset_index().rename(columns={0:'Count'})

print(reliability_data.head())
count = 0
def clean_reliability(row):
    global count
    allowed_scores = [0,1,2,3,4,5,6,7]
    allowed_colours = ['Green','Red']
    allowed_desc = ["Low patient reliability","Moderate patient reliability","Good patient reliability","Excellent patient reliability"]
    reli_row = [row['ReliabilityScore'],row['ReliabilityDesc'],row['ReliabilityColour']]
    for score in allowed_scores:
        for colour in allowed_colours:
            for desc in allowed_desc:
                if [score,desc,colour] == reli_row:
                    return pd.Series(reli_row)
    count += 1
    return pd.Series([-1,'NA','NA'])

#clean unrecognisable ID scores
reliability_data[['ReliabilityScore','ReliabilityDesc','ReliabilityColour']] = reliability_data.apply(clean_reliability ,axis=1)
print("{0} unrecognisable rows replaced".format(count))
#create reliability IDs
reliability_data['ReliabilityID'] = reliability_data.groupby(['ReliabilityScore','ReliabilityDesc','ReliabilityColour']).ngroup()

def has_reliability(row):
    if row['ReliabilityScore'] == -1:
        return "No"
    else:
        return "Yes"

reliability_data['ReliabilityExists'] = reliability_data.apply(has_reliability ,axis=1)

'''IDs to be added to the FACT_TABLE!!!'''
reliability_IDs = reliability_data['ReliabilityID'].tolist()
print(len(reliability_IDs))

reliability_data = reliability_data.drop(['TestID'], axis=1).drop_duplicates().sort_values(['ReliabilityScore'])


'''create new normalised patient table'''
TABLE_NAME = "RELIABILITY_TABLE.csv"
#Columns: ReliabilityID, ReliabilityExists, ReliabilityColour, ReliabilityDesc, ReliabilityScore
reliability_table = pd.DataFrame()
reliability_table['ReliabilityID'] = reliability_data['ReliabilityID']
reliability_table['ReliabilityExists'] = reliability_data['ReliabilityExists']
reliability_table['ReliabilityColour'] = reliability_data['ReliabilityColour']
reliability_table['ReliabilityDesc'] = reliability_data['ReliabilityDesc']
reliability_table['ReliabilityScore'] = reliability_data['ReliabilityScore']


reliability_table.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')

print(reliability_table)
