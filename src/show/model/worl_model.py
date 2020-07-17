#import pyodbc
import pandas as pd
import numpy as np
import requests
import json
import yaml
from datetime import datetime,date
import country_converter as coco

#Imports para classe abstrada
from abc import ABC, abstractmethod

import sys
src_path = '../../src'
sys.path.append(src_path)
from utils import dag_utils 

class WorlDataAbs(ABC):
    @abstractmethod
    def get_countrys(self):
        pass

    @abstractmethod
    def get_list_dict_countrys(self):
        pass

    @abstractmethod
    def get_deaths_by_country(self,country_code,start,end,cumulative=False):
        pass

    @abstractmethod
    def get_confirmed_by_country(self,country_code,start,end,cumulatfive=False):
        pass


class HerokuApiDada(WorlDataAbs):
    def __init__(self):
        self.link_api = 'https://coronavirus-tracker-api.herokuapp.com/v2/'
        self.p_milhao = False
        self.f_day = False

    def get_countrys(self):
        url = self.link_api+'locations?source=jhu'
        site = requests.get(url)
        try:
            json_data = site.json()
            df_locations = pd.DataFrame(json_data['locations'])
            return df_locations
        except:
            return None
    
    def get_list_dict_countrys(self):
        df_locations = self.get_countrys()
        if df_locations is None:
            return []
        zip_country = zip(df_locations['country_code'].values,df_locations['country'].values)
        list_dict_country = []
        for code,country in zip_country:
            if country == 'Brazil':
                country = 'Brasil'
            list_dict_country.append({'label':country,'value':code})
        #print("List_country",list_dict_country)
        return list_dict_country

    def get_deaths_by_country(self,country_code,start,end,cumulative=False,serie=False):
        url = self.link_api+f'locations?country_code={country_code}&timelines=1'
        site = requests.get(url)
        json_data = site.json()
        data_deaths = json_data['locations'][0]['timelines']['confirmed']['timeline']
        df_deaths = pd.DataFrame(data_deaths.values(),index=data_deaths.keys())
        df_deaths.columns = [country_code]
        df_deaths = df_deaths.set_index(pd.to_datetime(df_deaths.index))
        if serie:
            return df_deaths[country_code]
        else: 
            return df_deaths
        
    def get_confirmed_by_country(self,country_code,start,end,cumulative=False,serie=False):
        url = self.link_api+f'locations?country_code={country_code}&timelines=1'
        site = requests.get(url)
        json_data = site.json()
        data_confirmed = json_data['locations'][0]['timelines']['confirmed']['timeline']
        df_confirmed = pd.DataFrame(data_confirmed.values(),index=data_confirmed.keys())
        df_confirmed.columns = [country_code]
        df_confirmed = df_confirmed.set_index(pd.to_datetime(df_confirmed.index))
        if serie:
            return df_confirmed[country_code]
        else: 
            return df_confirmed


class WorldHealth(WorlDataAbs):
    def __init__(self):
        self.db = dag_utils.Database(connection='connection_world')
        self.p_milhao = False
        self.f_day = False

    def filter_firt_day(self,df,col,reset_index=True):
        first_day = 0
        for index, value in df[col].items():
            if value > 0:
                first_day = value
                break
        first = df[first_day:]
        if reset_index:
            first =  first.reset_index()
        return first
    
    def get_countrys(self):
        query = f"SELECT DISTINCT(country),country_code FROM countries"
        df_countries = self.db.execute_query(query)
        return df_countries

    def get_list_dict_countrys(self):
        df_locations = self.get_countrys().dropna()
        if df_locations is None:
            return [{'label':'','value':''}]
        zip_country = zip(df_locations['country_code'].values,df_locations['country'].values)
        list_dict_country = []
        for code,country in zip_country:
            if country == 'Brazil':
                country = 'Brasil'
            list_dict_country.append({'label':country,'value':code})
        return list_dict_country

    def get_deaths_by_country(self,country_code,start,end,
                              cumulative=False,serie=False,f_day=False,p_milhao=False):
        if f_day:
            start = '2019-12-01'
        query = f"SELECT date_reported,new_deaths FROM countries "\
                f"WHERE country_code='{country_code}' "\
                f"and date_reported BETWEEN '{start}' AND '{end}';"
        df_deaths = self.db.execute_query(query)
        df_deaths.date_reported = pd.to_datetime(df_deaths.date_reported)
        df_deaths = df_deaths.set_index('date_reported')
        df_deaths[df_deaths<0] = 0
        if f_day:
            df_deaths = self.filter_firt_day(df_deaths,'new_deaths')
        if p_milhao:
            query = f"SELECT country_population FROM locations WHERE country_code='{country_code}';"
            populacao = self.db.execute_query(query)['country_population'][0]/1000000
            df_deaths['new_deaths'] = df_deaths['new_deaths']/populacao
        if serie:
            return df_deaths['new_deaths']
        else: 
            return df_deaths

    def get_confirmed_by_country(self,country_code,start,end,
                                 cumulative=False,serie=False,f_day=False,p_milhao=False):
        if f_day:
            start = '2019-12-01'
        query = f"SELECT date_reported,new_cases FROM countries "\
                f"WHERE country_code='{country_code}' "\
                f"and date_reported BETWEEN '{start}' AND '{end}';"
        df_confirmed = self.db.execute_query(query)
        df_confirmed.date_reported = pd.to_datetime(df_confirmed.date_reported)
        df_confirmed = df_confirmed.set_index('date_reported')
        df_confirmed[df_confirmed<0] = 0
        if f_day:
            df_confirmed = self.filter_firt_day(df_confirmed,'new_cases')
        if p_milhao:
            query = f"SELECT country_population FROM locations WHERE country_code='{country_code}';"
            populacao = self.db.execute_query(query)['country_population'][0]/1000000
            df_confirmed['new_cases'] = df_confirmed['new_cases']/populacao
        if serie:
            return df_confirmed['new_cases']
        else: 
            return df_confirmed

    def get_word_data(self,p_milhao,data_col,convert_name=True):
        query = f'SELECT sum({data_col}) as {data_col},country from countries group by country'
        df = self.db.execute_query(query)    
        if p_milhao:
            query = f"SELECT country,country_population FROM locations;"
            populacao = self.db.execute_query(query)
            populacao['country_population'] = populacao['country_population']/1000000
            df = df.merge(populacao, on='country')
            df[data_col] = df[data_col]/df['country_population']    
        df['country'] = coco.convert(names=list(df['country']), to='ISO3')
        return df
        
