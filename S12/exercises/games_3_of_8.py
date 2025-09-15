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
query = '''
            SELECT * FROM data_raw
        '''
games_raw = pd.io.sql.read_sql(query, con=engine)

# tipos de conversión
games_raw['year_of_release'] = pd.to_datetime(games_raw['year_of_release'])
columns = ['na_players', 'eu_players', 'jp_players', 'other_players', 'user_score', 'critic_score']
for column in columns: games_raw[column] = pd.to_numeric(games_raw[column], errors='coerce')

# definir los datos para el informe
games_grouped = (games_raw.groupby(['year_of_release'])
                 .agg({'na_players': 'sum',
                       'eu_players': 'sum',
                       'jp_players': 'sum',
                       'other_players': 'sum'})
                 .reset_index()
                 )

# establecer los estilos dentro del bucle
line_styles = {'na_players': {'color':'red'},
               'eu_players': {'color':'green'},
               'jp_players': {'color':'blue'},              
               'other_players': {'color':'orange'}}

# definir los gráficos que se mostrarán
data_games_by_year = []
for column, style in line_styles.items():
    data_games_by_year += [go.Scatter(x=games_grouped['year_of_release'],
                                      y=games_grouped[column],
                                      mode='lines',
                                      line=style,
                                      stackgroup = 'one',
                                      name=column)]

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # crear un encabezado con una etiqueta HTML
    html.H1(children='Juegos vendidos por año'),

    dcc.Graph(
        figure={'data': data_games_by_year,
                'layout': go.Layout(xaxis={'title': 'Year'},
                                    yaxis={'title': 'Sales'})
                },
        id='sales_by_year'
    ),

])

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)