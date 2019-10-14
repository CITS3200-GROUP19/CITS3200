from datetime import datetime as dt
import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
import os
import pandas as pd


# from sqlalchemy import create_engine
# PW = os.environ.get('DB_PASSWORD')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
# db_connection = create_engine(SQLALCHEMY_DATABASE_URI)

# Use df = pd.read_sql(query.statement, query.session.bind)
# or df = pd.read_sql_query(query.statement, engine)
def register_callbacks(dashapp):
    from app.extensions import db

    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        var = selected_dropdown_value
        print(var)
        sql_string = 'SELECT Age,AVG('+var+'),COUNT('+var+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID WHERE '+var+' > 0 AND Age < 110 GROUP BY Age ORDER BY Age'
        df = pd.read_sql(sql_string, con=db.engine)
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
