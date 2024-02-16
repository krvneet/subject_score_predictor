# Importing Libraries
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

# Main/Driver Function
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)
    model_trainer = ModelTrainer()
    print(f"Best Model Accuracy (r2 Score) is {(model_trainer.inititate_model_training(train_arr, test_arr)):.2f}")