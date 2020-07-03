import pandas as pd 
from datetime import datetime
import pickle
from utils.dag_utils import *

#modelos 
def read_model(config_model,config_data):
    model_path = config_model['model']['models_path']
    model_id = config_model['model']['id']
    file_path = f"{model_path}/{model_id}/model.pkl"
    with open(file_path, 'rb') as f:
        unpickler = pickle.Unpickler(f)
        model = unpickler.load()
        if config_model['model']['retrain'] != False:
            return retrain(model,config_model,config_data)
        return model 
    
def retrain(model,config_model,config_data):
    print("Retrain")
    end_data = config_model['model']['retrain']['paramns']['end_data']
    data = read_master(config_data,where=f"date < '{end_data}'")
    y_column = config_model['model']['retrain']['paramns']['target']
    print('Columna:',data.columns)
    X = data.drop([y_column,'date'],axis=1)
    model.fit(X,data[y_column])
    return model