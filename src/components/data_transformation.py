# Importing Libraries
import os
import sys
from config.logging_config import logging
from config.exception import CustomException
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utilities import save_object
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    PREPROCESSOR_OBJECT_FILE_PATH = os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self) -> None:
        self.transformation_config = DataTransformationConfig()
        
    def get_preprocessor(self):
        try:
            # Separting numerical and categorical columns
            logging.info("Creating column division -- initiating")
            num_cols = ['writing_score', 'reading_score']
            cat_cols = [
                'gender',
                'lunch',
                'race_ethnicity',
                'parental_level_of_education',
                'test_preparation_course'
            ]
            logging.info(f"Numerical columns: {num_cols}")
            logging.info(f"Categorical columns: {cat_cols}")
            logging.info("Creating column divion -- success")
            
            # Creating numerical pipeline
            logging.info("Setting up pipeline -- initiating")
            num_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='median')),
                    ("scaler", StandardScaler())
                ]
            )
            
            # Creating categorical pipeline
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            logging.info("Setting up pipeline -- success")
            
            # Creating transformer and combining pipelines
            logging.info("Setting up preprocessor -- initiating")
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, num_cols),
                    ('cat_pipeline', cat_pipeline, cat_cols)
                ], 
                remainder = 'passthrough'
            )
            logging.info("Setting up preprocessor -- success")
            
            return preprocessor
                        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Loading dataset
            logging.info("Laoding dataset -- initiating")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Laoding dataset -- success")
            
            # Creating preprocessing object
            logging.info("Calling Function 'get_preprocessor()' -- initiating")
            preprocessor = self.get_preprocessor()
            logging.info("Calling Function 'get_preprocessor()' -- success")
            
            # Splitting data into features and label/target
            target_col = 'math_score'            
            X_train = train_df.drop(columns = [target_col], axis = 1)
            y_train = train_df[target_col]
            X_test = test_df.drop(columns = [target_col], axis = 1)
            y_test = test_df[target_col]
            
            # Fit transform
            logging.info("Fitting Transform -- initiating")
            X_train_arr = preprocessor.fit_transform(X_train)
            X_test_arr = preprocessor.fit_transform(X_test)
            logging.info("Fitting Transform -- success")
            
            # Combining feature and label of train set
            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]
            
            # Saving preprocessor object
            logging.info("Saving preprocessor object -- initiating")
            save_object(
                file_path = self.transformation_config.PREPROCESSOR_OBJECT_FILE_PATH,
                obj = preprocessor
            )
            logging.info("Saving preprocessor object -- success")
            
            return (
                train_arr, 
                test_arr,
                self.transformation_config.PREPROCESSOR_OBJECT_FILE_PATH
            )
            
        except Exception as e:
            raise CustomException(e, sys)