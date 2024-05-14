import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div(
        dbc.Container(
        [
            html.H1("Welcome to the dashboard!", className="text-light")
            ]
        )
)