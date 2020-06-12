#Importando bibliotecas nescessárias 
import pandas as pd 
import yaml
import psycopg2
from sqlalchemy import create_engine
from test_functions import *
import os

import json

def conver_json(data):
    if type(data) != dict and type(data) != list:
        return str(data)
    else:
        if type(data) == dict:
            for key in data:
                data[key] = conver_json(data[key])
        elif type(data) == list:
            for cont in range(len(data)):
                data[cont] = conver_json(data[cont])
    return data
                

if __name__ == '__main__':
    print("Iniciando tests...")
    
    #variavelis globais 
    config_path = "/home/vinicius/Documents/Projetos/Claro/Piloto/git_Homologação/config"
    data_config_path = f"{config_path}/data_config.yaml"
    test_config_path = f"{config_path}/unit_test_config.yaml"
    output_path = "../test_out.json"
    actual_path = os.path.dirname(os.path.abspath('.'))
    
    #Lendo configurações dos dados
    config_file = open(data_config_path)
    config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()

    #Lendo configurações de test
    test_file = open(test_config_path)
    config_test = yaml.load(test_file, Loader=yaml.FullLoader)
    test_file.close()

    #Criando string de conexão
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"

    #lendo tabelas
    out_data = {} #dicionario de testes das tabelas
    for table_name in config_data['tables']:
        print(f"Tabela {table_name}")
        df = pd.read_sql_table(table_name,textEngine)    
        list_functions = [test_columns,test_types,test_null_percent,test_n_uniques,test_category_percent]
        test_table = {} 
        for function in list_functions:
            name_test = function.__name__
            retorno = function(df,config_test[table_name])
            test_table[name_test] = retorno
        out_data[table_name] = test_table

    #Salvando saida
    try:
        with open(output_path, 'w') as outfile:
            json.dump(out_data, outfile, indent=2)
            print("normal")
    except TypeError as error:
        with open(output_path, 'w') as outfile:
            json.dump(conver_json(out_data), outfile, indent=2)
            print('convert_json')
    except Exception as e:
        print(e)
    print(f"\nTestes finalizados, salvos em:\n{actual_path}/{output_path.replace('../','').replace('..','')}\n")
