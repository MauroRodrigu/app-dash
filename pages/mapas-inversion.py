import plotly.express as px

import numpy as np

import pandas as pd

import dash

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
                                                     dcc.Dropdown(options = opciones,
                                                                 value= 'BUENOS AIRES',
                                                                 searchable= True, clearable= False,
                                                                 placeholder= 'Seleccionar provincia',
                                                                 id = 'filtro6',
                                                                 style= {'font-family':'Encode Sans'})], width = 12, lg=4),
                                              dbc.Col([html.H5('Filtrar por sectores', className= 'titulo',
                                                              style= {'font-family':'Encode Sans', 'color':'white', 'text-align':'center'}),
                                                      dcc.Dropdown(options=opc2,
                                                                  searchable=True, clearable=True,
                                                                  placeholder='Seleccionar por tipo de obra',
                                                                  id = 'filtro7',
                                                                  style= {'font-family':'Encode Sans'})], width=12, lg=4),
                                              dbc.Col([])
                                              
                                             ])
                                    ]),
                       html.Br(),html.Br(),
                       dbc.Container(dbc.Row([dbc.Col([dcc.Graph(id='mapa',
                                                               style= {'border-radius': '10px', 
                                                                       'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}), html.Br()], width = 12, lg=6),
                                              dbc.Col([dcc.Graph(id='graf3',
                                                                style= {'border-radius': '10px', 
                                                                       'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'})],width=12, lg=6),
                                              
                      ])),
                    html.Br()
                      ])



@callback(Output('mapa', 'figure'),
              Output('graf3', 'figure'),
             Input('filtro6', 'value'),
             Input('filtro7', 'value'))
def mapas(valor, valor2):
    if valor == 'TOTAL PAÍS':
        if valor2 == None:
            prov2 = prov[prov['Jurisdicción'] == valor]
            unidad = data['entidadejecutoranombre'].value_counts().reset_index().sort_values('entidadejecutoranombre')
            unidad['index'] = unidad['index'].str.capitalize()
            unidad['porc'] = [f'{i}%' for i in round(unidad['entidadejecutoranombre']/sum(unidad['entidadejecutoranombre'])*100,2)]
            dat = data.groupby(['nombreprovincia','nombredepto']).aggregate({'idproyecto':'count'}).sort_values('idproyecto', 
                                                                                                    ascending=False)
            dat = dat.reset_index()
            dat.columns = ['Provincia', 'Depto', 'Obras']
            loc = depto[['Provincia', 'Depto', 'Latitud', 'Longitud']]
            nvo = pd.merge(dat, loc, how = 'right')
            nvo['Latitud'] = nvo['Latitud'].astype('float')
            nvo['Longitud'] = nvo['Longitud'].astype('float')
            nvo['Obras'] = np.where(nvo['Obras'].isna() == True, 0, nvo['Obras'])
            

            graf = px.density_mapbox(nvo, lat = 'Latitud', lon= 'Longitud', z = 'Obras', hover_name= 'Depto',
                                     hover_data= {'Latitud': False, 'Longitud':False, 'Provincia':True},
                                     labels = {'Obras' : 'Cantidad de obras'},
                  title = 'Mapa de densidad - {}'.format(valor.title()), zoom = 2.4, 
                 mapbox_style = 'open-street-map', center = {'lon':float(prov2.Longitud),
                                                                 'lat':float(prov2.Latitud)},
                           height= 500, color_continuous_scale= 'viridis', opacity = 0.7)

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=15, b=10),
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=19)
            grafic = px.bar(unidad, x='entidadejecutoranombre', y='index', orientation= 'h', height=500,
                            text= 'entidadejecutoranombre', hover_name= 'index',
                            hover_data= {'entidadejecutoranombre': True, 'porc': True, 'index': False},
                            labels= {'index': 'Entidades', 'entidadejecutoranombre': 'Cantidad de obras',
                                    'porc': 'Porcentaje de obras sobre el total'},
                           title = 'Entidades ejecutoras de las inversiones')
            grafic.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafic.update_layout(font_size=9, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'},
                                  font_color='black', title_x=0.5, titlefont_size=19)
            return graf, grafic
        else:
            dat = data[data['sectornombre'] == valor2]
            unidad = dat['entidadejecutoranombre'].value_counts().reset_index().sort_values('entidadejecutoranombre')
            unidad['index'] = unidad['index'].str.capitalize()
            unidad['porc'] = [f'{i}%' for i in round(unidad['entidadejecutoranombre']/sum(unidad['entidadejecutoranombre'])*100,2)]
            prov2 = prov[prov['Jurisdicción'] == valor]
            dat = dat.groupby(['nombreprovincia','nombredepto']).aggregate({'idproyecto':'count'}).sort_values('idproyecto', 
                                                                                                    ascending=False)
            dat = dat.reset_index()
            dat.columns = ['Provincia', 'Depto', 'Obras']
            loc = depto[['Provincia', 'Depto', 'Latitud', 'Longitud']]
            nvo = pd.merge(dat, loc, how = 'right')
            nvo['Latitud'] = nvo['Latitud'].astype('float')
            nvo['Longitud'] = nvo['Longitud'].astype('float')
            nvo['Obras'] = np.where(nvo['Obras'].isna() == True, 0, nvo['Obras'])

            graf = px.density_mapbox(nvo, lat = 'Latitud', lon= 'Longitud', z = 'Obras', hover_name= 'Depto',
                                     hover_data= {'Latitud': False, 'Longitud':False, 'Provincia':True},
                                     labels = {'Obras' : 'Cantidad de obras'},
                  title = 'Mapa de densidad - {}'.format(valor.title()), zoom = 2.4, 
                 mapbox_style = 'open-street-map', center = {'lon':float(prov2.Longitud),
                                                                 'lat':float(prov2.Latitud)},
                           height= 500, color_continuous_scale= 'viridis', opacity = 0.7)

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=15, b=10),
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=19)
        
            grafic = px.bar(unidad, x='entidadejecutoranombre', y='index', orientation= 'h', height=500,
                           title = 'Entidades ejecutoras de las inversiones - {}'.format(valor2.capitalize()),
                            text= 'entidadejecutoranombre', hover_name= 'index',
                            hover_data= {'entidadejecutoranombre': True, 'porc': True, 'index': False},
                            labels= {'index': 'Entidades', 'entidadejecutoranombre': 'Cantidad de obras',
                                    'porc': 'Porcentaje de obras sobre el total'})
            grafic.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafic.update_layout(font_size=9, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'},
                                  font_color='black', title_x=0.5, titlefont_size=19)
        
            return graf, grafic
                
    else:    
        if valor2 == None:
            dat = data[(data['nombreprovincia'] == valor)]
            dep2 = depto[depto['Provincia'] == valor]
            prov2 = prov[prov['Jurisdicción'] == valor]
            unidad = dat['entidadejecutoranombre'].value_counts().reset_index().sort_values('entidadejecutoranombre')
            unidad['index'] = unidad['index'].str.capitalize()
            unidad['porc'] = [f'{i}%' for i in round(unidad['entidadejecutoranombre']/sum(unidad['entidadejecutoranombre'])*100,2)]
            dat = dat.groupby(['nombreprovincia','nombredepto']).aggregate({'idproyecto':'count'}).sort_values('idproyecto', 
                                                                                                    ascending=False)
            dat = dat.reset_index()
            dat.columns = ['Provincia', 'Depto', 'Obras']
            loc = dep2[['Provincia', 'Depto', 'Latitud', 'Longitud']]
            nvo = pd.merge(dat, loc, how = 'right')
            nvo['Latitud'] = nvo['Latitud'].astype('float')
            nvo['Longitud'] = nvo['Longitud'].astype('float')
            nvo['Obras'] = np.where(nvo['Obras'].isna() == True, 0, nvo['Obras'])

            graf = px.density_mapbox(nvo, lat = 'Latitud', lon= 'Longitud', z = 'Obras', hover_name= 'Depto',
                                     hover_data= {'Latitud': False, 'Longitud':False, 'Provincia':True},
                                     labels = {'Obras' : 'Cantidad de obras'},
                  title = 'Mapa de densidad - {}'.format(valor.title()), zoom = 5, 
                 mapbox_style = 'open-street-map', center = {'lon':float(prov2.Longitud),
                                                                 'lat':float(prov2.Latitud)},
                           height= 500, color_continuous_scale= 'viridis', opacity = 0.7)

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=15, b=10),
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=19)
        
            grafic = px.bar(unidad, x='entidadejecutoranombre', y='index', orientation= 'h', height=500,
                           title = 'Entidades ejecutoras de las inversiones', 
                            text= 'entidadejecutoranombre', hover_name= 'index',
                            hover_data= {'entidadejecutoranombre': True, 'porc': True, 'index': False},
                            labels= {'index': 'Entidades', 'entidadejecutoranombre': 'Cantidad de obras',
                                    'porc': 'Porcentaje de obras sobre el total'})
            grafic.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafic.update_layout(font_size=9, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'},
                                  font_color='black', title_x=0.5, titlefont_size=19)
        
            return graf, grafic
        else:
            dat = data[(data['nombreprovincia'] == valor)]
            dat = dat[dat['sectornombre'] == valor2]
            unidad = dat['entidadejecutoranombre'].value_counts().reset_index().sort_values('entidadejecutoranombre')
            unidad['index'] = unidad['index'].str.capitalize()
            unidad['porc'] = [f'{i}%' for i in round(unidad['entidadejecutoranombre']/sum(unidad['entidadejecutoranombre'])*100,2)]
            dep2 = depto[depto['Provincia'] == valor]
            prov2 = prov[prov['Jurisdicción'] == valor]
            dat = dat.groupby(['nombreprovincia','nombredepto']).aggregate({'idproyecto':'count'}).sort_values('idproyecto', 
                                                                                                    ascending=False)
            dat = dat.reset_index()
            dat.columns = ['Provincia', 'Depto', 'Obras']
            loc = dep2[['Provincia', 'Depto', 'Latitud', 'Longitud']]
            nvo = pd.merge(dat, loc, how = 'right')
            nvo['Latitud'] = nvo['Latitud'].astype('float')
            nvo['Longitud'] = nvo['Longitud'].astype('float')
            nvo['Obras'] = np.where(nvo['Obras'].isna() == True, 0, nvo['Obras'])

            graf = px.density_mapbox(nvo, lat = 'Latitud', lon= 'Longitud', z = 'Obras', hover_name= 'Depto',
                                     hover_data= {'Latitud': False, 'Longitud':False, 'Provincia':True},
                                     labels = {'Obras' : 'Cantidad de obras'},
                  title = 'Mapa de densidad - {}'.format(valor.title()), zoom = 5, 
                 mapbox_style = 'open-street-map', center = {'lon':float(prov2.Longitud),
                                                                 'lat':float(prov2.Latitud)},
                           height= 500, color_continuous_scale= 'viridis', opacity = 0.7)

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=15, b=10),
                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                             'font_color':'navy'}, font_color='black', title_x=0.5, font_size=12, titlefont_size=19)
        
            grafic = px.bar(unidad, x='entidadejecutoranombre', y='index', orientation= 'h', height=500,
                           title = 'Entidades ejecutoras de las inversiones - {}'.format(valor2.capitalize()),
                           text= 'entidadejecutoranombre', hover_name= 'index',
                            hover_data= {'entidadejecutoranombre': True, 'porc': True, 'index': False},
                            labels= {'index': 'Entidades', 'entidadejecutoranombre': 'Cantidad de obras',
                                    'porc': 'Porcentaje de obras sobre el total'})
            grafic.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafic.update_layout(font_size=9, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'},
                                  font_color='black', title_x=0.5, titlefont_size=19)
        
            return graf, grafic