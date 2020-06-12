#Importando bibliotecas nescessárias 
import pandas as pd 
import yaml
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
import json
#mlflow
import mlflow
import mlflow.sklearn
#internas
from models import *
from prep_data import *
from tests import *

def save_mlflow(model,result,config_model,model_name):
    data_path = config_model['model_output']['path']
    mlflow.set_tracking_uri(data_path+'/mlruns')
    
    #Salvando dados no mlflow
    experiment_id = mlflow.set_experiment(config_model['experiment_name']) 
    run_name = model_name
    mlflow.start_run(run_name=run_name)
    model_id = mlflow.active_run().info.run_id
    #Salvando metricas
    mlflow.log_params(paramns)
    #Colocando metricas no mlflow
    for column in result:
        mlflow.log_metric(column,result[column])
    mlflow.set_tag('type',model.__class__.__name__)
    mlflow.sklearn.save_model(model,f"{data_path}/model/{str(model_id)}")
    mlflow.sklearn.log_model(model,f"model/{str(model_id)}_log")
    mlflow.end_run()

def save_output(config_model,list_result,output_dict):
    out_type = config_model['model_output']['type'] 
    data_path = config_model['model_output']['path']
    if out_type == 'normal':
        output_table = pd.concat(list_result, axis=1, keys=config_model["models"].keys())
    else:
        out_list = []
        for result in list_result: 
            out_list.append(result)

        output_table = pd.DataFrame(out_list,index=config_model["models"].keys())

    #save table
    time_stamp_id = str(int(datetime.now().timestamp()))[-5:]
    output_table_name = f"model_output_{time_stamp_id}.csv"
    output_table.to_csv(f"{data_path}/output/{output_table_name}")
    print(f"Tabela salva em {data_path}/output/{output_table_name}")

    #save dict
    output_dict['table_path'] = f"{data_path}/output/{output_table_name}"
    with open(f'{data_path}/output/output_dict.json', 'w') as outfile:
        json.dump(output_dict, outfile, indent=2)
    print(f"dados dos modelos salvos em {data_path}/output/{output_table_name}")

    
#Paths
conf_path = '/home/vinicius/Documents/Projetos/Claro/Piloto/git_Homologação/config'
conf_data_path = f'{conf_path}/data_config.yaml'
conf_model_path = f'{conf_path}/model_config.yaml'

#Lendo arquivos de configuração
config_data_file = open(conf_data_path)
config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
config_data_file.close()

#Lendo arquivos de configuração
config_model_file = open(conf_model_path)
config_model = yaml.load(config_model_file, Loader=yaml.FullLoader)
config_model_file.close()

#Conectando com os dados
connect_data = config_data['connection']
textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"

#Lendo dados em pandas
master_table = pd.read_sql_table('master_table',textEngine)

#PrepData 
X,y = prep_data(master_table,config_model['prep_data'])

#Rodando modelos
output_dict = {}


list_result  = []
for model_name in config_model['models'] :
    model_dict = config_model['models'][model_name]
    print(f"Treinando modelo {model_name}")
    #Iniciando o modelo (buscado a classe com eval e iniciando os parametros)
    model_class = eval(model_dict['class'])
    paramns = model_dict['params']
    model = model_class(**paramns)
    #Fazendo teste 
    test_func = eval(config_model['test']['func'])
    result = test_func(model,X,y,config_model['test'])
    list_result.append(result)
    #Save files
    output_dict[model_name] = model.get_params()
    save_mlflow(model,result,config_model,model_name)
    
    
save_output(config_model,list_result,output_dict)
