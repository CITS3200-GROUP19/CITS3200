from datetime import datetime as dt
import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
import os
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from sqlalchemy import text
from app.models import FactTable, ReliabilityTable, EyeTable, DefectTable


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
        # sql_string = text('SELECT * FROM FactTable JOIN ReliabilityTable ON FactTable.ReliabilityID = ReliabilityTable.ReliabilityID JOIN EyeTable ON FactTable.EyeID = EyeTable.EyeID JOIN DefectTable ON DefectTable.DefectID = FactTable.DefectID')
        query = db.session.query(FactTable).join(ReliabilityTable).join(EyeTable).join(DefectTable)
        df = pd.read_sql(query.statement, con=db.engine)
        #print(df[varX])
        traces = []
        for x_value in eval("df."+varX+".unique()"):
            #print(x_value)
            traces.append(go.Box(y=df[df[varX] == x_value][varY],name=str(x_value),marker={"size": 4}))
        return {"data": traces,
                "layout": go.Layout(title="Aggregated Data",autosize=True,
                                    margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,"title": varX},
                                    yaxis={"title": varY})}
