def prep_data(master_table,config):
    #removendo index
    master_table = master_table.drop('index',axis=1)

    #pegando amostra dos dados
    percent_sample = config['percent_sample']
    ponto_corte = int(len(master_table)*percent_sample)
    master_part = master_table[:ponto_corte]

    #retirando nan
    master_part = master_part.dropna()
    
    #Separando X e y
    y = master_part['Revenue']
    X = master_part.drop(['Revenue'],axis=1)
    
    return X,y
    