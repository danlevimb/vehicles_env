#!/usr/bin/python
# -*- codificación: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import pandas as pd

# definir los datos a mostrar
from sqlalchemy import create_engine

# código de muestra para conectarse a la base de datos con SQLite
engine = create_engine('sqlite:////db/games.db', echo=False)

# obtención de datos en bruto
query = 'SELECT * FROM data_raw'
games_raw = pd.io.sql.read_sql(query, con=engine)

games_grouped = (games_raw.groupby('platform')
                 .agg({'name': 'nunique'})
                 .reset_index()
                 .rename(columns={'name': 'games_launched'})
                 .sort_values(by='games_launched', ascending=False)
    .head(10))

# definir los gráficos que se mostrarán
data = [go.Pie(labels = games_grouped['platform'],
values = games_grouped['games_launched'],
name = 'pie')]

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # crear un encabezado con una etiqueta HTML
    html.H1(children='Juegos lanzados por plataforma (top-10)'),

    dcc.Graph(
        figure={'data': data,
                'layout': go.Layout()
                },
        id='platform_pie'
    ),

])

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)