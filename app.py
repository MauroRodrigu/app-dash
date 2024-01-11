import plotly.express as px

import numpy as np

import pandas as pd

import dash

from dash import Dash, dcc, html, ctx, Output, Input, State, dash_table

from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

import dash_mantine_components as dmc

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

# Paginas

portada = html.Div([dbc.Container([html.Br(), html.Br(), html.Br(),
                html.Br(), html.Br(), html.Br(), html.Br(),
                html.H1('La inversión pública en Argentina durante el período 2020-2023', id = 'titulo')]),
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
          dbc.Col([html.P('Fuente: Ministerio de Obras Públicas y censo 2022', className= 'tit2'),
                   html.P('Ultima actualización de datos: Diciembre de 2023', className= 'tit2'),
                   html.P('Autor: Lic. Mauro Rodríguez', className= 'tit2')],
                  width=4)])

pagina2 = html.Div([html.Br(),
                    html.Br(),
                    dbc.Container([dbc.Row([dbc.Col([html.H5('FILTRAR POR PROVINCIA:', className='titulo'),
                                                       dcc.Dropdown(options= opciones,
                                                                    value= 'TOTAL PAÍS', 
                                                                    searchable= True, clearable= False,
                                                                    placeholder= 'Seleccionar provincia',
                                                                    id= 'filtro')], 
                                                    width=4),
                                               dbc.Col([html.H5('FILTRAR POR DEPARTAMENTO/PARTIDO:', className='titulo'),
                                                       dcc.Dropdown(options = '',
                                                                   searchable=True, clearable=False,
                                                                   placeholder= 'Seleccionar departamento/partido',
                                                                   id = 'filtro2')], 
                                                       width=4)
                                              ])
                                     ]),
                       html.Br(),
                    html.Br(),
                    html.Br(),
                       dbc.Container([dbc.Row([dbc.Col([html.Div(id='grafico')], width= 6),
                                               dbc.Col([html.H6('Obras totales'),
                                             dbc.Card([html.P(id='obras', className= 'indicador')]),
                                                        html.Br(),
                                                        html.Br(),
                                                       html.H6('Porcentaje sobre total nacional', id= 'nac'),
                                            dbc.Card(html.P(id='porcentaje1', className='indicador')),
                                                       html.Br(),
                                                        html.Br(),
                                                       html.H6('Inversión millones de pesos'),
                                            dbc.Card(html.P(id='pesos', className='indicador'))],
                                            width=3),
                                   dbc.Col([html.H6('Obras cada 10.000 habitantes'),
                                            dbc.Card(html.P(id='ha', className='indicador')),
                                            html.Br(),
                                            html.Br(),
                                           html.H6('Porcentaje de obras finalizadas'),
                                            dbc.Card(html.P(id='finalizadas', className='indicador')),
                                           html.Br(),
                                            html.Br(),
                                           html.H6('Inversión millones de dólares'),
                                             dbc.Card(html.P(id='dolares', className='indicador'))], width=3)])
                                   
                                              ])])

pagina3 = html.Div([html.Br(),
                    html.Br(),
                    dbc.Container([dbc.Row([dbc.Col([html.H5('FILTRAR POR PROVINCIA:', className='titulo'),
                                                       dcc.Dropdown(options= opciones,
                                                                    value= 'TOTAL PAÍS', 
                                                                    searchable= True, clearable= False,
                                                                    placeholder= 'Seleccionar provincia',
                                                                    id= 'filtro3')], 
                                                       width=4),
                                               dbc.Col([html.H5('FILTRAR POR DEPARTAMENTO/PARTIDO:', className='titulo'),
                                                       dcc.Dropdown(options = '',
                                                                   searchable=True, clearable=False,
                                                                   placeholder= 'Seleccionar departamento/partido',
                                                                   id = 'filtro4')], 
                                                       width=4),
                                              dbc.Col([html.H5('DESAGREGAR POR TIPO DE OBRA', className= 'titulo'),
                                                      dcc.Dropdown(options=opc2,
                                                                  searchable=True, clearable=True,
                                                                  placeholder='Seleccionar por tipo de obra',
                                                                  id = 'filtro5')])])
                                     ]),html.Br(),html.Br(),
                       dbc.Container(dbc.Row([dbc.Col(dcc.Graph(id='graf_sector'), width = 8),
                                              dbc.Col([dbc.Card([html.P('Datos censales 2022', className= 'tit'),
                                                                html.P(id = 'nombre'),
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
                                                                           id= 'tabla')])], width =4)
                               ]))
                      ])

pagina4 = html.Div([html.Br(),
                      html.Br(),
                      dbc.Container([dbc.Row([dbc.Col([html.H5('FILTRAR POR PROVINCIA:', className='titulo'),
                                                     dcc.Dropdown(options = opciones,
                                                                 value= 'BUENOS AIRES',
                                                                 searchable= True, clearable= False,
                                                                 placeholder= 'Seleccionar provincia',
                                                                 id = 'filtro6')], width = 4),
                                              dbc.Col([html.H5('FILTRAR POR SECTORES', className= 'titulo'),
                                                      dcc.Dropdown(options=opc2,
                                                                  searchable=True, clearable=True,
                                                                  placeholder='Seleccionar por tipo de obra',
                                                                  id = 'filtro7')], width=4),
                                              dbc.Col([])
                                              
                                             ])
                                    ]),
                       html.Br(),html.Br(),
                       dbc.Container(dbc.Row([dbc.Col(dcc.Graph(id='mapa'), width = 6),
                                              dbc.Col([dcc.Graph(id='graf3')],width=6),
                                              
                      ]))
                      ])

# APP

app = Dash(external_stylesheets= [dbc.themes.BOOTSTRAP], title = 'Dashboard Obra Pública')

server = app.server

app.layout = html.Div([html.H1(id= 'subtitulo'),
                       dcc.Location(id='url'),
                      dbc.NavbarSimple([dbc.NavLink('Portada', href= '/', className= 'boton', id= 'bot1'),
                                       dbc.NavLink('Detalles generales',href= '/detalles-generales', 
                                                   className= 'boton', id= 'bot2'),
                                        dbc.NavLink('Obras por sector', href= '/obras-por-sector',
                                                    className= 'boton', id= 'bot3'),
                                       dbc.NavLink('Mapas de inversión pública', href= '/mapas-inversion', 
                                                   className= 'boton', id= 'bot4')],
                                       brand= 'Barra de navegación:', 
                                       brand_style= {'color':'RGB(55,187,237)','font-weight':'bold',
                                                     'font-family':'Encode Sans'}, color='RGB(240,240,240)'),
                      html.Div(id= 'contenido')])

@app.callback(Output('contenido', 'children'),
              Output('subtitulo', 'children'),
              Output('bot1', 'style'),
              Output('bot2', 'style'),
              Output('bot3', 'style'),
              Output('bot4', 'style'),
             Input('url', 'pathname'))
def link(ruta):
    if ruta == '/':
        return portada, 'Portada', {'background-color' : 'rgb(55,187,255)', 'color':'white'}, None, None, None
    elif ruta == '/detalles-generales':
        return pagina2, 'Detalles generales', None, {'background-color' : 'rgb(55,187,255)', 'color':'white'}, None, None
    elif ruta == '/obras-por-sector':
        return pagina3, 'Obras por sector', None, None, {'background-color' : 'rgb(55,187,255)', 'color':'white'}, None
    elif ruta == '/mapas-inversion':
        return pagina4, 'Mapa de la obra pública', None, None, None, {'background-color' : 'rgb(55,187,255)', 'color':'white'}
    
@app.callback(Output('filtro2', 'options'),
              Output('filtro2','value'),
             Input('filtro','value'),
            prevent_initial_call = True)
def filtro(valor):
    filt = data[data['nombreprovincia'] == valor]
    depto = filt['nombredepto'].sort_values().unique()
    return depto, None

@app.callback(Output('grafico', 'children'),
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
    return dcc.Graph(figure= graf)

@app.callback(Output('obras','children'),
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
@app.callback(Output('filtro4', 'options'),
              Output('filtro4','value'),
             Input('filtro3','value'),
            prevent_initial_call = True)
def filtro4(valor):
    filt = data[data['nombreprovincia'] == valor]
    depto = filt['nombredepto'].sort_values().unique()
    return depto, None
@app.callback(Output('graf_sector', 'figure'),
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

@app.callback(Output('mapa', 'figure'),
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

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=5, b=5),
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

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=5, b=5),
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

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=5, b=5),
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

            graf.update_layout(showlegend = False, font_family='Encode Sans', margin = dict(r=5, l=5, b=5),
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

app.run(debug=True)
