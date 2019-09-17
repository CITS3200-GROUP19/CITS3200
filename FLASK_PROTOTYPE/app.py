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
import map_data
import heat



# VF DATA PREPARATION
vf_data = pd.read_csv("projectdata.csv")

visual_acuity_data = []
data_dict = {}

# DASH
# Dash CSS Stylesheet 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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


# Layout of page elements (html, graphs etc)
# Composed of a tree of elements
# dash_html_components has  componenet for every html tag
app.layout = html.Div(children=[
    # Title at top of page
    html.H1(children='Dash Gang'),
    # Sub title
    html.Div(children='''
        Table View
        '''),
    # DataTable
    dash_table.DataTable(
        id='All Data',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
    ),
    # Div for Heatmap below the table
    html.Div(
    children=[
        html.H1(id='hola', children='TEST RESULTS'),
        html.Div(id='graphs', children=dcc.Graph(id='dummy'))
    	]
	)
])


# Callback function to display test results from selected row
@app.callback(
    # Outputs id of selected row
    Output('graphs', "children"),
    # Output(component_id='cur_plot', component_property='src'),
    [Input('All Data', "selected_rows"),
     ])
# Returns row id of selected row
# Can now display data from this row index
def update(selected_row_ids):
    if len(selected_row_ids) == 0:
        raise PreventUpdate
    else:
        pat_id = selected_row_ids[0]
        # Patients Name
        pat_name = df.iloc[pat_id, 2]
        print("Patient Name: ", pat_name)
        # Patients Data
        pat_data = df.iloc[pat_id, 79]
        print("Patient Data: ", pat_data)

        # Patients Heatmap
        split_data = re.findall('..', pat_data)
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
        ]
        

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)




