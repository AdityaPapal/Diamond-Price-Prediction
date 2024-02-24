import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
 

# Data Configuration
class DataIngestionConfig():
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    row_data_path = os.path.join("artifacts","row.csv")

# DataFrame
class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Strating Data Ingestion')
        try:
            df = pd.read_csv(os.path.join("notebook/cleandata.csv"))
            logging.info("Row Data Reading Complete")
            
            os.makedirs(os.path.dirname(self.ingestion_config.row_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.row_data_path)

            train_set,test_set = train_test_split(df,test_size=0.25,random_state=42)
            logging.info("train test split is Complete")
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Data Ingestion is Completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    data_ingestion = DataIngestion()
    data_ingestion.initiate_data_ingestion()
