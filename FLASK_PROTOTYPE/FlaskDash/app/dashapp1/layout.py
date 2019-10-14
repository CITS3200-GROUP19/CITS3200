import dash_core_components as dcc
import dash_html_components as html
from app.models import FactTable
import pandas as pd
import os

PW = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
db_connection = create_engine(SQLALCHEMY_DATABASE_URI)

layout = html.Div([
    html.H1('Averages on Age'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Runtime', 'value': 'Runtime'},
            {'label': 'Mean Deviation', 'value': 'Mean_Deviation'},
            {'label': 'Pattern Deviation', 'value': 'Pattern_Deviation'},
            {'label': 'Age', 'value': 'Age'},
            {'label': 'Eye Acuity', 'value': 'EyeAcuity'},
            {'label': 'Reliability Score', 'value': 'ReliabilityScore'}
        ],
        value='Age'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})
