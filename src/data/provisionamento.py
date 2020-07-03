import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import yaml

#Paths
sale_facts_path = '../../data/raw/salesFacts.csv'
dados_path = '../../data/raw/Dados.xlsx'
config_path = '../../config/data_config.yaml'

####################
#Lendo dados
###################
#read salesFacts
df = pd.read_csv(sale_facts_path,encoding='utf-8',delimiter='\t',index_col=None)
df.head()

#read xlsx
arq = pd.ExcelFile(dados_path)
#read tables in xlsx
products = pd.read_excel(arq,'product',index_col=None)
manufacturer = pd.read_excel(arq,'manufacturer',index_col=None)
geo = pd.read_excel(arq,'geo',index_col=None)
date = pd.read_excel(arq,'date',index_col=None)

####################
#Conectando ao banco
###################
#lendo dados do banco
config_data_file = open(config_path)
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
lista_tabelas = [products,manufacturer,geo,date,df]
lista_nomes = ['products','manufacturer','geo','date','salesfacts']

for cont in range(len(lista_tabelas)):
    print(lista_nomes[cont])
    lista_tabelas[cont].to_sql(lista_nomes[cont], con=engine, if_exists='replace')
