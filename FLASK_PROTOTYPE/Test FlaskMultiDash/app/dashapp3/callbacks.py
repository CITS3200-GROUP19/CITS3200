# VF DATA
import re
import pandas as pd
import collections
# DASH MODULES
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
# PLOTLY
import plotly.graph_objs as go
import plotly.tools as tls
# VF DATA PROCESSING
from collections import defaultdict


# VF DATA PREPARATION
vf_data = pd.read_csv("processed_data.csv")

visual_acuity_data = []
data_dict = {}

# DASH
# Dash CSS Stylesheet 
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# # 
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# SPRINT 2.1 TABLE DELIVERABLE, TEST VIEW
# For testing purposes make data only first 20 lines
# Callback function below app.layout
df = vf_data[0:20]
pat_data = vf_data.iloc[4, 79]
split_data = re.findall('..', str(pat_data))
print("Split Data:", split_data)




# Returns raw data for given id
def returnData(id):
    data = vf_data.iloc[id, 79]
    print(data)
    return data


def data_table_map(data_pairs, data_table):
    # Top Row
    i = 3
    for x in range(6, 10):
        if x in data_pairs:
            data_table[0][i] = data_pairs[x]
        i = i + 1
    i = 2
    # 2nd Row
    for x in range(12, 18):
        if x in data_pairs:
            data_table[1][i] = data_pairs[x]
        i = i + 1
    i = 1
    # 3rd Row
    for x in range(20, 28):
        if x in data_pairs:
            data_table[2][i] = data_pairs[x]
        i = i + 1
    i = 0
    # 4th Row
    for x in range(29, 39):
        if x in data_pairs:
            data_table[3][i] = data_pairs[x]
        i = i + 1
    i = 0
    # 5th Row
    for x in range(39, 49):
        if x in data_pairs:
            data_table[4][i] = data_pairs[x]
        i = i + 1
    i = 1
    # 6th Row
    for x in range(50, 58):
        if x in data_pairs:
            data_table[5][i] = data_pairs[x]
        i = i + 1
    i = 2
    # 7th Row
    for x in range(60, 66):
        if x in data_pairs:
            data_table[6][i] = data_pairs[x]
        i = i + 1
    i = 3
    # 8th Row
    for x in range(68, 72):
        if x in data_pairs:
            data_table[7][i] = data_pairs[x]
        i = i + 1
    i = 0


# Data positions
# Right eye positions
right_eye_data_map = [22, 6, 7, 12, 13, 14, 20, 21, 23, 29, 30, 31, 32, 33, 25, 8, 9, 15, 16, 17, 24, 26, 27, 34, 35, 36, 37, 55, 44, 45, 46, 47, 54, 56, 57, 63, 64, 65, 70, 71, 52, 39, 40, 41, 42, 43, 50, 51, 53, 60, 61, 62, 68, 69]
# Left eye positions
left_eye_data_map = [25, 9, 8, 17, 16, 15, 27, 26, 24, 38, 37, 36, 35, 34, 22, 7, 6, 14, 13, 12, 23, 22, 20, 33, 32, 31, 30, 52, 43, 42, 41, 40, 53, 51, 50, 62, 61, 60, 69, 68, 55, 48, 47, 46, 45, 44, 57, 56, 54, 65, 64, 63, 70, 71]


# Function that takes which eye it is and the static point data
# and populates a dictionary with this data as the values and the positions
# as keys
# eye argument = data.iloc[0, ?], 0 for left and 1 for right eye
# data argument = split_data, this is the staticpointdata that has been processed
def map_to_dict(eye, data, left_eye_dict, right_eye_dict):
    i = 0
    # If left eye
    if eye == '0':
        for key in left_eye_data_map:
            left_eye_dict[key] = data[i]
            i = i + 1
        print(left_eye_dict)
    # If right eye
    elif eye == '1':
        for key in right_eye_data_map:
            right_eye_dict[key] = data[i]
            i = i + 1
        print("yeet", right_eye_dict)

##########################################
# Patient Based Search
def allPatients():
    # Array to hold all patient names
    # defaultdict() because append was not functioning with str values
    patients = defaultdict(list)

    for i in range(len(df)):
        # If patient not already in array
        if df.iloc[i, 2] not in patients.keys():
            # Add to patients array and add value (data)
            patients[df.iloc[i, 2]].append(df.iloc[i, 79])
        # If patient is already in patients dictionary
        elif df.iloc[i, 2] in patients.keys():
            # Append data as value for that patients key
            patients[df.iloc[i, 2]].append(df.iloc[i, 79])
    # Print array
    print("Patient Tests:", patients)
    # Convert to DataFrame for DataTable
    return patients

# Convert patient keys into dataframe with column patient names
patients_dict = allPatients()
patients_df = pd.DataFrame(patients_dict.keys(), columns=['Patient Name'])
##########################################

##########################################
# GET DATES
def testDates(patientName):
    dates = []
    for patients in range(len(df)):
        if patientName == df.iloc[patients, 2]:
            dates.append(df.iloc[patients, 1])
    return dates
###########################################



# name : patients name
# data : list of test results
# dates : list of dates tests were conducted
class Patient:
    def __init__(self, name, data, dates=[]):
        self.name = name
        self.data = data
        self.dates = dates



def register_callbacks(dashapp):
    # SLIDER CALLBACK
    # output title so displayed number doesnt change so it can be changed with another callback function
    @dashapp.callback(
        Output('slider-output-container', 'children'),
        [Input('my-slider', 'value'),
         Input('All Data', 'selected_rows')])
    def update_output(value, selected_rows):
        return format(value)

    # Callback function to display test results from selected row
    @dashapp.callback(
        # Outputs id of selected row
        Output('graphs', "children"),
        #Output('slider-output-container', 'children'),

        # Output(component_id='cur_plot', component_property='src'),
        [Input('All Data', "selected_rows"),
         Input('slider-output-container', 'children')
         ])

    # Returns row id of selected row
    # Can now display data from this row index
    def update(selected_row_ids, kids):
        if len(selected_row_ids) == 0:
            raise PreventUpdate
        else:
            pat_id = selected_row_ids[0]

            ###################### TEST VIEW
            # # Patients Name
            # pat_name = df.iloc[pat_id, 2]
            # print("Patient Name: ", pat_name)
            # # Patients Data
            # pat_data = df.iloc[pat_id, 79]
            # print("Patient Data: ", pat_data)
            #########################################

            ##################### PATIENT VIEW
            # Patients Name
            pat_name = patients_df.iloc[pat_id, 0]
            print("Patient Name: ", pat_name)
            # Access all of selected_row_ids data from patients dictionary
            patient_tests = patients_dict.get(pat_name)

            #### CLASS IMP
            # Creating instance of class Patient
            patient = Patient(pat_name, patient_tests, testDates(pat_name))
            # Data and dates should be in correct order

            # Patients Heatmap
            # Process data
            pat_data = '{:f}'.format(patient.data)  ## Convert numpy64float to float
            split_data = re.findall('..', pat_data[int(kids)])
            # Data Dict
            right_eye_dict = {}
            left_eye_dict = {}
            map_data.map_to_dict("1", split_data, left_eye_dict, right_eye_dict)

            # Append data to dataframe
            w, h = 9, 8
            data_table = [[0 for x in range(w)] for y in range(h)]
            # Append data to 2D array
            heat.data_table_map(right_eye_dict, data_table)
            # Create pandas dataframe from 2D list of data
            data_df = pd.DataFrame(data_table, dtype=float)
            # Convert dataframe to dictionary for plotly heatmap
            data_dict = data_df.to_dict('split')
            # Actual data values from dataframe
            vf_values = data_dict.get('data')

            # Heatmap
            fig = go.Figure(data=go.Heatmap(z=vf_values))

            # Return Heatmap as src output
            return [
                dcc.Graph(
                # Graph name
                    id='example-graph',
                    # Graph details
                    figure=fig,
                    ),
            ],
            patient.dates[int(kids)]

