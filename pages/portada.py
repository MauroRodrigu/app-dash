import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_ag_grid as dag


dash.register_page(__name__, path='/')

layout = html.Div([dbc.Container([html.Br(), html.Br(), html.Br(),
                html.Br(), html.Br(), html.Br(), html.Br(),
                html.H1('La inversión pública en Argentina durante el período 2020-2023', id = 'titulo',
                       style= {'font-family':'Encode Sans', 'text-align': 'center', 'color':'white', 'width':'97%', 'font-weight':'bold'})]),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          dbc.Col([html.P('Fuente: Ministerio de Obras Públicas y censo 2022', className= 'tit2',
                         style = {'font-family':'Encode Sans', 'color':'white', 'text-align': 'center','font-size':'13pt',
                                  'width': '100%'}),
                   html.P('Ultima actualización de datos: Diciembre de 2023', className= 'tit2',
                         style = {'font-family':'Encode Sans', 'color':'white','text-align': 'center', 'font-size':'13pt',
                                  'width': '100%'}),
                   html.P('Autor: Lic. Mauro Rodríguez', className= 'tit2',
                         style = {'font-family':'Encode Sans', 'color':'white', 'text-align': 'center', 'font-size':'13pt',
                                  'width': '100%'})],
                  width=12, lg=4)])