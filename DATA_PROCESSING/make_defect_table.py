import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from fuzzywuzzy import fuzz
import os
import csv
import re
##Altitudinal defect 58
##hemifield defect - not included (not in 1 , 0 format. in 0.00)
##arcuatedefect upper 60
##temporalwedgedefect 62
##paracentraldefect 63
##peripherarimdefect 64
##partialperiopheralrimdefect 65
##BlindSpotDefect 67
##NasalStepDefect 72
##ArcuateDefectLower 82
##CentrealDefect  83
##Altitudinaldefectsuperior 85
## NasalStepDefectSuperior 88
## NasalStepDefectInferior 89
## VerticalStepNasalDefect 90
##VerticalstepTemporaldefect 91
## SupernasalDefect 92
##InferonasalDefect93
##SuperotemporalDefect 94
##InferotemporalDefect 95
##622 combinations of defects from 45000 patients - could possibly be 524288

from get_data import data, SCHEMA_OUTPUT_FILE_PATH

defect_data = data.iloc[:, [0,58,60,62,63,64,65,67,72,82,83,85,88,89,90,91,92,93,94,95]].copy() #data.iloc[:, [0,2,5]].copy()
defect_data.columns = ['TestID','AD', 'ADU', 'TWD','PD','PRD','PPRD','BSD','NSD','ADL','CD','ADS','NSDS','NSDI','VSND','VSTD','SND','IND','STD','ITD']

print(defect_data.head())

def extract(row):
    defectcombo = ''.join(row[['AD', 'ADU', 'TWD','PD','PRD','PPRD','BSD','NSD','ADL','CD','ADS','NSDS','NSDI','VSND','VSTD','SND','IND','STD','ITD']].apply(lambda x: str(x)).tolist())
    defectcount = defectcombo.count('1')
    defectzeros = defectcombo.count('0')
    if defectcount + defectzeros != 19:
        print("Error")
        print("defectcombo")
    return pd.Series([defectcount,defectcombo])



defect_data[['DefectNumberOf','DefectCombination']] = defect_data.apply(extract ,axis=1)


'''IDs to be added to the FACT_TABLE!!!'''
defect_data['DefectID'] = defect_data.groupby(['DefectNumberOf','DefectCombination']).ngroup()
defect_IDs = defect_data['DefectID'].tolist()
print(len(defect_IDs))

defect_data = defect_data.drop(['TestID'], axis=1).drop_duplicates().sort_values(['DefectNumberOf'])


'''create new normalised patient table'''
TABLE_NAME = "DEFECT_TABLE.csv"
#Columns: defectID, defectSide, defectAcuity
defect_table = pd.DataFrame()
defect_table['DefectID'] = defect_data['DefectID']
defect_table['DefectNumberOf'] = defect_data['DefectNumberOf']
defect_table['DefectCombination'] = defect_data['DefectCombination']

defect_table.to_csv(SCHEMA_OUTPUT_FILE_PATH+TABLE_NAME, index=False, encoding='utf8')

print(defect_table)
