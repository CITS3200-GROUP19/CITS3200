from datetime import datetime as dt
import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
import os
import pandas as pd
import plotly.graph_objs as go
import numpy as np

def label(varX,x_value):
    if varX == "Runtime":
        return str(int(str(x_value)[0:2])) +" to "+ str(int(str(x_value)[0:2])+1)+" Minutes"
    elif varX == "Mean_Deviation":
        return "Between "+ str(10*int(x_value)) + " to " + str(10*int(x_value)+10)
    elif varX == "Pattern_Deviation":
        return "Between "+ str(5*int(x_value)) + " to " + str(5*int(x_value)+5)
    elif varX == "Age":
        return "Between "+ str(10*int(x_value)) + " to " + str(10*int(x_value)+10)
    else:
        return str(x_value)


# from sqlalchemy import create_engine
# PW = os.environ.get('DB_PASSWORD')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
# db_connection = create_engine(SQLALCHEMY_DATABASE_URI)

# Use df = pd.read_sql(query.statement, query.session.bind)
# or df = pd.read_sql_query(query.statement, engine)
def register_callbacks(dashapp):
    from app.extensions import db

    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown-Y', 'value'),Input('my-dropdown-X', 'value')])
    def update_graph(varY,varX):
        print(varX,varY)
        sql_string = 'SELECT * FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID'
        df = pd.read_sql(sql_string, con=db.engine)
        #BINNING
        if (varX == "Age" or varX == "Mean_Deviation"):
            df[varX] = df[varX]//10
        elif varX == "Pattern_Deviation":
            df[varX] = df[varX]//5
        elif varX == "Runtime":
            df[varX] = df[varX]//(60*10**9)
        #print(df[varX])
        df = df.sort_values(by=[varX])
        traces = []
        for x_value in eval("df."+varX+".unique()"):
            #LABLES
            labels = label(varX,x_value)

            traces.append(go.Box(y=df[df[varX] == x_value][varY],name=labels,marker={"size": 4}))
        return {"data": traces,
                "layout": go.Layout(title="Aggregated Data",autosize=True,
                                    margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,"title": varX},
                                    yaxis={"title": varY})}

    @dashapp.callback(Output('bar-chart', 'figure'), [Input('my-dropdown-Y', 'value'),Input('my-dropdown-X', 'value')])
    def update_graph(varY,varX):
        print(varX,varY)

        if (varX == "Age" or varX == "Mean_Deviation"):
            sql_string = 'SELECT FLOOR('+varX+'/10) AS '+varX+', COUNT('+varX+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID GROUP BY FLOOR('+varX+'/10)'
        elif (varX == "Pattern_Deviation"):
            sql_string = 'SELECT FLOOR('+varX+'/5) AS '+varX+', COUNT('+varX+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID GROUP BY FLOOR('+varX+'/5)'
        elif (varX == "Runtime"):
            sql_string = 'SELECT MINUTE('+varX+') AS '+varX+', COUNT('+varX+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID GROUP BY MINUTE('+varX+')'
        else:
            sql_string = 'SELECT '+varX+', COUNT('+varX+') FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID GROUP BY '+varX

        df = pd.read_sql(sql_string, con=db.engine)
        df['labels'] = df[varX].apply(lambda x: label(varX,x))
        print(df)
        print(df.groupby(varX).size())
        return {"data": [
                    {"type": "bar",
                    'x': df['labels'],
                    'y': df['COUNT('+varX+")"]}
        ],
                "layout": {
                    'title': 'Counts of '+varX
                }
        }
