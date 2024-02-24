import sys
import os
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_model

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file = os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation Initiated')

            #Define which Colums should be ordinal-encoding and which should be scaled
            categorical_cols = ['cut','color','clearity']
            numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']

            # Define the custom ranking for each ordinal variable
            cut_categorie = ['Fair','Good','Very Good','Premium','Ideal']
            color_categorie = ['D','E','F','G','H','I','J']
            clearity_categorie = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']


            logging.info("Pipeline Initiated")

            # Numerical Pipeline 
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler()),
                ]
            )


            # Categorical Pipeline 
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoding',OrdinalEncoder(categories=[cut_categorie,color_categorie,clearity_categorie])),
                ]
            )
            

            # Preprocessing 
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_cols),
                    ('cat_pipeline',cat_pipeline,categorical_cols)
                ]
            )
            return preprocessor

            logging.info('Pipeline Compeleted')


        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)
        

    def initaite_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data Completed")
            logging.info(f"Train Dataframe Head : \n{train_df.head().to_string()}")
            logging.info(f"Test Dataframe Head : \n{test_df.head().to_string()}")

            logging.info("obtaining Preprocessing Object")

            preprocessing_obj = self.get_data_transformation_object()
            
            target_column_name = "Price"
            drop_colums = [target_column_name,'id']

            input_feature_train_df = train_df.drop(columns=drop_colums,axis=1)
            target_feature_train_df = train_df[target_column_name]
                    
            input_feature_test_df = test_df.drop(columns=drop_colums,axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Transformation using preporcessor obj
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)


            logging.info("Apply preprocessing object on traing and testing datasets.")

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr =np.c_[input_feature_test_arr,np.array(target_feature_test_df)]


            save_model(

                file_path=self.data_transformation_config.preprocessor_obj_file,
                obj=preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file,
            )

        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise CustomException(e,sys) 