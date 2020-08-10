import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import yaml
import gzip
import shutil
import requests

#Path config
data_path = '/root/covid/data/raw/'
config_data_path = '/root/covid/config/data_config.yaml'

#Links download dados
link_brasil_io = 'https://data.brasil.io/dataset/covid19/'

link_casos_full = link_brasil_io + 'caso_full.csv.gz'
link_casos = link_brasil_io + 'caso.csv.gz'
link_boletim = link_brasil_io + 'boletim.csv.gz'
link_obitos = link_brasil_io + 'obito_cartorio.csv.gz'

dict_links = {'casos_full':link_casos_full,'casos':link_casos,
              'boletim':link_boletim,'obitos':link_obitos}
####################################
#Fazendo Download e lendo o csv
####################################
print("Fazendo download do dados:")
dict_df = {} 
for name in dict_links:
    print('\t',name)
    link = dict_links[name]
    filedata = requests.get(link)
    file_path = data_path+name+'.gz'    
    with open(file_path, 'wb') as f:
        f.write(filedata.content)
        df = pd.read_csv(file_path,compression='gzip', header=0, quotechar='"', error_bad_lines=False)
        dict_df[name] = df

####################
#Conectando ao banco
###################
print("Conectando ao banco")
#lendo dados do banco
config_data_file = open(config_data_path)
config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
config_data_file.close()
#salvando em variaveis 
connect_data = config_data['connection']
drive = connect_data['driver']
user = connect_data['user']
passw = connect_data['password']
host = connect_data['host']
port = connect_data['port']
database = connect_data['database']

#Criando engine de conexão
textEngine = f"{drive}://{user}:{passw}@{host}:{port}/{database}"
engine = create_engine(textEngine, echo=False)

##################
#Salvando dados
##################
for name in dict_df:
    print('\t',name)
    df = dict_df[name]
    df.to_sql(name, con=engine, if_exists='replace')
