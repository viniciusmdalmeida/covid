from datetime import datetime
import json
import pandas as pd
from sqlalchemy import create_engine
#mlflow
import mlflow
import mlflow.sklearn

def save_predict(df_predict,config_data):
    #criando string de conexão
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    engine = create_engine(textEngine, echo=False)
    df_predict.to_sql('predict', con=engine, if_exists='replace')

def save_csv(model,result,config_model,model_name):
    output_dict = {}
    out_type = config_model['save']['type'] 
    data_path = config_model['save']['path']
    if out_type == 'normal':
        output_table = pd.concat(result, axis=1, keys=config_model["models"].keys())
    else:
        out_list = []
        for result in result: 
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

def save_mlflow(model,result,config_model,model_name):
    print("Salvando dados no mlflow")
    data_path = config_model['save']['path']
    mlflow.set_tracking_uri(data_path+'/mlruns')
    #Salvando dados no mlflow
    experiment_id = mlflow.set_experiment(config_model['experiment_name']) 
    run_name = model_name
    mlflow.start_run(run_name=run_name)
    model_id = mlflow.active_run().info.run_id
    paramns = model.get_params()
    #Salvando metricas
    mlflow.log_params(paramns)
    #Colocando metricas no mlflow
    for column in result:
        mlflow.log_metric(column,result[column])
    mlflow.set_tag('type',model.__class__.__name__)
    mlflow.sklearn.save_model(model,f"{data_path}/model/{str(model_id)}")
    mlflow.sklearn.log_model(model,f"model/{str(model_id)}_log")
    mlflow.end_run()    
