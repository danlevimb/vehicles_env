#!/usr/bin/python
# -*- codificación: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from datetime import datetime

import pandas as pd

# definir los datos a mostrar
from sqlalchemy import create_engine

# código de muestra para conectarse a la base de datos con PostgreSQL
# db_config = {'user': 'my_user',
#             'pwd': 'my_user_password',
#             'host': 'localhost',
#             'port': 5432,
#             'db': 'games'}
# engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
#                                                            db_config['pwd'],
#                                                            db_config['host'],
#                                                            db_config['port'],
#                                                            db_config['db']))
# código de muestra para conectarse a la base de datos con SQLite
engine = create_engine('sqlite:////db/games.db', echo=False)

# obtención de datos en bruto
query = 'SELECT * FROM data_raw'
games_raw = pd.io.sql.read_sql(query, con=engine)

# tipos de conversión
games_raw['year_of_release'] = pd.to_datetime(games_raw['year_of_release'])
columns = ['na_players', 'eu_players', 'jp_players', 'other_players']
for column in columns:
    games_raw[column] = pd.to_numeric(games_raw[column], errors='coerce')

# definir los datos para el informe
games_grouped = (
    games_raw.groupby(['year_of_release', 'genre'])
    .agg({'name': 'nunique'})
    .reset_index()
    .rename(columns={'name': 'games_launched'})
)

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, compress=False
)
app.layout = html.Div(
    children=[
        # crear un encabezado con una etiqueta HTML
        html.H1(children='Juegos lanzados por año'),
        # seleccionar el intervalo de tiempo
        html.Label('Time range:'),
        dcc.DatePickerRange(
            start_date=games_grouped['year_of_release'].dt.date.min(),
            end_date=datetime(2016, 1, 1).strftime('%Y-%m-%d'),
            initial_visible_month=datetime(2016, 1, 1).strftime(
                '%Y-%m-%d'
            ),  # definir el mes del calendario que se muestra por primera vez
            display_format='YYYY-MM-DD',
            id='dt_selector',
        ),
        # seleccionar un modo de visualización: valores absolutos/relativos
        html.Label('Display mode:'),
        dcc.RadioItems(
            options=[
                {'label': 'Absolute values', 'value': 'absolute_values'},
                {
                    'label': '% from the total number of games released',
                    'value': 'relative_values',
                },
            ],
            value='absolute_values',
            id='mode_selector',
        ),
        # seleccionar género
        html.Label('Genres:'),
        dcc.Checklist(
            options=[
                {'label': x, 'value': x}
                for x in games_grouped['genre'].unique()
            ],
            value=games_grouped['genre'].unique().tolist(),
            id='genre_selector',
        ),
        # gráfico de juegos lanzados por año
        dcc.Graph(id='launches_by_year'),
    ]
)

# lógica del dashboard
@app.callback(
    [
        Output('launches_by_year', 'figure'),
    ],
    [
        Input('dt_selector', 'start_date'),
        Input('dt_selector', 'end_date'),
        Input('mode_selector', 'value'),
        Input('genre_selector', 'value'),
    ],
)
def update_figures(start_date, end_date, mode, selected_genres):

    # converting input parameters to the required types
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # applying filters
    filtered_data = games_grouped.query(
        'year_of_release >= @start_date and year_of_release <= @end_date'
    )
    filtered_data = filtered_data.query('genre in @selected_genres')

    # convertir parámetros de entrada a los tipos requeridos
    if mode == 'relative_values':
        total_by_year = (
            filtered_data.groupby('year_of_release')
            .agg({'games_launched': 'sum'})
            .rename(columns={'games_launched': 'total'})
        )
        filtered_data = (
            filtered_data.set_index('year_of_release')
            .join(total_by_year)
            .reset_index()
        )
        filtered_data['games_launched'] = (
            filtered_data['games_launched'] / filtered_data['total']
        )
    # crear los gráficos que se mostrarán
    data = []
    for genre in filtered_data['genre'].unique():
        data += [
            go.Scatter(
                x=filtered_data.query('genre == @genre')['year_of_release'],
                y=filtered_data.query('genre == @genre')['games_launched'],
                mode='lines',
                stackgroup='one',
                name=genre,
            )
        ]
    # formar el resultado a mostrar
    return (
        {
            'data': data,
            'layout': go.Layout(
                xaxis={'title': 'Date and time'},
                yaxis={'title': 'Games released'},
            ),
        },
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)