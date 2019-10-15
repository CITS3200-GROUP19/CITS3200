




layout = html.Div(children=[
    # Title at top of page
    html.H1(children='Dash Gang'),
    # Sub title
    html.Div(children='''
        Table View
        '''),
    # DataTable
    dash_table.DataTable(
        id='All Data',
        # columns=[{"name": i, "id": i} for i in patients_df.columns],
        columns=[{"name": i, "id": i} for i in patients_df.columns],
        data=patients_df.to_dict('records'),
        # data=patients_df.to_dict('records'),
        # data=df.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
    ),
    # Div for Heatmap below the table
    html.Div(
    children=[
        html.H1(id='hola', children='TEST RESULTS'),
        html.Div(id='graphs', children=dcc.Graph(id='dummy'))
        ]
    ),
    # Slider from https://dash.plot.ly/dash-core-components/slider
    dcc.Slider(
        id='my-slider',
        # arbitrary numbers
        min=0,
        max=10,
        step=1,
        value=10,
    ),
    html.Div(id='slider-output-container')

    ####
    # slider should be number of tests because dates will be too weird (eg size of patient.data)
]