#Importando bibliotecas nescessárias 
import pandas as pd 
import yaml
import psycopg2
from sqlalchemy import create_engine
from .test_functions import *
import os
import sys
    

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
                

def unit_test(config_data,config_test):
    print("Iniciando tests...")
    output_path = config_test['output']['path']
    #Criando string de conexão
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    #criando lista de tests
    list_all_tests_func = []
    for test_func in config_test['tests']:
        list_all_tests_func.append(eval(test_func))
    #lendo tabelas
    out_data = {} #dicionario de testes das tabelas
    for table_name in config_data['tables']:
        print(f"Tabela {table_name}")
        df = pd.read_sql_table(table_name,textEngine)    
        test_table = {} 
        #Criando lista de teste para a tabela
        if config_test['tables'][table_name]['tests'] == 'all':
            list_tests_func = list_all_tests_func
        else:
            list_tests_func = []
            for test_func in table_name['tests']:
                list_tests_func.append(eval(test_func))
        #Executando as funções de testes
        for function in list_tests_func:
            name_test = function.__name__
            retorno = function(df,config_test['tables'][table_name])
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
    print(f"\nTestes finalizados, salvos em:\n {output_path}\n")