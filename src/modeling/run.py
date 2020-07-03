#Importando bibliotecas nescessárias 
import pandas as pd 
from datetime import datetime
import pickle

#Biliotecas internas
import os
os.chdir(os.path.dirname(__file__))
import sys
src_path = '../../src'
sys.path.append(src_path)
from modeling.test import *
from modeling.save import *
from modeling.model import *
from utils.dag_utils import *

def run_model(config_model,config_data):
    #get data
    start_date = config_data['prep_data']['start_predict']
    X = read_master(config_data,where=f"date > '{start_date}'")
    X = X.drop('revenue',axis=1)
    #get model
    print("read model")
    model = read_model(config_model,config_data)
    #predict
    print("Predict data")
    list_predict = model.predict(X.drop('date',axis=1))
    df_predict = pd.DataFrame(list_predict,index=X.date)
    #save predict
    save_func = eval(config_model['predict']['save_func'])
    save_func(df_predict,config_data)
    #teste
    print("test old prediction")
    test_func = eval(config_model['test']['test_func'])
    test_func(df_predict,config_data,config_model)
    