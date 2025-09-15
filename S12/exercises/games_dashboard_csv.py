# Este código no funcionará porque falta bajar y direccionar el CSV

from dash import Dash, dcc, html, Input, Output

import plotly.graph_objs as go

import pandas as pd

# definir los datos a mostrar
games_raw = pd.read_csv('/datasets/games_full.csv')
games_raw['Year_of_Release'] = pd.to_datetime(games_raw['Year_of_Release'])

# definir los datos para el informe
games_grouped = (
    games_raw.groupby(['Genre', 'Year_of_Release'])
    .agg({'Name': 'count'})
    .reset_index()
    .rename(columns={'Name': 'Games Released'})
)

#print(games_grouped)

# definir los gráficos que se mostrarán
data = []
for genre in games_grouped['Genre'].unique():
    current = games_grouped.query('Genre == @genre')
    data += [
        go.Scatter(
            x=current['Year_of_Release'],
            y=current['Games Released'],
            mode='lines',
            stackgroup='one',
            name=genre,
        )
    ]
# definir el diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(
    __name__, external_stylesheets=external_stylesheets, compress=False
)
app.layout = html.Div(
    children=[
        # html
        html.H1(children='Juegos lanzados por año'),
        dcc.Graph(
            figure={
                'data': data,
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


