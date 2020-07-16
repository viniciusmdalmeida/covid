#Importando bibliotecas nescessárias 
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import yaml

class DashVariables:
    """Class to store information useful to callbacks"""
    def __init__(self):
        self.attr = {}

    def update_attr(self, value, attr):
        self.attr[attr] = value

class Database:
    def __init__(self,connection='connection'):
        self.connection=connection

    def connect(self,config_data=None):
        if config_data is None:
            project_path = '../..'
            conf_path = f'{project_path}/config'
            conf_data_path = f'{conf_path}/data_config.yaml'
            config_data_file = open(conf_data_path)
            config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
            config_data_file.close()
        #Conectando com os dados
        connect_data = config_data[self.connection]
        connect_string = f"{connect_data['driver']}://{connect_data['user']}:"\
                     f"{connect_data['password']}@{connect_data['host']}:"\
                     f"{connect_data['port']}/{connect_data['database']}"
        self.cnxn = create_engine(connect_string)

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

