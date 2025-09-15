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

# definir los datos para el informe
games_grouped = (games_raw.groupby(['genre'])
                 .agg({'name': 'nunique'})
                 .rename(columns={'name': 'games_launched'})
                 .reset_index()
                 )

games_grouped = games_grouped.sort_values(by='games_launched', ascending=False)

# formar etiquetas
#games_grouped['label'] = games_grouped.apply(lambda x: '{} games'.format(...), axis=1)

games_grouped['label'] = games_grouped.apply(lambda x: f"{int(x['games_launched'])} games", axis=1)

# definir los gráficos que se mostrarán
data = [go.Bar(x = games_grouped['genre'],
y = games_grouped['games_launched'],
text = games_grouped['label'],
textposition = 'auto',
name = 'games_launched')]

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # crear un encabezado con una etiqueta HTML
   html.H1(children='Juegos lanzados por género'),

    dcc.Graph(
        figure={'data': data,
                'layout': go.Layout(xaxis={'title': 'Genre'},
                                    yaxis={'title': 'Games #released'})
                },
        id='launches_by_genre'
    ),
])

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)