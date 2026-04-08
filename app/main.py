import dash
import dash_bootstrap_components as dbc
from dash import html
from app.layout import layout
from app.callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "HDB Resale Analytics"
app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
