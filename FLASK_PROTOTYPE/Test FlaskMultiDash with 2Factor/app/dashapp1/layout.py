import dash_core_components as dcc
import dash_html_components as html
from app.models import FactTable
import pandas as pd
import os

# from sqlalchemy import create_engine

# PW = os.environ.get('DB_PASSWORD')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
# db_connection = create_engine(SQLALCHEMY_DATABASE_URI)
# df = pd.read_sql('SELECT Age,AVG(ReliabilityScore),COUNT(ReliabilityScore) FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID Where ReliabilityExists = "Yes" GROUP BY Age ORDER BY Age', con=db.engine)

# print(df)

layout = html.Div([
    html.H1('Averages on Age'),
    dcc.Dropdown(
        id='my-dropdown-X',
        options=[
            {'label': 'Runtime', 'value': 'Runtime'},
            {'label': 'Mean Deviation', 'value': 'Mean_Deviation'},
            {'label': 'Pattern Deviation', 'value': 'Pattern_Deviation'},
            {'label': 'Age', 'value': 'Age'},
            {'label': 'Eye Acuity', 'value': 'EyeAcuity'},
            {'label': 'Reliability Score', 'value': 'ReliabilityScore'},
            {'label': 'Number of Defects', 'value': 'DefectNumberOf'}

        ],
        value='Age'
    ),
    dcc.Dropdown(
        id='my-dropdown-Y',
        options=[
            {'label': 'Runtime', 'value': 'Runtime'},
            {'label': 'Mean Deviation', 'value': 'Mean_Deviation'},
            {'label': 'Pattern Deviation', 'value': 'Pattern_Deviation'},
            {'label': 'Age', 'value': 'Age'},
            {'label': 'Eye Acuity', 'value': 'EyeAcuity'},
            {'label': 'Reliability Score', 'value': 'ReliabilityScore'},
            {'label': 'Number of Defects', 'value': 'DefectNumberOf'}
        ],
        value='Age'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})
