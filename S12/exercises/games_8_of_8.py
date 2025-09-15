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

# tipos de conversión
games_raw['year_of_release'] = pd.to_datetime(games_raw['year_of_release'])

columns = ['na_players', 'eu_players', 'jp_players', 'other_players']

for column in columns: games_raw[column] = pd.to_numeric(games_raw[column], errors='coerce')
games_raw['total'] = games_raw[['na_players',
                                'eu_players',
                                'jp_players',
                                'other_players']].sum(axis=1).round(2)

# definir los gráficos que se mostrarán
games_raw = games_raw[['name', 'platform', 'genre', 'total']].sort_values(by='total', ascending=False).head(10)

data = [go.Table(header = {'values': ['<b>Game</b>', '<b>Platform</b>', '<b>Genre</b>', '<b>Sales by region</b>'],
                         'fill_color': 'lightgrey',
                         'align': 'center'},
                 cells={'values': games_raw.T.values})]

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # crear un encabezado con una etiqueta HTML
    html.H1(children='Top-10 games by sales'),

    dcc.Graph(
        figure={'data': data,
                'layout': go.Layout()
                },
        id='games_by_genre'
    ),

])

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)