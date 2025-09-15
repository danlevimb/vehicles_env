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
games_raw['total'] = games_raw[['na_players', 'eu_players', 'jp_players', 'other_players']].sum(axis=1)

# definir los gráficos que se mostrarán
data = []
for genre in games_raw.genre.unique():
    current = games_raw.query('genre == @genre')
    data += [go.Box(y=current['total'], name=genre)]

    # definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # crear un encabezado con una etiqueta HTML
    html.H1(children='Juegos vendidos por género'),

    dcc.Graph(
        figure={'data': data,
                'layout': go.Layout(xaxis={'title': 'Genre'},
                                    yaxis={'title': 'Sales'})
                },
        id='games_by_genre'
    ),

])

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)