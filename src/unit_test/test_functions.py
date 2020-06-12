def test_columns(df,config):
    return list(df.columns)

def test_types(df,config):
    dict_types = dict(df.dtypes) 
    valid_flag = True
    list_column_error = []
    out_dict = {}
    for column in dict_types:
        if 'types' in config and str(dict_types[column]) != config['types'][column]:
            valid_flag = False
            list_column_error.append(column)
        dict_types[column] = str(dict_types[column])
    if valid_flag:
        return dict_types
    else:
        return False
    
def test_null_percent(df,config):
    dict_percent = dict(df.isnull().sum()/len(df))
    if 'min_null' in config:
        for percent in dict_percent.values():
            if percent > config['max_null']:
                return False
    return dict_percent

def test_n_uniques(df,config):
    return dict(df.nunique())

def test_category_percent(df,config):
    count = 0
    for type_table in df.dtypes:
        for cat_type in config['cat_types']:
            if str(type_table) == cat_type:
                count += 1
                break
    return count/len(df.columns)

