import dash_core_components as dcc
import dash_html_components as html
from sqlalchemy import create_engine
from app.extensions import db
from app.models import FactTable
import pandas as pd
import os

PW = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
db_connection = create_engine(SQLALCHEMY_DATABASE_URI)
df = pd.read_sql('SELECT Age,AVG(ReliabilityScore),COUNT(ReliabilityScore) FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID Where ReliabilityExists = "Yes" GROUP BY Age ORDER BY Age', con=db_connection)

print(df)

layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(
        id='test',
        figure={
            'data': [
                {'x': df['Age'], 'y': df["AVG(ReliabilityScore)"], 'type': 'bar', 'name': 'Test'},

            ],
            'layout': {
                'title': 'ReliabilityScore vs Age',

            }
        }
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})
