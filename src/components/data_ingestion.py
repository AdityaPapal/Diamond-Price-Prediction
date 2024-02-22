import os 
import sys
import pandas as pd
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split


# Data Configuration
class DataIngestionConfig():
    def __init__(self):
        train_data_path = os.path.join("artifact","train.csv")
        test_data_path = os.path.join("artifact","test.csv")
        row_data_path = os.path.join("artifact","row.csv")

# DataFrame
class DataIngestion():
    def __init__(self):
        self.ingenstion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Strating Data Ingestion')
        try:
            df = pd.read_csv(os.path.join("notebook/cleandata.csv"))
            logging.info("Row Data Reading Complete")
            
            os.makedirs(os.path.dirname(self.ingenstion_config.row_data_path),exist_ok = True)
            df.to_csv(self.ingenstion_config.row_data_path)

            train_set,test_set = train_test_split(df,test_size=0.25,random_state=42)
            logging.info("train test split is Complete")
            
            train_set.to_csv(self.ingenstion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingenstion_config.test_data_path,index=False,header=True)
            logging.info("Data Ingestion is Completed")

            return(
                self.ingenstion_config.train_data_path,
                self.ingenstion_config.test_data_path
            )

        except Exception as ex:
            raise Exception