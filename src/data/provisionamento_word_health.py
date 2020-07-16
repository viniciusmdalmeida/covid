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
link_csv = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'

#Fazendo download csv
filedata = requests.get(link_csv)    
file_path = data_path+'countries_data.csv'
with open(file_path, 'wb') as f:
    f.write(filedata.content)
    df_countrys = pd.read_csv(file_path)
    df_countrys.columns = df_countrys.columns.str.strip()
    df_countrys.columns = df_countrys.columns.str.lower()
    df_countrys.to_sql('countries', con=engine, if_exists='replace')

