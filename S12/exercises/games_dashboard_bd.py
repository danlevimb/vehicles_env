# Crear dashboard desd una bd

from dash import Dash, dcc, html, Input, Output

import plotly.graph_objs as go

import pandas as pd

# establecer los datos que se mostrarán
from sqlalchemy import create_engine

# código de muestra para conectarse a la base de datos con SQLite
engine = create_engine('sqlite:////db/games.db', echo=False)

# obtener datos en bruto
query = 'select * from data_raw'
games_raw = pd.io.sql.read_sql(query, con=engine)

# definir los datos para el informe
games_grouped = (
    games_raw.groupby(['genre', 'year_of_release'])
    .agg({'name': 'count'})
    .reset_index()
    .rename(columns={'name': 'Games Released'})
)

# definir los gráficos que se mostrarán
data_games_by_year = []
for genre in games_grouped['genre'].unique():
    current = games_grouped.query('genre == @genre')
    data_games_by_year += [go.Scatter(x=current['year_of_release'], y=current['Games Released'], mode='lines', stackgroup='one', name=genre)]
  
# definir el diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, compress=False
)
app.layout = html.Div(
    children=[
        # html
        html.H1(children='Juegos lanzados por año'),
        dcc.Graph(
            figure={
                'data': data_games_by_year,
                'layout': go.Layout(
                    xaxis={'title': 'Año'}, yaxis={'title': 'Juegos lanzados'}
                ),
            },
            id='games_by_year',
        ),
    ]
)

# lógica del dashboard
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)