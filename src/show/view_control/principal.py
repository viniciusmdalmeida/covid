import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64

from app.globais import app
from view_control import conteiner

layout = html.Div([
        #Abas
        html.Div(className="header",
        children=[
                #Titulo
            html.H1("Piloto industrialização",
            className='title'),
            
            dcc.Tabs(
                id = "tabs",
                parent_className='custom-tabs',
                className='custom-tabs-container',
                children=[
                        dcc.Tab(label='Graficos',
                            value='graficos',
                            className='custom-tab',
                            selected_className='custom-tab--selected'),
                        dcc.Tab(label='Airflow',
                                value='airflow',
                                className='custom-tab',
                                selected_className='custom-tab--selected'),
                        dcc.Tab(label='MlFlow',
                            value='mlflow',
                            className='custom-tab',
                            selected_className='custom-tab--selected')
                ],
                value='graficos')
        ]),

        #Conteudo de cada aba
        html.Div(id='tab_content',className='content',style={'padding':'20px'}),

        #Pegando estilos
        html.Link(href="https://fonts.googleapis.com/css?family=Montserrat&display=swap", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
        rel="stylesheet"),
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")

    ],
    className="row",
    style={"margin": "0%"})

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def trocar_aba(tab):
    if tab == "graficos":
        return conteiner.layout
    elif tab == "airflow":
        print('location')
        return dcc.Location(href="http://0.0.0.0:8080/", id="id_airflow")
    elif tab == 'mlflow':
        return dcc.Location(href="http://127.0.0.1:5000", id="id_mlflow")