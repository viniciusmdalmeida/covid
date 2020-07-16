import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import yaml
import gzip
import shutil
import requests

#Path config
data_path = '../../../data/raw/'
config_data_path = '../../config/data_config.yaml'
dict_df = {}


####################
#Conectando ao banco
###################
print("Conectando ao banco")
#lendo dados do banco
config_data_file = open(config_data_path)
config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
config_data_file.close()
#salvando em variaveis 
connect_data = config_data['connection_world']
drive = connect_data['driver']
user = connect_data['user']
passw = connect_data['password']
host = connect_data['host']
port = connect_data['port']
database = connect_data['database']
#Criando engine de conexão
textEngine = f"{drive}://{user}:{passw}@{host}:{port}/{database}"
engine = create_engine(textEngine, echo=False)

######################################
# Buscando dados da API Herokuapp
###########3##########################
#Links download dados
link_api = 'https://coronavirus-tracker-api.herokuapp.com/v2/'

#Pegando paises
url = link_api+'locations?source=jhu'
site = requests.get(url)
json_data = site.json()
df_locations = pd.DataFrame(json_data['locations'])
for column in df_locations:
    if df_locations[column].dtype == 'O':
        df_locations[column] = df_locations[column].astype(str)
df_locations.to_sql('locations', con=engine, if_exists='replace')
print('Locations')
#Pegando dados de morte covid
df_deaths = {}
first = True
for country_code in df_locations['country_code'].values:
    print("deaths:",country_code)
    url = link_api+f'locations?country_code={country_code}&timelines=1'
    site = requests.get(url)
    json_data = site.json()
    data_deaths = json_data['locations'][0]['timelines']['confirmed']['timeline']
    df_deaths_country = pd.DataFrame(data_deaths.values(),index=data_deaths.keys())
    df_deaths_country.columns = [country_code]
    df_deaths_country = df_deaths_country.set_index(pd.to_datetime(df_deaths.index))
    if first:
        df_deaths_country.to_sql('deaths', con=engine, if_exists='replace')
        first = False
    else:
        df_deaths_country.to_sql('deaths', con=engine, if_exists='append')


#Pegando dados de contaminados covid
first = True
for countcountry_codery in df_locations['country_code'].values:
    print("confirmed:",country_code)
    url = link_api+f'locations?country_code={country_code}&timelines=1'
    site = requests.get(url)
    json_data = site.json()
    data_confirmed = json_data['locations'][0]['timelines']['confirmed']['timeline']
    df_confirmed_country = pd.DataFrame(data_confirmed.values(),index=data_confirmed.keys())
    df_confirmed_country.columns = [country_code]
    df_confirmed_country = df_confirmed_country.set_index(pd.to_datetime(df_confirmed.index))
    if first:
        df_confirmed_country.to_sql('deaths', con=engine, if_exists='replace')
        first = False
    else:
        df_confirmed_country.to_sql('deaths', con=engine, if_exists='append')
