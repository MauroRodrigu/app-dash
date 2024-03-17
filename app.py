import dash

from dash import Dash, dcc, html, Output, Input

import dash_bootstrap_components as dbc

import dash_ag_grid as dag

app = Dash(__name__, use_pages = True, external_stylesheets= [dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Encode+Sans:wght@300&display=swap"], title = 'Dashboard Obra Pública',
          meta_tags=[{'name':'viewport','content':'width=device-width, initial-scale=1.0'}])

app.layout = html.Div([dbc.Row(html.H1(id= 'subtitulo',
                              style= {'font-family':'Encode Sans', 'width':'97%', 'font-weight':'bold', 
                                     'color': 'white'}), style= {'background-color':'RGB(55,187,237)'}),
                       dcc.Location(id='url'),
                      dbc.NavbarSimple([dbc.NavLink('Portada',
                                                    href= '/', className= 'boton'),
                                       dbc.NavLink('Detalles generales',href= '/detalles-generales', 
                                                   className= 'boton'),
                                        dbc.NavLink('Obras por sector', href= '/obras-por-sector',
                                                    className= 'boton'),
                                       dbc.NavLink('Mapas de inversión pública', href= '/mapas-inversion', 
                                                   className= 'boton')],
                                       brand= 'Barra de navegación:', 
                                       brand_style= {'color':'RGB(55,187,237)','font-weight':'bold',
                                                     'font-family':'Encode Sans'}, color='RGB(240,240,240)'),
                      dash.page_container])


@app.callback(Output('subtitulo', 'children'),
             Input('url', 'pathname'))
def link(ruta):
    if ruta == '/':
        return 'Portada'
    elif ruta == '/detalles-generales':
        return 'Detalles generales'
    elif ruta == '/obras-por-sector':
        return 'Obras por sector'
    elif ruta == '/mapas-inversion':
        return 'Mapa de la obra pública'

if __name__ == '__main__':
    app.run()
