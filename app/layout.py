from dash import dcc, html
import dash_bootstrap_components as dbc

tabs = dcc.Tabs([
    dcc.Tab(label="Overview", children=[
        html.Div(id="overview-content")
    ]),
    dcc.Tab(label="Price Trends", children=[
        html.Div(id="price-trends-content")
    ]),
    dcc.Tab(label="Town Analysis", children=[
        html.Div(id="town-analysis-content")
    ]),
    dcc.Tab(label="Map Explorer", children=[
        html.Div(id="map-explorer-content")
    ]),
    dcc.Tab(label="Flat Type Breakdown", children=[
        html.Div(id="flat-type-breakdown-content")
    ])
])

layout = dbc.Container([
    html.H1("Singapore HDB Resale Analytics", className="my-4"),
    tabs
], fluid=True)
