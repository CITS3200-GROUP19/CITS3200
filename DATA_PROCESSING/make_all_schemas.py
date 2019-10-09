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
import make_patient_table
#Columns: PatientID, PatientFirstName, PatientLastName, PatientDOB

#build RELIABILITY table
import make_reliability_table
#Columns: ReliabilityID, ReliabilityGiven, ReliabilityColour, ReliabilityDesc, ReliabilityScore

#build DEFECTS table
import make_defect_table
#Columns: DefectID, DefectNumberOf, DefectCombination

#build EYE table
import make_eye_table
#Columns: EyeID, EyeSide, EyeAcuity

#build HUMPHREY table
import make_humphrey_table
#Columns: HumphreyID, H1, H2, H3, ... H76

#make fact_table here...
#Columns Test_ID, (schema IDs...), Date, Runtime, Mean_Deviation, Pattern_Deviation, Age

TABLE_NAME = "FACT_TABLE.csv"
FACT_TABLE = pd.DataFrame()
FACT_TABLE['Test_ID'] = data.iloc[:,0].copy().tolist()
FACT_TABLE['Defect_ID'] = pd.Series(make_defect_table.defect_IDs) #from make_reliability file
#FACT_TABLE['Humphrey_ID'] = pd.Series(make_humphrey_table.humphrey_IDs) #from make_reliability file
FACT_TABLE['Eye_ID'] = pd.Series(make_eye_table.eye_IDs) #from make_reliability file
FACT_TABLE['Patient_ID'] = pd.Series(make_patient_table.patient_IDs) #from make_reliability file
FACT_TABLE['Reliability_ID'] = pd.Series(make_reliability_table.reliability_IDs) #from make_reliability file


FACT_TABLE['Date'] = data.iloc[:,1].copy().tolist()
FACT_TABLE['Runtime'] = data.iloc[:,10].copy().tolist()
FACT_TABLE['Mean_Deviation'] = data.iloc[:,55].copy().tolist()
FACT_TABLE['Pattern_Deviation'] = data.iloc[:,56].copy().tolist()

def get_age(row):
    date = row['Date']
    #need to get cleaned DOB...
    PatientID = row['Patient_ID']
    df = make_patient_table.patient_data
    DOB = df.loc[df["PatientID"] == PatientID]['PatientDOB']
    print(DOB)
    if DOB.empty:
        return 0
    else:
        DOB=DOB.values[0]
        #compute age
        age = pd.to_datetime(date) - pd.to_datetime(DOB)
        age = int(age.days / (365.25))
    return age

FACT_TABLE['Age'] = FACT_TABLE.apply(get_age, axis=1)

print(FACT_TABLE.head())
FACT_TABLE.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')
