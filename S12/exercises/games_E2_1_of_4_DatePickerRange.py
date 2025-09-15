#!/usr/bin/python
# -*- codificación: utf-8 -*-

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd

# configurar los datos a mostrar
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database/games.db", future=True, echo=False)

# obtención de datos en bruto
query = 'SELECT * FROM data_raw'
games_raw = pd.io.sql.read_sql(query, con = engine)

# tipos de conversión
games_raw['year_of_release'] = pd.to_datetime(games_raw['year_of_release'])
columns = ['na_players', 'eu_players', 'jp_players', 'other_players']
for column in columns: games_raw[column] = pd.to_numeric(games_raw[column], errors = 'coerce')

# definir los datos para el informe
games_grouped = (games_raw.groupby(['year_of_release', 'genre'])
                          .agg({'name': 'nunique'})
                          .reset_index()
                          .rename(columns = {'name': 'games_launched'})
                )

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,compress=False)
app.layout = html.Div(children=[  
    
    # formar un encabezado con una etiqueta HTML
    html.H1(children = 'Juegos lanzados por año'),

    # seleccionar el intervalo de tiempo
    html.Label('Time range:'),
    dcc.DatePickerRange(
        start_date = games_grouped['year_of_release'].dt.date.min(),
        end_date = datetime(2016,1,1).strftime('%Y-%m-%d'),
        initial_visible_month = datetime(2016, 1, 1).strftime('%Y-%m-%d'), # definir el mes del calendario que se muestra por primera vez
        display_format = 'YYYY-MM-DD',
        id = 'dt_selector',       
    ),   

    # gráfico de juegos lanzados por año
    dcc.Graph(
        id = 'launches_by_year'
    ),         
 
])

# lógica del dashboard
@app.callback(
    [
        Output('launches_by_year', 'figure'),
    ],
    [
        Input('dt_selector', 'start_date'),
        Input('dt_selector', 'end_date'),
    ],
)
def update_figures(start_date, end_date):
    # convertir parámetros de entrada a los tipos requeridos
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # aplicar filtros
    filtered_data = games_grouped.query(
        'year_of_release >= @start_date and year_of_release <= @end_date'
    )

    # construir gráficos para mostrar
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