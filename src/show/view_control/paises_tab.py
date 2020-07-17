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
from show.model import worl_model

####################################################
#   PrepPage
####################################################

#variaveis
#TODO: Conseguir pegar o model_path do dag_industrial
graficos = Graficos()
wdata = worl_model.WorldHealth()
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
                        html.Div(
                            "Paises",
                            className='texto-opcao opcao-item'
                        ),
                        dcc.Dropdown(
                            options=wdata.get_list_dict_countrys(),
                            value=['BR','AR','US'],
                            id='world_dropdown',
                            multi=True,
                            style=dict(width='100%'))
                        ],
                        style=dict(width='30%'),
                        className='div-opcoes'),
                    html.Fieldset(
                        [
                            html.Legend('Normalizações'),
                            html.Button('Por mi hab',
                                id='btn_milhao',
                                className='div-opcoes',
                                style={'float':'left'}),
                            html.Button('1º caso',
                                id='btn_primeiro_caso',
                                className='div-opcoes',
                                style={'float':'left'}),
                        ],
                        className="div-opcoesdiv_horizontal",
                        style={'padding':'3px'},
                    ),
                    html.Div([
                        html.Div(
                            "Periodo",
                            className='texto-opcao opcao-item'
                        ),
                        dcc.DatePickerRange(
                            id='world_dataRange',
                            start_date=datetime(2020, 3, 1),
                            end_date=datetime.now(),
                            className='opcao-item'
                        ),

                    ],className='div-opcoes')
                ],
                className='lista_opcoes div_horizontal'
            ),

            #Graficos
            html.Div([],id='world_map',className='row',style={'padding':'5px'}),
            html.Div([],id='world_deaths_acum',className='row',style={'padding':'5px'}),
            html.Div([],id='mortes_novos', className='row',style={'padding':'5px'}),
            html.Div([],id='world_confirmed_acum',className='row',style={'padding':'5px'}),
            html.Div([],id='casos_novos', className='row',style={'padding':'5px'}),
        ],
        className="container",
        id='conteiner'
    )
]

####################################################
#     Controle: Callbacks para as ações
####################################################
@app.callback(
    Output("btn_milhao", "className"),
    [Input("btn_milhao","n_clicks")]
)
def click_milhao(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return 'button-place-click'
    else:
        return 'button-place'
        
@app.callback(
    [Output("btn_primeiro_caso", "className"),
     Output("world_dataRange", "disabled")],
    [Input("btn_primeiro_caso","n_clicks")]
)
def click_f_day(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return 'button-place-click',True
        
    else:
        return 'button-place',False
        
@app.callback(
    Output("world_deaths_acum", "children"),
    [Input("world_dropdown","value"),
    Input("world_dataRange","start_date"),
    Input("world_dataRange","end_date"),
    Input("btn_milhao","n_clicks"),
    Input("btn_primeiro_caso","n_clicks")]
)
def get_total_mortes(list_countrys,start,end,click_milhao,click_f_day):
    if click_milhao and click_milhao % 2 == 1:
        p_milhao = True
    else:
        p_milhao = False
    if click_f_day and click_f_day % 2 == 1:
        f_day = True
        x_nome = 'Dias após primeira morte'
    else:
        f_day = False
        x_nome = 'Data'
    dict_data = {}
    for country_code in list_countrys:
        dict_data[country_code] = wdata.get_deaths_by_country(country_code,start,end,
                                                            serie=True,p_milhao=p_milhao,f_day=f_day)
    return graficos.grafico_temporal(dict_data,
                                    titulo='Mortes diarias',
                                    x_nome=x_nome,
                                    y_nome='mortes')

@app.callback(
    Output("world_confirmed_acum", "children"),
    [Input("world_dropdown","value"),
    Input("world_dataRange","start_date"),
    Input("world_dataRange","end_date"),
    Input("btn_milhao","n_clicks"),
    Input("btn_primeiro_caso","n_clicks")]
)
def get_total_contaminados(list_countrys,start,end,click_milhao,click_f_day):
    if click_milhao and click_milhao % 2 == 1:
        p_milhao = True
    else:
        p_milhao = False
    if click_f_day and click_f_day % 2 == 1:
        f_day = True
        x_nome = "Dias após primeiro caso"
    else:
        f_day = False
        x_nome = "Data"
    
    dict_data = {}
    for country_code in list_countrys:
        dict_data[country_code] = wdata.get_confirmed_by_country(country_code,start,end,
                                                                serie=True,p_milhao=p_milhao,f_day=f_day)
    return graficos.grafico_temporal(dict_data,
                                    titulo='Casos diarios',
                                    x_nome=x_nome,
                                    y_nome='casos')

@app.callback(
    Output("world_map", "children"),
    [Input("btn_milhao","n_clicks")]
)
def get_world_map(click_milhao):
    if click_milhao and click_milhao % 2 == 1:
        norm = True   
    else:
        norm = False
    data_col = 'new_deaths'
    world_data = wdata.get_word_data(norm,data_col) 
    if norm:
        nome = 'mortes Mi. hab'
    else:
        nome = 'total de mortes'
    world_data = world_data.rename(columns={"country": "pais", data_col: nome})
    return graficos.map_graph(world_data,'pais',nome,hover_name='pais')
