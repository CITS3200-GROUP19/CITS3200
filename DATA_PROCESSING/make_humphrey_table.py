import os
import csv
import re
import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from fuzzywuzzy import fuzz

from get_data import data, SCHEMA_OUTPUT_FILE_PATH
#Columns: humphreyID, humphreySide, humphreyAcuity
'''get relevant fields from BIG_DATA_FILE (Id, birthdate, fullname)'''
humphrey_data = data.iloc[:, [0,79]].copy() #data.iloc[:, [0,2,5]].copy()
humphrey_data.columns = ['TestID','HumphreyData']

print(humphrey_data.head())

def extract(row): ## match left humphrey, right humphrey positions with correct humphry values in a dictionary, such that a csv
                ## file can be made with the index representing position and the humphry value in the cell.
    extractedData = [] ## stores list of lists containing final humphry values in correct positions
    values = []
    rightPositions = [22,6,7,12,13,14,20,21,23,29,30,31,32,33,25,8,9,15,
16,17,24,26,27,34,35,36,37,55,44,45,46,47,54,56,57,63,64,65,70,71,
52,39,40,41,42,43,50,51,53,60,61,62,68,69]
    leftPositions = [25,9,8,17,16,15,27,26,24,38,37,36,35,34,22,7,6,14,
13,12,23,22,20,33,32,31,30,52,43,42,41,40,53,51,50,62,61,60,69,
68,55,48,47,46,45,44,57,56,54,65,64,63,70,71]
    count = 0
    raw = row['HumphreyData']
    n = 2
    raw = str(raw)
    values = re.findall('..', raw) ## converts raw values into a list of double digit numbers (as strings temporarily)
    for i in range(0,len(values)):
        print(values)
        values[i] = int(values[i]) ## converts all values back to integer from string
    if(int(row[3])): ##is right humphrey
        mapping = dict(zip(rightPositions, values))
    else: ##is left humphrey
        mapping = dict(zip(leftPositions, values))
    templist = []
    for i in range (0, 77):
        templist.append(mapping.get(i, "-")) ##creates list of humphry values in its corresponding position as the
                                            ##index of the list, if there is no value in the index position, -
    print(templist)
    return(pd.Series(templist))

columns = ['H'+str(i) for i in range(1,77)]

humphrey_data[columns] = humphrey_data.apply(extract ,axis=1)


'''IDs to be added to the FACT_TABLE!!!'''
humphrey_data['HumphreyID'] = humphrey_data.groupby(columns).ngroup()
humphrey_IDs = humphrey_data['HumphreyID'].tolist()
print(len(humphrey_IDs))

humphrey_data = humphrey_data.drop(['TestID'], axis=1).drop_duplicates().sort_values(columns)


'''create new normalised patient table'''
TABLE_NAME = "humphrey_TABLE.csv"
#Columns: humphreyID, humphreySide, humphreyAcuity
humphrey_table = pd.DataFrame()
humphrey_table['HumphreyID'] = humphrey_data['HumphreyID']
humphrey_table[columns] = humphrey_data[columns]

humphrey_table.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')

print(humphrey_table)
