# Importing Libraries
import os
import sys
from catboost.core import train
from matplotlib.table import CustomCell
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from config.exception import CustomException
from config.logging_config import logging
from src.utilities import save_object, eval_models
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    MODEL_FILE_PATH = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.trainer_config = ModelTrainerConfig()
        
    def inititate_model_training(self, train_arr, test_arr):
        try:
            # Splitting into train - test features and label
            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1], 
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )
            
            # Model list
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            # Hyperparameters of models
            params = {
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2']
                },
                "Random Forest":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            
            # Evaluating models
            logging.info("Creating model report -- initiating")
            model_report : dict = eval_models(X_train, y_train, X_test, y_test, models, params)
            logging.info("Creating model report -- success")
            
            # Finding best model
            logging.info("Finding best model -- initiating")
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("Finding best model -- success")
            
            logging.info("Saving trained model -- initiating")
            save_object(
                file_path = self.trainer_config.MODEL_FILE_PATH,
                obj = best_model
            )
            logging.info("Saving trained model -- success")
            
            y_pred = best_model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            return r2
        
        except Exception as e:
            raise CustomException(e, sys)