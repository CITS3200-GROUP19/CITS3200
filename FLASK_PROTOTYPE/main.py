'''
Goal of this prototype is to connect to SQL server,
retrieve StaticPointData of one patient and display their
visual field test data on a flask webpage
'''


# Open/Access SQL DB in Python
# .....
# used for regex
import re

# used for dataframes
import pandas as pd

# Placeholder for accessing server with SQLAlchemy
data = pd.read_csv("projectdata.csv")
# Access StaticPointData field of csv
unmapped = data.iloc[0, 79]
# Split data into pairs
split_data = re.findall('..', unmapped)
# #



# Access necessary StaticPointData
# Import file with functions to access this data
import map_data
# Create Right eye dictionary.
# Key-Val pairs where Key is position and Value is ...value
right_eye_dict = {}
# Left eye dict
left_eye_dict = {}

# Map data depending on what eye it is, 0 = Left, 1 = Right
map_data.map_to_dict("1", split_data, left_eye_dict, right_eye_dict)



# Import function that maps data from dictionary to a comment
# that displays static point data
# currently only maps for right eye
# For testing purposes
import comment_map
# Print out a commented map of the data
comment_map.right_comment_map(right_eye_dict)


# MatplotLib heatmap of data
import heat
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Response, send_file

# 2D List to hold data for processing
w, h = 9, 8;
data_table = [[0 for x in range(w)] for y in range(h)]
# Append data to 2D array
heat.data_table_map(right_eye_dict, data_table)
# Create pandas dataframe from 2D list of data
data_df = pd.DataFrame(data_table, dtype=float)




# Start Flask instance and display heatmap
# Import Flask module
# Render template attaches HTML template from templates directory to this app
from flask import Flask, render_template, request
import base64
import urllib.parse
import matplotlib
matplotlib.use('Agg')

# Tells where app located
app = Flask(__name__)

#Setup route so dont 404
@app.route('/')
def index():
    # instead of returning hello world, return html file from templates
    # Dont need to specify folder name, knows to look for templates directory
    return render_template('index.html')

@app.route('/heatmap')
def fig():
    # Create heatmap
    plt.imshow(data_df, cmap='OrRd', vmin=15, vmax=40, interpolation='none')
    # Create bytes buffer
    img = io.BytesIO()
    # Save plot to img
    plt.savefig(img, format='png')
    img.seek(0)
    # Decode to string before passing image to flask to display
    plot_heatmap = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return render_template('heatmap.html', plot_url=plot_heatmap)

# Run app in debug mode (shows errors)
if __name__ == "__main__":
    app.run(debug=True)

