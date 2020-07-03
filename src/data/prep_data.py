#Importando bibliotecas nescessárias 
import pandas as pd 
import yaml
import psycopg2
from sqlalchemy import create_engine
import sys

def tratarReceita(receita):
    if type(receita) == str:
        receita = receita.replace('$','').replace(',','')
        return float(receita)

def func_prep_data(config_data):
    print("Conexão")
    #criando string de conexão
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    
    #lendo dados com pandas
    vendas =  pd.read_sql_table('salesfacts',textEngine)
    products = pd.read_sql_table('products',textEngine)
    geo = pd.read_sql_table('geo',textEngine)
    manufacturer = pd.read_sql_table('manufacturer',textEngine)
    date = pd.read_sql_table('date',textEngine)

    ###################
    # Limpeza
    ###################
    print("Limpeza")
    #Removendo index
    vendas = vendas.drop('index',axis=1)
    #Convertendo receita para numerico
    vendas['revenue'] = vendas['revenue'].apply(tratarReceita)
    #Convertendo date para datetime
    vendas['date'] = pd.to_datetime(vendas['date'],format='%d/%m/%Y %H:%M:%S %p')
    #Trasnformando IsCompeteHide, isVanArsdel e IsCompete em boleanos
    products.isvanarsdel = products.isvanarsdel.apply(lambda x : x == 'Yes') 
    products.iscompete = products.iscompete.apply(lambda x : x == 'Yes') 
    products.iscompetehide = products.iscompetehide.apply(lambda x : x == 'Y')
    #Removendo redundancia
    products = products.drop(['iscompetehide','index'],axis=1)
    #Transformando District em inteiro
    geo.district = geo.district.apply(lambda x : x.split('District #')[1])
    geo.district = geo.district.astype(int)
    #Retirando index
    date = date.drop('index',axis=1)
    #Retirando redundancia
    date = date.drop('month',axis=1) 
    #Transformando quarter em index
    date.quarter = date.quarter.apply(lambda x : x[1]).astype(int)

    ###################
    # Enriquecimento
    ###################
    print("Enriquecimento")
    #fazendo merge
    merge_Produto = pd.merge(vendas,products,on='productid')
    merge_geo = pd.merge(merge_Produto,geo,on='zip')
    master_table = pd.merge(merge_geo,manufacturer,on='manufacturerid')
    #Removendo redundancia
    master_table = master_table.drop('manufacturer_y',axis=1)
    master_table = master_table.rename({'manufacturer_x':'manufacturer'},axis=1)
    #Alterando dados de data
    master_table = master_table.sort_values('date',ascending=False)
    master_table['day'] = master_table.date.dt.day
    master_table['month'] = master_table.date.dt.month
    master_table['year'] = master_table.date.dt.year
    master_table['week_day'] = master_table.date.dt.dayofweek
    #Removendo redundancia novamente
    master_final = master_table.drop(['product','manufacturer','city'],axis=1)
    #Convertendo para dummies 
    master_final = pd.get_dummies(master_final)
    #removendo Nans
    master_final = master_final.dropna()
   
    ###################
    # Reingestão
    ###################
    print("Reingestão")
    engine = create_engine(textEngine, echo=False)
    master_final.to_sql('master_table', con=engine, if_exists='replace',index = False)
    