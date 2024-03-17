import dash

import plotly.express as px

import numpy as np

import pandas as pd

from dash import Dash, dcc, html, Output, Input, callback

import dash_bootstrap_components as dbc

import dash_ag_grid as dag

data = pd.read_csv('https://raw.githubusercontent.com/MauroRodrigu/app-dash/main/dataset.csv', index_col= 'Unnamed: 0')

depto = pd.read_csv('https://raw.githubusercontent.com/MauroRodrigu/app-dash/main/censo22_depto.csv', index_col= 'Unnamed: 0')

prov = pd.read_csv('https://raw.githubusercontent.com/MauroRodrigu/app-dash/main/censo22_provincia.csv', index_col = 'Unnamed: 0')

data['etapa'] = np.where(data['avancefisico'] == 100.0, 'Finalizadas', 'No finalizadas')

opciones = ['TOTAL PAÍS']
opc = list(data['nombreprovincia'].unique())
opc.sort(key = str.title)
opciones.extend(opc)

opc2 = data['sectornombre'].sort_values().unique()

opc3 = data['tipoproyecto'].sort_values().unique()

dash.register_page(__name__)

layout = html.Div([html.Br(),
                    html.Br(),
                    dbc.Container([dbc.Row([dbc.Col([html.H5('Filtrar por provincia:', className='titulo',
                                                            style= {'font-family':'Encode Sans', 'color':'white', 'text-align':'center'}),
                                                       dcc.Dropdown(options= opciones,
                                                                    value= 'TOTAL PAÍS', 
                                                                    searchable= True, clearable= False,
                                                                    placeholder= 'Seleccionar provincia',
                                                                    id= 'filtro', style= {'font-family':'Encode Sans'})], 
                                                    width=12, lg=4),
                                               dbc.Col([html.H5('Filtrar por departamento:', className='titulo',
                                                               style= {'font-family':'Encode Sans', 'color':'white', 'text-align':'center'}),
                                                       dcc.Dropdown(options = '',
                                                                   searchable=True, clearable=False,
                                                                   placeholder= 'Seleccionar departamento/partido',
                                                                   id = 'filtro2', style= {'font-family':'Encode Sans'})], 
                                                       width=12, lg=4)
                                              ])
                                     ]),
                       html.Br(),
                    html.Br(),
                    html.Br(),
                       dbc.Container([dbc.Row([dbc.Col([html.Div(id='grafico'), html.Br(), html.Br()], width= 12, lg=6),
                                               dbc.Col([html.H6('Obras totales', style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                             dbc.Card([html.P(id='obras', className= 'indicador',
                                                             style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'})],
                                                     style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}),
                                                        html.Br(),
                                                        html.Br(),
                                                       html.H6('Porcentaje sobre total nacional', id= 'nac',
                                                              style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                            dbc.Card(html.P(id='porcentaje1', className='indicador',
                                                           style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'}),
                                                    style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}),
                                                       html.Br(),
                                                        html.Br(),
                                                       html.H6('Inversión millones de pesos', 
                                                               style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                            dbc.Card(html.P(id='pesos', className='indicador', 
                                                           style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'}),
                                                    style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}), html.Br(), html.Br()],
                                            width=12, lg=3),
                                   dbc.Col([html.H6('Obras cada 10.000 habitantes', style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                            dbc.Card(html.P(id='ha', className='indicador',
                                                           style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'}),
                                                    style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}),
                                            html.Br(),
                                            html.Br(),
                                           html.H6('Porcentaje de obras finalizadas',style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                            dbc.Card(html.P(id='finalizadas', className='indicador',
                                                           style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'}),
                                                    style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}),
                                           html.Br(),
                                            html.Br(),
                                           html.H6('Inversión millones de dólares',style= {'font-family':'Encode Sans', 'color':'white',
                                                                                         'font-weight':'bold',
                                                                                         'text-align':'center'}),
                                             dbc.Card(html.P(id='dolares', className='indicador',
                                                            style = {'font-family':'Encode Sans',
                                                                      'color':'black', 'text-align': 'center',
                                                                      'font-weight':'bold', 'font-size':'20pt',
                                                                      'letter-spacing':'1px'}),
                                                     style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'})], width=12, lg=3)])
                                   
                                              ]), html.Br()])

@callback(Output('filtro2', 'options'),
              Output('filtro2','value'),
             Input('filtro','value'),
            prevent_initial_call = True)
def filtro(valor):
    filt = data[data['nombreprovincia'] == valor]
    depto = filt['nombredepto'].sort_values().unique()
    return depto, None

@callback(Output('grafico', 'children'),
              Input('filtro2','value'),
             Input('filtro', 'value'))
def filtro2(valor2, valor):
    if valor == 'TOTAL PAÍS':
        filt = data
    else:
        filt = data[data['nombreprovincia'] == valor]
        if valor2 != None:
            filt = filt[filt['nombredepto'] == valor2]
        else:
            filt
    cuenta = filt[filt['fechainicioanio'] >= 2020]
    cuenta = cuenta.groupby(['fechainicioanio', 'etapa']).aggregate({'idproyecto':'count',
                                                     'avancefisico':'mean',
                                                     'avancefinanciero':'mean'}).reset_index()
    cuenta['avancefisico'] = [f'{i}%' for i in round(cuenta['avancefisico'],2)]
    
    if (valor2 == None) | (valor2 == 'CIUDAD AUTÓNOMA DE BUENOS AIRES'):
        graf= px.bar(cuenta, x='fechainicioanio', y='idproyecto', title= 'Cantidad de obras por año - {}'.format(valor.title()),
                height=400, color= 'etapa', color_discrete_map={'Finalizadas':'rgb(55,187,237)','No finalizadas':'navy'},
                labels = {'etapa':'Etapa', 'fechainicioanio': 'Año de inicio',
                          'idproyecto':'Cantidad de obras', 'avancefisico':'Porcentaje de avance de las obras'},
                hover_data={'avancefisico':True, 'fechainicioanio':False, 'etapa':False}, hover_name= 'etapa',
                     template='plotly',
                    category_orders= {'fechainicioanio': [2020,2021,2022,2023], 'etapa':['Finalizadas', 'No finalizadas']})
        graf.update_layout(font_family='Encode Sans',
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=22,
                          )
        graf.update_xaxes(type='category')
    else:
        graf= px.bar(cuenta, x='fechainicioanio', y='idproyecto', title= 'Cantidad de obras por año - {} ({})'.format(valor2.title(),
                                                                                                                     valor.title()),
                height=400, color= 'etapa', color_discrete_map={'Finalizadas':'rgb(55,187,237)','No finalizadas':'navy'},
                labels = {'etapa':'Etapa', 'fechainicioanio': 'Año de inicio',
                          'idproyecto':'Cantidad de obras', 'avancefisico':'Porcentaje de avance de las obras'},
                hover_data={'avancefisico':True, 'fechainicioanio':False, 'etapa': False}, hover_name= 'etapa',
                     template='plotly',
                    category_orders= {'fechainicioanio': [2020,2021,2022,2023], 'etapa':['Finalizadas', 'No finalizadas']})
        graf.update_layout(font_family='Encode Sans',
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=22)
        graf.update_xaxes(type='category')
    return dbc.Card(dcc.Graph(figure= graf), style= {'border-radius': '10px', 'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'})

                                              
@callback(Output('obras','children'),
              Output('finalizadas','children'),
              Output('pesos', 'children'),
              Output('dolares', 'children'),
              Output('porcentaje1','children'),
              Output('ha', 'children'),
              Output('nac', 'children'),
             Input('filtro','value'),
             Input('filtro2', 'value'))
def filtro3(valor,valor2):
    if valor == 'TOTAL PAÍS':
        filt = data
        pob = int(prov['Población'][0])
        tipo = 'Porcentaje sobre el total nacional'
        total1 = len(data) 
    else:
        filt = data[data['nombreprovincia'] == valor]
        provincia = data[data['nombreprovincia'] == valor]
        total1 = len(data)
        pob = int(prov[prov['Jurisdicción'] == valor]['Población'])
        if valor2 != None:
            filt = provincia[provincia['nombredepto'] == valor2]
            pob = depto[depto['Provincia'] == valor]
            pob = int(pob[pob['Depto'] == valor2]['Población'])
            tipo = 'Porcentaje sobre el total provincial'
            total1 = len(provincia)
        else:
            filt
            pob
            tipo = 'Porcentaje sobre el total nacional'
        
    total = filt[filt['avancefisico'] == 100.0]
    no_total = filt[filt['avancefisico'] != 100.0]
    pesos = filt[filt['tipomoneda'] == 'pesos argentinos']
    dolares = filt[filt['tipomoneda'] == 'dolares estadounidenses']
    
    
    return ('{}'.format(len(filt)), '{}%'.format(round(len(total)/len(filt)*100,2)),
            '${}'.format(round(pesos['montototal'].sum()/1000000,2)),
           '${}'.format(round(dolares['montototal'].sum()/1000000,2)),
           '{}%'.format(round(len(filt)/float(total1)*100,2)),
           '{}'.format(round(len(filt)/pob*10000,2)),
           tipo)






