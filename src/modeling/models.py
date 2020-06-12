#modelos
#Modelos de regressão Sklearn
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

#Imports para classe abstrada
from abc import ABC, abstractmethod
 

class AbstractModel(ABC):
    @abstractmethod
    def fit(self, X, y):
        pass
    
    @abstractmethod
    def predict(self, X):
        return self._decision_function(X)
    
class ConcretModel(AbstractModel):
    def fit(self,x,y):
        pass
    
    def predict(self,x):
        pass