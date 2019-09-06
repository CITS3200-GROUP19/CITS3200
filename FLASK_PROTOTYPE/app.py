# VF DATA
import re
import pandas as pd
import collections
# Dash Tutorial
# https://dash.plot.ly/getting-started
import dash
import dash_core_components as dcc
import dash_html_components as html
# Plotly for more sophisticated visualisation
import plotly.graph_objs as go

####################################### VF DATA
vf_data = pd.read_csv("projectdata.csv")
# Function to grab data
visual_acuity_data = []
data_dict = {}


for dt in range(10000):
    #Create hashmap that has years as keys and push each years data to that key
    test_date = vf_data.iloc[dt, 1]
    year = test_date[0:4]
    # Add year to dictionary
    if year not in data_dict:
        data_dict[year] = []

    # Add data to correct year in dictionary
    patient_data = vf_data.iloc[dt, 79]
    split_accuity = re.findall('..', patient_data)
    sum_data = 0
    for data in split_accuity:
        sum_data = sum_data + int(data)
    visual_acuity = round(sum_data / len(split_accuity))
    # Add data to correct year in dictionary
    data_dict[year].append(visual_acuity)

print(data_dict)

all_years = ["1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010"]
for i in all_years:
	print(i)
# Variables to feed to dcc.Graph
x = data_dict.keys()
y = data_dict.values()


####################################### DASH
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# The Dash tutorial page has notes on all of these functions under tutorial

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# Layout of page elements (html, graphs etc)
# Composed of a tree of elements
# dash_html_components has  componenet for every html tag
app.layout = html.Div(children=[
	# Title at top of page
	html.H1(children='Dash Gang'),
	# Sub title
	html.Div(children='''
		Visualize that shit!
		'''),
	# Graph
	dcc.Graph(
		# Graph name
		id='example-graph',
		# Graph details
		figure= {
			'data': [
				# Could do separate line for each set of data from hashmap
                #{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                #{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'scatter', 'name': u'Montréal'},
                go.Scatter(
                	x= all_years,
                	y= list(data_dict.get(i) ),
                	mode='markers',
                	#pacity=0.7,
                	marker={
                	    'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                	},
                	name = i
                	#) for i in data_dict.keys()
                	) for i in all_years
            ],
            'layout': {
            	'title' : 'Visual Acuity Data Visualisation'
            }

		}
	)
])

# Run server
if __name__ == '__main__':
	app.run_server(debug=True)
