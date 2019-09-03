#Created 27th August 2019 Alex Rohl
import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from pathlib import Path
from get_data import data, SCHEMA_OUTPUT_FILE_PATH

#build PATIENT table
#import make_patient_table
#Columns: PatientID, PatientFirstName, PatientLastName, PatientDOB

#build RELIABILITY table
#import make_reliability_table
#Columns: ReliabilityID, ReliabilityGiven, ReliabilityColour, ReliabilityDesc, ReliabilityScore

#build DEFECTS table
#import make_defects_table
#Columns: DefectID, DefectExists, DefectCombination

#build EYE table
import make_eye_table
#Columns: EyeID, EyeSide, EyeAcuity


#make fact_table here...
#Columns Test_ID, Date, Runtime, Mean_Deviation, Pattern_Deviation, Age
FACT_TABLE = pd.DataFrame()
FACT_TABLE['Test_ID'] = data.iloc[:,0].copy().tolist()
FACT_TABLE['Eye_ID'] = pd.Series(make_eye_table.eye_IDs) #from make_reliability file
'''
FACT_TABLE['Patient_ID'] = pd.Series(make_patient_table.patient_IDs) #from make_reliability file
FACT_TABLE['Reliability_ID'] = pd.Series(make_reliability_table.reliability_IDs) #from make_reliability file
'''

print(FACT_TABLE.head())
