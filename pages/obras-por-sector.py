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
                                                                    id= 'filtro3',
                                                                   style= {'font-family':'Encode Sans'})], 
                                                       width=12, lg=4),
                                               dbc.Col([html.H5('Filtrar por departamento:', className='titulo',
                                                               style= {'font-family':'Encode Sans', 'color':'white', 'text-align':'center'}),
                                                       dcc.Dropdown(options = '',
                                                                   searchable=True, clearable=False,
                                                                   placeholder= 'Seleccionar departamento/partido',
                                                                   id = 'filtro4',
                                                                   style= {'font-family':'Encode Sans'})], 
                                                       width=12, lg=4),
                                              dbc.Col([html.H5('Desagregar por sector', className= 'titulo',
                                                              style= {'font-family':'Encode Sans', 'color':'white', 'text-align':'center'}),
                                                      dcc.Dropdown(options=opc2,
                                                                  searchable=True, clearable=True,
                                                                  placeholder='Seleccionar por tipo de obra',
                                                                  id = 'filtro5',
                                                                  style= {'font-family':'Encode Sans'})])])
                                     ]),html.Br(),html.Br(),
                       dbc.Container(dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graf_sector'),
                                                              style= {'border-radius': '10px',
                                                                      'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'}), html.Br()], width = 12, lg=8),
                                              dbc.Col([dbc.Card([html.P('Datos censales 2022', className= 'tit',
                                                                       style= {'font-family':'Encode Sans',
                                                                               'text-align': 'center',
                                                                               'font-size':'13pt',
                                                                               'width': '100%'}),
                                                                html.P(id = 'nombre',
                                                                      style = {'font-family':'Encode Sans',
                                                                              'text-align':'center'}),
                                                                dag.AgGrid(columnDefs= [dict(field='Indicador',
                                                                                            filter = False,
                                                                                            sortable = False, 
                                                                                             editable = False,
                                                                                             resizable= True,
                                                                                            width = 85),
                                                                                       dict(field='Valor',
                                                                                            filter = False,
                                                                                            sortable = False, 
                                                                                             editable = False,
                                                                                             resizable= True, 
                                                                                           width = 15)],
                                                                           dashGridOptions={'pagination':False}, # paginación
                                                                           className= 'ag-theme-alpine', # Temas 
                                                                           columnSize= 'sizeToFit', # ajusta las columnas
                                                                           style = {'font-family':'Encode Sans',
                                                                                    'font-size':'12pt',
                                                                                    'height':'415px'},
                                                                           id= 'tabla')],
                                                               style= {'border-radius': '10px', 
                                                                       'box-shadow': '10px 10px 3px 1px',
                                                             'border': '1px solid black'})], width =12, lg=4)
                               ])),
                   html.Br()
                      ])

@callback(Output('filtro4', 'options'),
              Output('filtro4','value'),
             Input('filtro3','value'),
            prevent_initial_call = True)
def filtro4(valor):
    filt = data[data['nombreprovincia'] == valor]
    depto = filt['nombredepto'].sort_values().unique()
    return depto, None
@callback(Output('graf_sector', 'figure'),
              Output('nombre', 'children'),
              Output('tabla', 'rowData'),
             Input('filtro3', 'value'),
             Input('filtro4', 'value'),
             Input('filtro5', 'value'))
def graf2(valor, valor2, valor3):
    if (valor == 'TOTAL PAÍS'):
        nomb = 'Total país'
        if (valor3 != None) & (valor2 == None):
            filt = data[data['sectornombre'] == valor3]
            datos3 = filt['tipoproyecto'].value_counts().reset_index().sort_values('tipoproyecto')
            datos3['index'] = datos3['index'].str.capitalize()
            datos3['porc'] = [f'{i}%' for i in round(datos3['tipoproyecto']/sum(datos3['tipoproyecto'])*100,2)]
            datos3 = datos3.head(15)
            grafico = px.bar(datos3, x='tipoproyecto', y='index', orientation= 'h', height=500,
                            title = 'Obras totales en el país - sector {}'.format(valor3.lower()),
                            text = datos3['tipoproyecto'], labels= {'tipoproyecto':'Cantidad de obras',
                                                           'index':'Tipo de Obra',
                                                                   'porc':'Porcentaje - sector {}'.format(valor3.lower())}, 
                             hover_name= 'index',
                            hover_data= {'index': False, 'porc': True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'},
                                  font_color='black', title_x=0.5, titlefont_size=19)
            dat = prov[prov['Jurisdicción'] == 'TOTAL PAÍS'].T
            dat = dat.reset_index()
            dat = dat.iloc[1:12,]
            dat.columns = ['Indicador', 'Valor']
        else:
            datos3 = data.groupby('sectornombre').aggregate({'idproyecto':'count'}).reset_index().sort_values('idproyecto')
            datos3['sectornombre'] = datos3['sectornombre'].str.capitalize()
            datos3['porc'] = [f'{i}%' for i in round(datos3['idproyecto']/len(data)*100,2)]
            grafico = px.bar(datos3, x='idproyecto', y='sectornombre', orientation= 'h', height=500,
                            title = 'Obras totales en el país por sectores',
                            text = 'idproyecto', labels= {'idproyecto':'Cantidad de obras',
                                                           'sectornombre':'Sector',
                                                         'porc': 'Porcentaje sobre el total de obras'}, hover_name= 'sectornombre',
                            hover_data= {'sectornombre': False, 'porc':True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False,
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'}, 
                                  font_family='Encode Sans', 
                                  font_color='black', title_x=0.5, titlefont_size=19)
            dat = prov[prov['Jurisdicción'] == 'TOTAL PAÍS'].T
            dat = dat.reset_index()
            dat = dat.iloc[1:12,]
            dat.columns = ['Indicador', 'Valor']
        return grafico, nomb, dat.to_dict('records')
    else:
        filt = data[data['nombreprovincia'] == valor]
        nomb = '{}'.format(valor.title())
        if (valor2 != None) & (valor3 != None):
            filt = filt[filt['nombredepto'] == valor2]
            filt = filt[filt['sectornombre'] == valor3]
            filt = filt['tipoproyecto'].value_counts().reset_index().sort_values('tipoproyecto')
            filt['index'] = filt['index'].str.capitalize()
            filt['porc'] = [f'{i}%' for i in round(filt['tipoproyecto']/sum(filt['tipoproyecto'])*100,2)]
            filt = filt.head(15)
            grafico = px.bar(filt, x='tipoproyecto', y='index', orientation= 'h', height=500,
                            title = 'Obras en {}, {} - sector {}'.format(valor2.title(), valor.title(), valor3.lower()),
                            text = 'tipoproyecto', labels= {'tipoproyecto':'Cantidad de obras',
                                                           'index':'Sector',
                                                           'porc':'Porcentaje - sector {}'.format(valor3.lower())},
                             hover_name= 'index', hover_data= {'index': False, 'porc': True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'}, 
                                  font_color='black', title_x=0.5, titlefont_size=19)
            nomb = '{}, {}'.format(valor2.title(), valor.title())
            dat = depto[depto['Provincia'] == valor]
            dat = dat[dat['Depto'] == valor2].T
            dat = dat.reset_index()
            dat = dat.iloc[2:12,]
            dat.columns = ['Indicador', 'Valor']
        if (valor2 == None) & (valor3 != None):
            filt = filt[filt['sectornombre'] == valor3]
            filt = filt['tipoproyecto'].value_counts().reset_index().sort_values('tipoproyecto')
            filt['index'] = filt['index'].str.capitalize()
            filt['porc'] = [f'{i}%' for i in round(filt['tipoproyecto']/sum(filt['tipoproyecto'])*100,2)]
            filt = filt.head(15)
            grafico = px.bar(filt, x='tipoproyecto', y='index', orientation= 'h', height=500,
                            title = 'Obras en {} - sector {}'.format(valor.title(), valor3.lower()),
                            text = 'tipoproyecto', labels= {'index':'Sector',
                                                           'tipoproyecto':'Cantidad de obras',
                                                           'porc': 'Porcentaje - sector {}'.format(valor3.lower())},
                            hover_name= 'index', hover_data= {'index': False, 'porc': True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'}, 
                                  font_color='black', title_x=0.5, titlefont_size=19)
            dat = prov[prov['Jurisdicción'] == valor].T
            dat = dat.reset_index()
            dat = dat.iloc[1:12,]
            dat.columns = ['Indicador', 'Valor']
        if (valor2 != None) & (valor3 == None):
            filt = filt[filt['nombredepto'] == valor2]
            filt = filt.groupby('sectornombre').aggregate({'idproyecto':'count'}).reset_index().sort_values('idproyecto')
            filt['sectornombre'] = filt['sectornombre'].str.capitalize()
            filt['porc'] = [f'{i}%' for i in round(filt['idproyecto']/sum(filt['idproyecto'])*100,2)]
            grafico = px.bar(filt, x='idproyecto', y='sectornombre', orientation= 'h', height=500,
                            title = 'Obras en {}, {} por sectores'.format(valor2.title(), valor.title()),
                            text = 'idproyecto', labels= {'idproyecto':'Cantidad de obras',
                                                           'sectornombre':'Sector',
                                                         'porc': 'Porcentaje sobre total de obras'},
                            hover_name= 'sectornombre', hover_data= {'sectornombre':False, 'porc':True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'}, 
                                  font_color='black', title_x=0.5, titlefont_size=19)
            nomb = '{}, {}'.format(valor2.title(), valor.title())
            dat = depto[depto['Provincia'] == valor]
            dat = dat[dat['Depto'] == valor2].T
            dat = dat.reset_index()
            dat = dat.iloc[2:12,]
            dat.columns = ['Indicador', 'Valor']
        if (valor2 == None) & (valor3 == None):
            datos3 = filt.groupby('sectornombre').aggregate({'idproyecto':'count'}).reset_index().sort_values('idproyecto')
            datos3['sectornombre'] = datos3['sectornombre'].str.capitalize()
            datos3['porc'] = [f'{i}%' for i in round(datos3['idproyecto']/sum(datos3['idproyecto'])*100,2)]
            grafico = px.bar(datos3, x='idproyecto', y='sectornombre', orientation= 'h', height=500,
                            title = 'Obras en {} por sectores'.format(valor.title()),
                            text = 'idproyecto', labels= {'idproyecto':'Cantidad de obras',
                                                           'sectornombre':'Sector',
                                                         'porc':'Porcentaje sobre total de obras'},
                            hover_name= 'sectornombre', hover_data= {'sectornombre':False, 'porc':True})
            grafico.update_traces(marker_color='rgb(55,187,237)', marker_line_color='navy', marker_line_width=2, opacity= 0.7,
                  textfont_size=13, textangle=0, textposition='outside')
            grafico.update_layout(font_size=10, margin= dict(b=5, r=15),showlegend=False, 
                                  font_family='Encode Sans', 
                                  hoverlabel={'bgcolor':'white', 'font_size':16, 'font_family':'Encode Sans',
                                              'font_color':'navy'}, 
                                  font_color='black', title_x=0.5, titlefont_size=19)
            dat = prov[prov['Jurisdicción'] == valor].T
            dat = dat.reset_index()
            dat = dat.iloc[1:12,]
            dat.columns = ['Indicador', 'Valor']
        return grafico, nomb, dat.to_dict('records')
