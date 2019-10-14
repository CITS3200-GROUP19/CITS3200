from datetime import datetime as dt
from sqlalchemy import create_engine
import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
import os
import pandas as pd

PW = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
db_connection = create_engine(SQLALCHEMY_DATABASE_URI)


def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        var = selected_dropdown_value
        print(var)
        sql_string = 'SELECT Age,AVG('+var+'),COUNT('+var+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID WHERE Age < 110 GROUP BY Age ORDER BY Age'
        df = pd.read_sql(sql_string, con=db_connection)
        return {
            'data': [{
                'x': df['Age'],
                'y': df['AVG('+var+')'],
                'type': 'bar'
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30},
                        'xaxis' : {'title': 'Age'}
                        }
        }
