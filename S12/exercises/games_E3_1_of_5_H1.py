#!/usr/bin/python
# -*- codificación: utf-8 -*-


from dash import Dash, dcc, html, Input, Output

import plotly.graph_objs as go

note = '''
          Este dashboard te ayudará a aprender los conceptos básicos de composición.
       '''

# definición del diseño
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(
    __name__, external_stylesheets=external_stylesheets, compress=False
)
app.layout = html.Div(
    children=[
        # crear un encabezado con una etiqueta HTML
        html.H1(children='Historial del mercado de juegos'),
        html.Br(),
        # descripción
        html.Label(note),
        html.Br()
    ]
)

# lógica del dashboard
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)