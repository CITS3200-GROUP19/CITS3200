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
patient_data = data.iloc[:, [2,4,5]].copy() #data.iloc[:, [0,2,5]].copy()
patient_data.columns = ['FullName', 'OriginalID', 'BirthDate']
'''
patient_data["count"] = patient_data.groupby(patient_data.columns.tolist(),as_index=False).size()
patient_data = patient_data.drop_duplicates().head(100)
'''
patient_data = patient_data.groupby(patient_data.columns.tolist()).size().reset_index().rename(columns={0:'Count'})
patient_data = patient_data

print(patient_data.head())
#the patientID field is useless!! Same people have different IDs and same IDs refer to different people... or no IDs at all...

'''create new normalised patient table'''
TABLE_NAME = "PATIENT_TABLE.csv"
#Columns: PatientID, PatientFirstName, PatientLastName, PatientDOB
patient_table = pd.DataFrame()
#patient_table.columns = ['PatientID', 'PatientFirstName', 'PatientLastName', 'PatientDOB']

'''Cleaning Names'''
NULL_NAME = "N/A"
NAMES_LIST = []

#when we find matches we have to decide which spelling/DOB to keep... will go on commonality.
def keep_most_common_name(name_count1,name_count2,list):
    #name1 already in list.
    if name_count1[-1] >= name_count2[-1]:
        if name_count1[0:2]!=name_count2[0:2]:
            print("{0} matched with and was replaced by {1}".format(name_count2,name_count1))
        return list
    else:
        #new name has a higher count so use this instead.
        list.remove(name_count1)
        list.append(name_count2)
        if name_count1[0:2]!=name_count2[0:2]:
            print("{0} matched with and has replaced {1}".format(name_count2,name_count1))
        return list

#groups patients based on similar birthdates and similar names in order to match misentered data.
#this is only a 'rough' clean since we still have cases of nicknames/maidennames being used
#print statements will show which names have been matched...
def rough_clean_name(row):
    global NAMES_LIST
    raw_name = row['FullName'] #name on raw file

    DOB = row['BirthDate'] #DOB on file
    DOB = DOB.replace('-','/')

    count = row['Count']

    #remove any glitched(?) names that contain numbers e.g. "1086RMTN-2.00-2.75X070"
    for char in raw_name:
        if char.isdigit():
            return pd.Series([NULL_NAME,NULL_NAME,DOB])

    #basic character manipulation to make naming structure consistent.
    name = raw_name.replace(',',' ').replace('.',' ').replace("'",'').replace('"','').replace('/','').replace('[','').replace("]",'') #some name fields have , and . and ' that need removing
    name = name.replace("(",'').replace(")",'') #some cases have prefered names in ( ) will treat these as middle names...
    name = name.upper() #convert all names to UPPERCASE only
    name = name.replace('MRS ','').replace('MR ','').replace('MR ','').replace('DR ','').replace(' MRS','').replace(' MR','').replace(' MR','').replace(' DR','') #need to remove titles from some names....
    name = ' '.join(name.split()).strip(' ').split(' ') #remove unneccesary spaces and split on space between names

    #separate into first and last name
    fname = name[-1]
    lname = ' '.join(name[0:-1]) #remake lname if has multiple parts
    new_name_DOB = [fname,lname,DOB,count]
    #case where first and last names have been entered in different orders...
    rev_name_DOB = [lname,fname,DOB,count]

    for check_name_DOB in NAMES_LIST:
        #first look for simiar birthdates. IF not, clearly different person hopefully!
        newDMY = DOB.split("/")
        checkDMY = check_name_DOB[2].split("/")
        if fuzz.ratio(DOB,check_name_DOB[2])>82 or (newDMY[0]==checkDMY[1] and newDMY[1]==checkDMY[0] and newDMY[2]==checkDMY[2]):
            #check for name matching within similar birthdates
            if fuzz.ratio(str(new_name_DOB[0:2]),str(check_name_DOB[0:2]))>91 or fuzz.ratio(str(rev_name_DOB[0:2]),str(check_name_DOB[0:2]))>91:
                NAMES_LIST = keep_most_common_name(check_name_DOB,new_name_DOB, NAMES_LIST)
                return pd.Series(check_name_DOB[0:3])
    NAMES_LIST.append(new_name_DOB)
    return pd.Series(new_name_DOB[0:3])



CLEAN_NAMES_LIST = []
#Assuming DOB is now all cleaned up...
#now check specifically for cases of patients with same birthdates
#if the original IDs are close enough and one first/last name pair matches then we group as one person
def fine_clean_name(row):
    global CLEAN_NAMES_LIST
    clean_fname = row['PatientFirstName']
    clean_lname = row['PatientLastName']
    clean_DOB = row['PatientDOB']
    clean_ID = str(row['OriginalID']).replace("/",'')
    if clean_fname == NULL_NAME:
        count = 0
    else:
        count = row['Count']
    new_name_DOB = [clean_fname,clean_lname,clean_DOB,clean_ID,count]
    for check_name_DOB in CLEAN_NAMES_LIST:
        check_fname, check_lname, check_DOB, check_ID = check_name_DOB[0], check_name_DOB[1], check_name_DOB[2], check_name_DOB[3]
        if check_DOB == clean_DOB:
            #found DOB match
            if fuzz.ratio(check_ID,clean_ID) > 70 and len(check_ID)>3 and len(clean_ID)>3:
                #found similar ID
                CLEAN_NAMES_LIST = keep_most_common_name(check_name_DOB,new_name_DOB, CLEAN_NAMES_LIST)
                return pd.Series(check_name_DOB[0:3])
            else:
                #IDs vastly different...
                if check_lname == clean_lname:
                    #found matching lastname
                    if check_fname[0] == clean_fname[0]:
                        #matching first letter is probably the best indicator we have for nicknames...
                        CLEAN_NAMES_LIST = keep_most_common_name(check_name_DOB,new_name_DOB, CLEAN_NAMES_LIST)
                        return pd.Series(check_name_DOB[0:3])
                else:
                    #non matching lastname
                    if fuzz.ratio(check_fname,clean_fname)>75:
                        #first name is reasonably close
                        CLEAN_NAMES_LIST = keep_most_common_name(check_name_DOB,new_name_DOB, CLEAN_NAMES_LIST)
                        return pd.Series(check_name_DOB[0:3])
    CLEAN_NAMES_LIST.append(new_name_DOB)
    return pd.Series(new_name_DOB[0:3])

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

print("applying rough clean...")
patient_data[['PatientFirstName','PatientLastName','PatientDOB']] = patient_data.apply(rough_clean_name ,axis=1)
print("applying fine clean...")
patient_data[['PatientFirstName','PatientLastName','PatientDOB']] = patient_data.apply(fine_clean_name ,axis=1)

#patient_table["PatientFirstName"] = [clean_name(name)[0] for name in all_names]
#patient_table["PatientLastName"] = [clean_name(name)[1] for name in all_names]

print(patient_table.head())

patient_data.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')
