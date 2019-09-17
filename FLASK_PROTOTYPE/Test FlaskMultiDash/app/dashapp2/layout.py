import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import re


vf_data = pd.read_csv("projectdata.csv")

visual_acuity_data = []
data_dict = {}

df = vf_data[0:20]
pat_data = vf_data.iloc[4, 79]
split_data = re.findall('..', str(pat_data))
# Layout of page elements (html, graphs etc)
# Composed of a tree of elements
# dash_html_components has  componenet for every html tag
layout = html.Div(children=[
    # Title at top of page
    html.H1(children='Eye Heatmap'),
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