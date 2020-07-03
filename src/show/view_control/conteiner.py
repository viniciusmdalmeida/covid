import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime,date
import os 
import subprocess
import yaml


from app.globais import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from view_control.graficos import Graficos

import sys
src_path = '../../src'
sys.path.append(src_path)
from utils.dag_utils import *
####################################################
#    Model
####################################################
class MDada():
    def getIndex(self,valor):
        return datetime.strftime(valor, '%Y/%m')

    def __init__(self):
        self.db = Database()

    def get_master(self):
        master_table = self.db.get_table('master_table')
        master_table['date'] = pd.to_datetime(self.master_table['date'])
        master_table = self.master_table.set_index('date')
        return master_table

    def get_revenue_data(self,start,end,freq='d',op='sum'):
        query = f"SELECT revenue,date FROM master_table WHERE date BETWEEN '{start}' AND '{end}'"
        print('Get Revenue\n',query)
        revenue = self.db.execute_query(query)
        revenue['date'] = pd.to_datetime(revenue['date'])
        revenue = revenue.set_index('date')
        revenue = revenue.groupby(pd.Grouper(freq=freq)).sum()
        return revenue

    def get_predict(self,start,end,freq='d',op='sum'):
        query = f"SELECT * FROM predict WHERE date BETWEEN '{start}' AND '{end}'"
        predict = self.db.execute_query(query)
        predict['date'] = pd.to_datetime(predict['date'])
        predict = predict.set_index('date')
        predict = predict.groupby(pd.Grouper(freq=freq)).sum()
        return predict

    def get_total_revenue(self,start=None,end=None):
        print(f'get total revenue start {start} end {end}')
        if start is None and end is None:
            query = 'SELECT sum(revenue) FROM master_table'
        else:
            query = f"SELECT sum(revenue) FROM master_table WHERE date BETWEEN '{start}' AND '{end}'"
        sum_value = self.db.execute_query(query)
        print("Total:",sum_value.iloc[0].values[0])
        return str(sum_value.iloc[0].values[0])

    def get_exchange(self,table,start,end):
        query = f"SELECT {table} FROM master_table WHERE index BETWEEN '{start}' AND '{end}'"
        df_exchange = self.db.get_table(table)
        df_exchange['index'] = pd.to_datetime(df_exchange['index'])
        df_exchange = df_exchange.set_index('index')
        return df_exchange


####################################################
#   PrepPage
####################################################

#variaveis
#TODO: Conseguir pegar o model_path do dag_industrial
project_path = '/home/vinicius/Documents/Projetos/Claro/Piloto/industrializacao'
conf_model_path = f'{project_path}/config/model_config.yaml'
config_model_file = open(conf_model_path)
config_model = yaml.load(config_model_file, Loader=yaml.FullLoader)
config_model_file.close()

list_models = os.listdir(config_model['model']['models_path'])
list_option_model = []
for i in list_models:
    list_option_model.append({'label':i[:5],'value':i})
actual_idmodel = config_model['model']['id']

graficos = Graficos()
mdata = MDada()

####################################################
#    View
####################################################

layout = [
    html.Div(
        [
            #Botoões escolha
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id = 'dropdown_tipo',
                            options=[
                                {'label':'Real','value':'usd_brl'},
                                {'label':'Euro','value':'usd_eur'}
                            ],
                            value='usd_eur',
                            className='plot'
                        ),
                        className="two columns",
                    ),
                    html.Div([
                            html.Div(
                                "Modelo",
                                className='texto-opcao opcao-item'
                            ),
                            html.Div(
                                dcc.Dropdown(
                                    id = 'dropdown_modelo',
                                    options=list_option_model,
                                    value=actual_idmodel,
                                    className='plot'
                                ),
                                className="opcao-item",
                            )
                        ],className='div-opcoes'),
                    html.Div([
                        html.Div(
                            "Periodo",
                            className='texto-opcao opcao-item'
                        ),
                        dcc.DatePickerRange(
                            id='dataRange',
                            start_date=datetime(2000, 1, 1),
                            end_date=datetime(2014, 12, 1),
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
                        "Receita total atual",
                        "receita_van",
                        p_width= "47%",
                        className='indicator plot',
                        children = mdata.get_total_revenue()
                    ),
                    graficos.indicator(
                        "#00cc96",
                        "Receita total prevista",
                        "receita_total",
                        p_width="47%",
                        className='indicator plot',
                        children = mdata.get_total_revenue()
                    )
                ],
                className="div_horizontal",
                style={'padding':'3px'}
            ),

            #Graficos
            html.Div([],id='predict',className='row',style={'padding':'5px'}),
            html.Div([],id='moeda', className='row',style={'padding':'5px'}),
            html.Div(id='hidden-div', style={'display':'none'})
        ],
        className="container",
        id='conteiner'
    )
]

####################################################
#     Professores Controle: Callbacks para as ações
####################################################

@app.callback(
    Output("predict", "children"),
    [Input("dataRange","start_date"),Input("dataRange","end_date")]
)
def get_predict(start,end):
    start = start[:10]
    end = end[:10]
    df_revenue = mdata.get_revenue_data(start,end)
    df_predict = mdata.get_predict(start,end) 
    return graficos.grafico_temporal({'revenue':df_revenue['revenue'],'predict':df_predict['0']},
                                    titulo='Revenue',x_nome='data',y_nome='value')

@app.callback(
    Output("moeda", "children"),
    [Input(component_id='dropdown_tipo', component_property='value'),
     Input("dataRange","start_date"),Input("dataRange","end_date")]
)
def get_moeda(table,start,end):
    start = start[:10]
    end = end[:10]
    df_exchange = mdata.get_exchange(table,start,end)
    return graficos.grafico_temporal({table:df_exchange[table]},
                                    titulo=table,x_nome='data',y_nome='value')

@app.callback(
    Output("hidden-div", "children"),
    [Input(component_id='dropdown_modelo', component_property='value')]
)
def change_model(model):
    print('Strart Model',model)
    if model == config_model['model']['id']:
        return 
    config_model['model']['id'] = model
    with open(conf_model_path, 'w') as config_model_file:
        yaml.dump(config_model, config_model_file)
    now = datetime.now()
    print('Executando airflow')
    os.environ["AIRFLOW_HOME"] = "~/Documents/Projetos/Claro/Piloto/airflow"
    os.system(f'yes | airflow backfill  claro_industrializacao  -s {str(now)[:10]} --reset_dagruns') 
    #return dcc.Location(href="http://0.0.0.0:8080/admin/airflow/graph?dag_id=claro_industrializacao&execution_date", id="id_airflow")
    return 
    
