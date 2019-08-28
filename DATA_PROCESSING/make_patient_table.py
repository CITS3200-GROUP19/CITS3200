import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from fuzzywuzzy import fuzz

from make_all_schemas import BIG_DATA_FILE_PATH, SCHEMA_OUTPUT_FILE_PATH, data

'''get relevant fields from BIG_DATA_FILE (Id, birthdate, fullname)'''
patient_data = data.iloc[:, [2,5]].copy() #data.iloc[:, [0,2,5]].copy()
patient_data = patient_data.drop_duplicates()
print(patient_data.head())
#the patientID field is useless!! Same people have different IDs and same IDs refer to different people
patient_data.columns = ['FullName', 'BirthDate']

'''create new normalised patient table'''
TABLE_NAME = "PATIENT_TABLE.csv"
#Columns: PatientID, PatientFirstName, PatientLastName, PatientDOB
patient_table = pd.DataFrame()
#patient_table.columns = ['PatientID', 'PatientFirstName', 'PatientLastName', 'PatientDOB']

'''Cleaning Names'''
NULL_NAME = "N/A"
NAMES_LIST = []
#cleans name into first/last
def clean_name(row):
    raw_name = row['FullName']
    DOB = row['BirthDate']
    DOB = DOB.replace('-','/')
    for char in raw_name:
        if char.isdigit():
            return pd.Series([NULL_NAME,NULL_NAME,DOB])
    name = raw_name.replace(',',' ').replace('.',' ').strip("'").replace('"','').replace('/','') #some name fields have , and . and ' that need removing

    name = name.upper() #convert all names to UPPERCASE only
    name = name.replace('MRS','').replace('MR','').replace('MR','').replace('DR','') #need to remove titles from some names....
    name = ' '.join(name.split()).strip(' ').split(' ') #remove unneccesary spaces and split on space between names

    #separate into first and last name
    fname = name[-1]
    lname = ' '.join(name[0:-1]) #remake lname if has multiple parts
    new_name_DOB = [fname,lname,DOB]
    rev_name_DOB = [lname,fname,DOB]

    for check_name_DOB in NAMES_LIST:
        #first look for simiar birthdates. IF not, clearly different person hopefully!
        newDMY = DOB.split("/")
        checkDMY = check_name_DOB[2].split("/")
        if fuzz.ratio(DOB,check_name_DOB[2])>82 or (newDMY[0]==checkDMY[1] and newDMY[1]==checkDMY[0] and newDMY[2]==checkDMY[2]):
            #check for name matching within similar birthdates
            if fuzz.ratio(str(new_name_DOB[0:2]),str(check_name_DOB[0:2]))>91 or rev_name_DOB == check_name_DOB:
                return pd.Series(check_name_DOB)
    NAMES_LIST.append(new_name_DOB)
    print(new_name_DOB)
    return pd.Series(new_name_DOB)
'''
all_names = patient_data.iloc[:,0].tolist()
all_DOBs = patient_data.iloc[:,1].tolist()
#sanity checks
print(len(all_DOBs))
same_Names_list=[]
for i in range(len(all_DOBs)):
    if i%100 == 0:
        print(i)
    DOB = all_DOBs[i]
    n = clean_name(all_names[i])
    lname = n[1]
    for j in range(i,len(all_DOBs)):
        m = clean_name(all_names[j])
        if n==m:
            if DOB != all_DOBs[j]:
                if [m,all_names[i],DOB,all_names[j],all_DOBs[j]] not in same_Names_list:
                    same_Names_list.append([m,all_names[i],DOB,all_names[j],all_DOBs[j]])
                    print([m,all_names[i],DOB,all_names[j],all_DOBs[j]])
print(same_Names_list)
#sanity checks
same_Bday_list=[]
for i in range(len(all_DOBs)):
    DOB = all_DOBs[i]
    n = clean_name(all_names[i])
    lname = n[1]
    for j in range(i,len(all_DOBs)):
        if all_DOBs[j] == DOB:
            name2 = all_names[j]
            m = clean_name(name2)
            if n != m:
                if fuzz.ratio(str(n),str(m))>70:
                    if [n,m,DOB] not in same_Bday_list:
                        same_Bday_list.append([n,m,DOB])
print(same_Bday_list)

print(all_names)
'''
'''
patient_data['PatientFirstName'] = patient_data.apply(lambda row: clean_name(row['FullName'])[0], axis=1)
patient_data['PatientLastName'] = patient_data.apply(lambda row: clean_name(row['FullName'])[1], axis=1)
patient_data['PatientDOB']'''

patient_data[['PatientFirstName','PatientLastName','PatientDOB']] = patient_data.apply(clean_name ,axis=1)
#patient_table["PatientFirstName"] = [clean_name(name)[0] for name in all_names]
#patient_table["PatientLastName"] = [clean_name(name)[1] for name in all_names]

print(patient_table.head())

patient_data.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')
