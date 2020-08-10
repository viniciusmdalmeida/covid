#import pyodbc
import pandas as pd
import numpy as np
import requests
import json
import yaml
from datetime import datetime,date

import sys
src_path = '../../src'
sys.path.append(src_path)
from utils import dag_utils 

class BrasilDada():
    def __init__(self,config_data_path='../..'):
        self.db = dag_utils.Database(project_path=config_data_path)

    def getIndex(self,valor):
        self.place_type = 'city'
        return datetime.strftime(valor, '%Y/%m')


    def fix_df(self,df):
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.sort_index()
        for col in df:
            if len(df[col]) > 0 and df[col].iloc[-1]==0:
                df = df[:-1]
        return df

    def get_state(self,city):
        query = f"select distinct(state) from casos where city ='{city}'"
        df_state = self.db.execute_query(query)
        return df_state.iloc[0].values[0]

    def get_total_mortes(self,city,start,end):
        query = f"SELECT sum(new_deaths) FROM casos_full WHERE {self.place_type} = '{city}' and date BETWEEN '{start}' AND '{end}'"
        sum_value = self.db.execute_query(query)
        return str(sum_value.iloc[0].values[0])

    def get_total_casos(self,city,start,end):
        query = f"SELECT sum(new_confirmed) FROM casos_full WHERE {self.place_type} = '{city}' and date BETWEEN '{start}' AND '{end}'"
        sum_value = self.db.execute_query(query)
        return str(sum_value.iloc[0].values[0])
    
    def calc_status(self,city,start,end,column='new_deaths',period=14):
        df_mortes = self.get_mortes_time(city,start,end)['sum']
        df_moving_avg = df_mortes.rolling(window=7).mean()
        last_day = df_moving_avg[-1]
        period = df_moving_avg[-period]
        value = last_day/period
        if last_day < 5 and period < 5:
            return f'Estavel'
        if value > 1.15:
            return f'Subindo {(value - 1)*100:.0f}%'
        if value < 0.85:
            return f'Caindo {(value - 1)*100:.0f}%'
        else:
            return f'Estavel {(value - 1)*100:.0f}%'

    def get_casos_time(self,city,start,end,cumulative=False):
        query = f"SELECT date,sum(new_confirmed) FROM casos_full WHERE {self.place_type} = '{city}' and date BETWEEN '{start}' AND '{end}' GROUP BY date"
        df_casos = self.db.execute_query(query)
        df_casos = self.fix_df(df_casos)
        if cumulative:
            df_casos['sum'] = df_casos['sum'].cumsum()
        return df_casos
    
    def get_mortes_time(self,city,start,end,cumulative=False):
        query = f"SELECT date,sum(new_deaths) FROM casos_full WHERE {self.place_type} = '{city}' and date BETWEEN '{start}' AND '{end}' GROUP BY date"
        df_mortes = self.db.execute_query(query)
        df_mortes = self.fix_df(df_mortes)
        if cumulative:
            df_mortes['sum']  = df_mortes['sum'].cumsum()
        return df_mortes

    def calc_moving_average(self,column,city,start,end):
        query =  f"select date,cast(avg({column}) as int) "\
            f"over(order by date asc rows between 7 preceding and current row) "\
            f"from casos_full where {self.place_type} = '{city}';"
        df_moving = self.db.execute_query(query)
        df_moving = self.fix_df(df_moving)
        data_zeros = 0
        for data in reversed(df_moving['avg']):
            if data == 0:
                data_zeros +=1
            else:
                break
        return df_moving['avg'][:-data_zeros]
    
    def get_option_place(self,place_type='city'):
        query = f"SELECT DISTINCT {place_type} FROM casos_full WHERE place_type = '{place_type}'"
        self.place_type = place_type
        df_places = self.db.execute_query(query)
        list_option = []
        for value in df_places[self.place_type].values:
            list_option.append({'label':value,'value':value})
        return list_option
    
    def get_obitos(self,state,start,end,year):
        query = f"SELECT * FROM obitos WHERE state = '{state}'"
        df_obitos = self.db.execute_query(query)
        colunas = [x for x in df_obitos.columns if year in x and 'new' in x]
        colunas.append('date')
        df_obitos = df_obitos[colunas]
        df_obitos = df_obitos.set_index(f'date')
        #df_obitos = df_obitos.groupby(f'epidemiological_week_{year}').mean()
        df_obitos.columns = [x.split('_')[-2] for x in df_obitos.columns]
        return df_obitos

    def get_interiorizacao(self,state,star,end):
        query = f"SELECT * FROM obitos WHERE state = '{state}'"
        df_obitos = self.db.execute_query(query)
        return

