#Importando bibliotecas nescessárias 
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import yaml


def read_master(config_data,where=None):
    #Conectando com os dados
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    #Lendo dados em pandas
    if where is None:
        master_table = pd.read_sql_table('master_table',textEngine)
    else:
        query = f"select * from master_table where {where}"
        master_table = pd.read_sql_query(query,textEngine)
    return master_table

class Database:

    def connect(self,config_data=None):
        if config_data is None:
            project_path = '/home/vinicius/Documents/Projetos/Claro/Piloto/industrializacao'
            conf_path = f'{project_path}/config'
            conf_data_path = f'{conf_path}/data_config.yaml'
            config_data_file = open(conf_data_path)
            config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
            config_data_file.close()
        #Conectando com os dados
        connect_data = config_data['connection']
        connect_string = f"{connect_data['driver']}://{connect_data['user']}:"\
                     f"{connect_data['password']}@{connect_data['host']}:"\
                     f"{connect_data['port']}/{connect_data['database']}"
        self.cnxn = create_engine(connect_string)

    def read_master(self,where):
        if where is None:
            master_table = self.get_table('master_table')
            master_table = master_table.drop('date',axis=1)
        else:
            query = f"select * from master_table where {where}"
            master_table = self.select_query(query)
            master_table = master_table.drop('date',axis=1)
        return master_table

    def disconncet(self):
        pass

    def get_table(self,table):
        self.connect()
        query = "select * from {}".format(table)
        out = pd.read_sql(query, self.cnxn)
        self.disconncet()
        return out

    def execute_query(self,query):
        self.connect()
        out = pd.read_sql(query, self.cnxn)
        self.disconncet()
        return out

