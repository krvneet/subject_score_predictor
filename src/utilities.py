# Importing Libraries
import os
import sys
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from config.exception import CustomException
from config.logging_config import logging

# Function to save objects as pickle file
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        logging.info("Saving object as pickle file -- initiating")
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Saving object as pickle file -- success")

    except Exception as e:
        raise CustomException(e, sys)

# Function to evaluate performance of models
def eval_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        logging.info("Evaluating all models -- initiating")
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            
            # Applying grid search over all params
            gs = GridSearchCV(model, param, cv = 3)
            gs.fit(X_train, y_train)
            
            # Training model over best params found
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Finding r2 score of best model
            test_model_score = r2_score(y_test, y_pred)
            report[list(models.keys())[i]] = test_model_score
            
        logging.info("Evaluating all models -- success")    
        return report
            
    except Exception as e:
        raise CustomException(e, sys)
    
# Function to load objects from pickle file
def load_object(file_path):
    try:
        logging.info("Loading pickle object file -- initiating")
        with open(file_path, "rb") as file_obj:
            logging.info("Loading pickle object file -- success")
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)