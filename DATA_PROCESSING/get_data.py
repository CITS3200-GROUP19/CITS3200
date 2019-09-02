#Created 27th August 2019 Alex Rohl
import csv
import glob, os, os.path
import numpy as np
import pandas as pd
import datetime
import time
import shutil
from pathlib import Path

#ensure the data is labelled "projectdata.csv" and sits adjacent to the GitHub Repo
BIG_DATA_FILE_PATH = "../../projectdata.csv"

SCHEMA_OUTPUT_FILE_PATH = "../../CITS3200_schemas/"

#reset schema folder
shutil.rmtree(SCHEMA_OUTPUT_FILE_PATH)
os.makedirs(SCHEMA_OUTPUT_FILE_PATH)

#read in BIG_DATA_FILE_PATH
data = pd.read_csv(BIG_DATA_FILE_PATH, low_memory=False,header=None) #names = ['Id','DateOfTest','PatientName','EyeTested','PatientId','BirthDate','NameOfTest','TimeOfTest','TypeOfTest','DataStatus','ElapsedTime','PupilDiameter','CentralDefectivePoints','WidespreadLoss','NasalStepDefectSuperior','NasalStepDefectInferior','VerticalStepNasalDefect','VerticalStepTemporalDefect','SuperonasalDefect','InferonasalDefect','SuperotemporalDefect','InferotemporalDefect'])
print("BIG_DATA_FILE has {0} columns and {1} rows".format(len(data.columns),len(data.index)))
