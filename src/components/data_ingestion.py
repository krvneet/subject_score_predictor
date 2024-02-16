# Importing Libraries
import warnings
warnings.filterwarnings('ignore')
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from config.logging_config import logging
from config.exception import CustomException
from src.components.data_transformation import DataTransformation
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    RAW_DATA_PATH : str = os.path.join('artifacts', 'raw.csv')
    TRAIN_DATA_PATH : str = os.path.join('artifacts', 'train.csv')
    TEST_DATA_PATH : str = os.path.join('artifacts', 'test.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Initiated data ingestion -- 'initiate_data_ingestion()' function triggered")
        try:
            # Reading the dataset
            PATH  = os.path.join('data', 'student.csv')
            logging.info("Reading the dataset -- initiating")
            df = pd.read_csv(PATH)
            logging.info("Reading the dataset -- success")
            
            # Saving raw data
            os.makedirs(os.path.dirname(self.ingestion_config.TRAIN_DATA_PATH), exist_ok=True)
            df.to_csv(self.ingestion_config.RAW_DATA_PATH, index=False, header=True)
            
            # Initiating train test split & saving train and test data
            logging.info("Train Test Split -- initiating")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state = 42)
            train_set.to_csv(self.ingestion_config.TRAIN_DATA_PATH, index = False, header = True)
            test_set.to_csv(self.ingestion_config.TEST_DATA_PATH, index = False, header = True)
            logging.info("Train Test Split -- successs")
            
            logging.info("Data ingestion completed")
            return (self.ingestion_config.TRAIN_DATA_PATH, self.ingestion_config.TEST_DATA_PATH)
        
        except Exception as e:
            raise CustomException(e, sys)
        
# Testing Code
# if __name__ == "__main__":
#     obj = DataIngestion()
#     train_data, test_data = obj.initiate_data_ingestion()
    # data_transformation = DataTransformation()
    # train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)