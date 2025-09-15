#!/usr/bin/python
# -*- coding: utf-8 -*-

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
query = 'SELECT * FROM agg_games_year_genre_platform'
agg_games_year_genre_platform = pd.io.sql.read_sql(query, con=engine)
agg_games_year_genre_platform['year_of_release'] = pd.to_datetime(
    agg_games_year_genre_platform['year_of_release']
)

query = 'SELECT * FROM agg_games_year_score'
agg_games_year_score = pd.io.sql.read_sql(query, con=engine)
agg_games_year_score['year_of_release'] = pd.to_datetime(
    agg_games_year_score['year_of_release']
)
# ignorar registros sin valores
agg_games_year_score = agg_games_year_score.query(
    'avg_user_score > 0 and avg_critic_score > 0'
)

note = '''
          Este dashboard muestra el historial del mercado de juegos (excluyendo los de dispositivos móviles).
				  Usa selectores de rango de tiempo, género y plataformas para filtrar el dashboard.
				  Use el selector de modo de visualización para cambiar entre absoluto y valores relativos.
       '''

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, compress=False
)
app.layout = html.Div(
    children=[
        # formar un encabezado con una etiqueta HTML
        html.H1(children='Historial del mercado de juegos'),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        # gráficos de juegos lanzados por año y género
                        html.Label('Juegos lanzados por género:'),
                        dcc.RadioItems(
                            options=[
                                {
                                    'label': 'Absolute values',
                                    'value': 'absolute_values',
                                },
                                {
                                    'label': '% of the total number of games released',
                                    'value': 'relative_values',
                                },
                            ],
                            value='absolute_values',
                            id='mode_selector',
                        ),
                        dcc.Graph(id='launches_by_year'),
                    ],
                    className='eight columns',
                ),
                html.Div(
                    [
                        # gráfico de juegos lanzados por plataforma
                        html.Label('Juegos lanzados por plataforma:'),
                        dcc.Graph(id='launches_by_platform'),
                    ],
                    className='four columns',
                ),
            ],
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        # gráficos de juegos vendidos por año y género
                        html.Label('Juegos vendidos por género:'),
                        dcc.Graph(id='sales_by_year'),
                    ],
                    className='eight columns',
                ),
                html.Div(
                    [
                        # puntuaciones medias por gráfico de género
                        html.Label('Valores promedio por género:'),
                        dcc.Graph(id='score_scatter'),
                    ],
                    className='four columns',
                ),
            ],
            className='row',
        ),
        # descripción
        html.Label(note),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        # seleccionar rango de tiempo
                        html.Label('Año de lanzamiento:'),
                        dcc.DatePickerRange(
                            start_date=agg_games_year_genre_platform[
                                'year_of_release'
                            ].dt.date.min(),
                            end_date=datetime(2016, 1, 1).strftime('%Y-%m-%d'),
                            initial_visible_month=datetime(
                                2016, 1, 1
                            ).strftime(
                                '%Y-%m-%d'
                            ),  # definir el mes del calendario que se muestra por primera vez
                            display_format='YYYY-MM-DD',
                            id='dt_selector',
                        ),
                    ],
                    className='two columns',
                ),
                html.Div(
                    [
                        # seleccionar género
                        html.Label('Género:'),
                        dcc.Dropdown(
                            options=[
                                {'label': x, 'value': x}
                                for x in agg_games_year_genre_platform[
                                    'genre'
                                ].unique()
                            ],
                            value=agg_games_year_genre_platform['genre']
                            .unique()
                            .tolist(),
                            multi=True,
                            id='genre_selector',
                        ),
                    ],
                    className='four columns',
                ),
                html.Div(
                    [
                        # selecting platform
                        html.Label('Platforms:'),
                        dcc.Dropdown(
                            options=[
                                {'label': x, 'value': x}
                                for x in agg_games_year_genre_platform[
                                    'platform'
                                ].unique()
                            ],
                            value=agg_games_year_genre_platform['platform']
                            .unique()
                            .tolist(),
                            multi=True,
                            id='platform_selector',
                        ),
                    ],
                    className='six columns',
                ),
            ],
            className='row',
        ),
    ]
)

# lógica del dashboard
@app.callback(
    [
        Output('launches_by_year', 'figure'),
        Output('sales_by_year', 'figure'),
        Output('launches_by_platform', 'figure'),
        Output('score_scatter', 'figure'),
    ],
    [
        Input('dt_selector', 'start_date'),
        Input('dt_selector', 'end_date'),
        Input('mode_selector', 'value'),
        Input('genre_selector', 'value'),
        Input('platform_selector', 'value'),
    ],
)
def update_figures(
    start_date, end_date, mode, selected_genres, selected_platforms
):

    # aplicar filtros
    filtered = agg_games_year_genre_platform.query(
        'year_of_release >= @start_date and year_of_release <= @end_date'
    )
    filtered = filtered.query('genre in @selected_genres')
    filtered = filtered.query('platform in @selected_platforms')

    filtered_score = agg_games_year_score.query(
        'year_of_release >= @start_date and year_of_release <= @end_date'
    )
    filtered_score = filtered_score.query('genre in @selected_genres')
    filtered_score = filtered_score.query('platform in @selected_platforms')

    games_by_genre = (
        filtered.groupby(['year_of_release', 'genre'])
        .agg({'games': 'sum', 'total_copies_sold': 'sum'})
        .reset_index()
    )

    games_by_platform = (
        filtered.groupby(['platform']).agg({'games': 'sum'}).reset_index()
    )
    # colocar todas las plataformas con una pequeña cantidad de juegos en una categoría
    games_by_platform['percent'] = (
        games_by_platform['games'] / games_by_platform['games'].sum()
    )
    games_by_platform.loc[
        games_by_platform['percent'] < 0.05, 'platform'
    ] = 'Other'
    # agrupar los datos una vez más
    games_by_platform = (
        games_by_platform.groupby(['platform'])
        .agg({'games': 'sum'})
        .reset_index()
    )

  # transformar según el modo seleccionado
    y_label = 'Juegos lanzados'
    y_label_sales = 'Juegos vendidos , millones de copias'
    if mode == 'relative_values':
        y_label = '% de juegos lanzados'
        y_label_sales = '% de juegos vendidos'
        total = (
            games_by_genre.groupby('year_of_release')
            .agg({'games': 'sum', 'total_copies_sold': 'sum'})
            .rename(
                columns={
                    'games': 'total_launches',
                    'total_copies_sold': 'total_sales',
                }
            )
        )
        games_by_genre = (
            games_by_genre.set_index('year_of_release')
            .join(total)
            .reset_index()
        )
        games_by_genre['games'] = (
            games_by_genre['games'] / games_by_genre['total_launches']
        )
        games_by_genre['total_copies_sold'] = (
            games_by_genre['total_copies_sold'] / games_by_genre['total_sales']
        )
    # gráficos de juegos lanzados y juegos vendidos por género
    data_by_genre = []
    sales_by_genre = []
    for genre in games_by_genre['genre'].unique():
        data_by_genre += [
            go.Scatter(
                x=games_by_genre.query('genre == @genre')['year_of_release'],
                y=games_by_genre.query('genre == @genre')['games'],
                mode='lines',
                stackgroup='one',
                name=genre,
            )
        ]
        sales_by_genre += [
            go.Bar(
                x=games_by_genre.query('genre == @genre')['year_of_release'],
                y=games_by_genre.query('genre == @genre')['total_copies_sold'],
                name=genre,
            )
        ]
    # gráfico de juegos lanzados por plataforma
    data_by_platform = [
        go.Pie(
            labels=games_by_platform['platform'],
            values=games_by_platform['games'],
            name='platforms',
        )
    ]

    # valores por año y gráfico de dispersión de género
    scores_by_genre = []
    for genre in filtered_score['genre'].unique():
        scores_by_genre += [
            go.Scatter(
                x=filtered_score.query('genre == @genre')['avg_user_score'],
                y=filtered_score.query('genre == @genre')['avg_critic_score'],
                mode='markers',
                name=genre,
            )
        ]
    # formar el resultado a mostrar
    return (
        {
            'data': data_by_genre,
            'layout': go.Layout(
                xaxis={'title': 'Año'}, yaxis={'title': y_label}
            ),
        },
        {
            'data': sales_by_genre,
            'layout': go.Layout(
                xaxis={'title': 'Año'},
                yaxis={'title': y_label_sales},
                barmode='stack',
            ),
        },
        {'data': data_by_platform, 'layout': go.Layout()},
        {
            'data': scores_by_genre,
            'layout': go.Layout(
                xaxis={'title': 'Puntuación media del usuario'},
                yaxis={'title': 'Puntuación media de la crítica'},
            ),
        },
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)