from datetime import datetime,date
import os 
import subprocess

from app.globais import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from view_control.graficos import Graficos

import sys
src_path = '../../src'
sys.path.append(src_path)
from utils.dag_utils import *
from show.model import brasil_model 


####################################################
#   PrepPage
####################################################

#variaveis
graficos = Graficos()
mdata = brasil_model.BrasilDada()
dash_var = DashVariables()

####################################################
#    View
####################################################
layout = [
    html.Div(
        [
            #Botoões escolha
            html.Div(
                [   html.Div([
                        html.Div([
                            html.Button('Cidades',
                                id='btn_cidades',
                                className='button-place'),
                            html.Button('Estados',
                                id='btn_estados',
                                className='button-place')
                        ],
                        style=dict(display='flex')
                        ),
                        dcc.Dropdown(
                            options=mdata.get_option_place(),
                            value='São Paulo',
                            id='place_dropdown',
                            style=dict(width='100%'))
                        ],
                        style=dict(width='50%'),
                        className='div-opcoes'),
                    html.Div([
                        html.Div(
                            "Periodo",
                            className='texto-opcao opcao-item'
                        ),
                        dcc.DatePickerRange(
                            id='city_dataRange',
                            start_date=datetime(2020, 3, 1),
                            end_date=datetime.now(),
                            className='opcao-item'
                        ),
                    ],className='div-opcoes')
                ],
                className='lista_opcoes div_horizontal'
            ),
            #Indicadores
            html.Div(
                [
                    graficos.indicator(
                        "#00cc96",
                        "Total de mortes",
                        "city_total_mortes",
                        p_width= "47%",
                        className='indicator plot'
                    ),
                    graficos.indicator(
                        "#00cc96",
                        "Status",
                        "city_status",
                        p_width="47%",
                        className='indicator plot'
                    ),
                    graficos.indicator(
                        "#00cc96",
                        "Total contaminados",
                        "city_total_contaminados",
                        p_width="47%",
                        className='indicator plot'
                    )
                ],
                className="div_horizontal",
                style={'padding':'3px'}
            ),

        #Graficos
            html.Div([
                    html.Div([],
                            id='city_casos_novos',
                            className='six columns grafico',
                            style={'padding':'5px'}),
                    html.Div([],
                            id='city_casos_acum', 
                            className='six columns grafico',
                            style={'padding':'5px'})
                ],
                className='row'),
            html.Div([
                    html.Div([],
                            id='city_mortes_novos',
                            className='six columns grafico',
                            style={'padding':'5px'}),
                    html.Div([],
                            id='city_mortes_acum', 
                            className='six columns grafico',
                            style={'padding':'5px'})
                ],
                className='row'),
            html.Div([],id='graph_states_obitos', className='row',style={'padding':'5px'}),
        ],
        className="container",
        id='conteiner'
    )
]

####################################################
#     Controle:: Callbacks para as ações
####################################################
@app.callback(
        [
            Output('btn_estados', 'className'),

            Output('btn_cidades', 'className'),
            Output('place_dropdown', 'options')
        ],
        [Input('btn_cidades', 'n_clicks'),
        Input('btn_estados', 'n_clicks')])
def show_input(clicks_cidades, clicks_estados):  
    #Se for o primeiro clck
    if  clicks_cidades is None:
        dash_var.update_attr(0,'btn_cidades')
        clicks_cidades = 0
    if clicks_estados is None:
        dash_var.update_attr(0,'btn_estados')
        clicks_estados = 0
    #demais clicks
    if clicks_cidades != dash_var.attr['btn_cidades'] \
    or clicks_cidades is None and clicks_estados is None:
        dash_var.update_attr(clicks_cidades,'btn_cidades')
        dict_data = mdata.get_option_place('city')
        return 'button-place','button-place-click',dict_data
    if clicks_estados != dash_var.attr['btn_estados']:
        dash_var.update_attr(clicks_estados,'btn_estados')
        dict_data = mdata.get_option_place('state')
        return 'button-place-click','button-place',dict_data
    else:
        dict_data = mdata.get_option_place('city')
        return 'button-place','button-place',dict_data

@app.callback(
    Output("city_total_mortes", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_total_mortes(place,start,end):
    start = start[:10]
    end = end[:10]
    return mdata.get_total_mortes(place,start,end)

@app.callback(
    Output("city_status", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_statuss(place,start,end):
    start = start[:10]
    end = end[:10]
    return mdata.calc_status(place,start,end)
    
    
@app.callback(
    Output("city_total_contaminados", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_total_contaminados(place,start,end):
    start = start[:10]
    end = end[:10]
    return mdata.get_total_casos(place,start,end)

@app.callback(
    Output("city_casos_novos", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_casos_novos(place,start,end):
    dict_grafico = {}
    start = start[:10]
    end = end[:10]
    dict_grafico['casos'] = mdata.get_casos_time(place,start,end)['sum']
    dict_grafico['media_movel'] = dict_grafico['casos'].rolling(window=7).mean()
    return graficos.grafico_brasil(dict_grafico,
                                    titulo='Casos Diarios',x_nome='data',y_nome='casos')

@app.callback(
    Output("city_mortes_novos", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_mortes_novas(place,start,end):
    dict_grafico = {}
    start = start[:10]
    end = end[:10]
    dict_grafico['mortes'] = mdata.get_mortes_time(place,start,end)['sum']
    dict_grafico['media_movel'] = dict_grafico['mortes'].rolling(window=7).mean()
    print(dict_grafico['media_movel'])
    return graficos.grafico_brasil(dict_grafico,
                                    titulo='Mortes Diarias',x_nome='data',y_nome='mortes')

@app.callback(
    Output("city_casos_acum", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_casos_acumulativo(place,start,end):
    start = start[:10]
    end = end[:10]
    df_data = mdata.get_casos_time(place,start,end,cumulative=True)
    return graficos.grafico_temporal({'mortes':df_data['sum']},
                                    titulo='Casos acumulativos',x_nome='data',y_nome='casos')

@app.callback(
    Output("city_mortes_acum", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def get_mortes_acumulativo(place,start,end):
    start = start[:10]
    end = end[:10]
    df_data = mdata.get_mortes_time(place,start,end,cumulative=True)
    return graficos.grafico_temporal({'mortes':df_data['sum']},
                                    titulo='Mortes acumulativas',x_nome='data',y_nome='mortes')

@app.callback(
    Output("graph_states_obitos", "children"),
    [Input("place_dropdown","value"),
    Input("city_dataRange","start_date"),
    Input("city_dataRange","end_date")]
)
def make_graph_obitos(place,start,end):
    if mdata.place_type != 'state':
        place = mdata.get_state(place) 
    start = start[:7]
    end = end[:7]
    df_data = mdata.get_obitos(place,start,end,'2020')
    df_data = df_data.drop('total',axis=1)
    df_data = df_data.dropna()
    dict_state ={}
    for  column in df_data:
        dict_state[column] = df_data[column]
    dict_state['covid'] = mdata.get_mortes_time(place,start,end)['sum']
    return graficos.grafico_temporal(dict_state,
                                    titulo='Obitos no estado 2020',
                                    x_nome='Data',
                                    y_nome='mortes')
