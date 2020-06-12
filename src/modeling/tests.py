from sklearn import model_selection
import pandas as pd

def cross_validate(model,X,y,config):
    scoring = config['scoring']
    cv = config['cv']
    #make test
    score = model_selection.cross_validate(model, X, y, scoring=scoring,cv=cv)
    score_df = pd.DataFrame(score)
    #calc operation
    dict_score = score_df.apply(config['operation']).to_dict()
    return dict_score