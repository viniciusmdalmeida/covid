#Importando bibliotecas nescessárias 
import pandas as pd 
from datetime import datetime

#import para get_exchange
import requests 
import numpy as np
import json
from sqlalchemy import create_engine

def get_base(config_data,name):
    return 

def get_exchange(config_data,name):
    #get config data
    config_exchange = config_data['get_data'][name]
    base = config_exchange['paramns']['base']
    symbol= config_exchange['paramns']['symbol']
    start_date = config_exchange['paramns']['start_date']
    end_date = config_exchange['paramns']['end_date']
    print(f"get value {base} to {symbol}")
    #acess api
    base_url = 'https://api.exchangeratesapi.io/history'
    url = f'{base_url}?start_at={start_date}&end_at={end_date}&symbols={symbol}&base={base}'
    print("URL:",url)
    #read data
    site = requests.get(url)
    json_data = site.json()
    #create Df
    data = pd.DataFrame.from_dict(json_data['rates'],orient='index')
    data.columns = [f'{base.lower()}_{symbol.lower()}']
    #save data
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    engine = create_engine(textEngine, echo=False)
    data.to_sql(f'{base.lower()}_{symbol.lower()}', con=engine, if_exists='replace')
    print("Get data finished")

def get_pib(config_data):
    return 
    