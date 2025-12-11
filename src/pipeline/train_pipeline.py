import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging


def run_training_pipeline():
    """
    Execute the full training workflow:
    1) Ingest raw data and perform train/test split.
    2) Transform data (imputation, encoding, scaling).
    3) Train and select the best regression model.

    Returns
    -------
    float
        R² score of the best model on the test set.
    """
    try:
        logging.info("Starting training pipeline")

        # 1) Data ingestion
        ingestion = DataIngestion()
        train_path, test_path = ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion completed: train={train_path}, test={test_path}")

        # 2) Data transformation
        transformer = DataTransformation()
        train_arr, test_arr, _ = transformer.initiate_data_transformation(
            train_path, test_path
        )
        logging.info("Data transformation completed")

        # 3) Model training
        trainer = ModelTrainer()
        r2_score = trainer.initiate_model_trainer(train_arr, test_arr)
        logging.info(f"Training completed with R2 score: {r2_score}")

        return r2_score

    except Exception as e:
        # Convert to CustomException for consistent error handling/logging
        raise CustomException(e, sys)


if __name__ == "__main__":
    score = run_training_pipeline()
    print(f"Training complete. Best model R2 score: {score}")
