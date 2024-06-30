# data selection from cleaned experimental data and prepare for further data analysis and ML

import pandas as pd
import sys, os
from typing import Annotated, Tuple
from zenml import step

class DataProcessingEngine:
    """
    Data Processing Engine is used for various data processing related steps

    # loading meta table

    # slicing data as per meta table and make a experimental database

    # data standardization

    # processing categorical data

    
    """
    def __init__(self, dir_path: str):
        """
        to initialize data processing engine

        args:
            dir_path: str '../data/'

        returns:
            None
        """
        self.dir_path = dir_path

    def load_meta_table(self, file_name: str='meta_table_data.csv'):
        """
        to load meta table that contain information of the all experimental data

        args:
            file_name: str

        returns:
            df: pd.DataFrame
        """
        meta_table_path = self.dir_path + file_name
        df = pd.read_csv(meta_table_path)

        # basic cleaning
        df.dropna(thresh=9, inplace=True)
        df.drop_duplicates(inplace=True)
        return df
    
    def processing_date_time(self, df:pd.DataFrame, 
                             col:str,
                             col_date:str,
                             col_time:str, 
                             format:str='%d/%m/%Y%H:%M:%S')-> Annotated[pd.DataFrame,'Process DateTime col']:
        """
        to process date time cols from row data and returns timestamp col for further analysis

        args:
            df:pd.DataFrame # experimental raw data
            col:str # col name output
            col_date:str
            col_time:str
            format:str # datetime expected format

        use:
            df = processing_date_time(df, col, format)

        """
        df[col] = df[col_date] + df[col_time]
        df[col] = pd.to_datetime(df[col], format=format)
        return df
    
    def data_slicing_combine(self, 
                             df_meta:pd.DataFrame, 
                            df_raw_data:pd.DataFrame,
                            col_start:str='dt_start',
                            col_stop:str='dt_stop'):
        """
        to slice data from the clean experimental combined data

        args:
            df_meta: pd.DataFrame
            df_raw_data: pd.DataFrame
            col_start:str,
            col_stop:str

        returns:
            pd.DataFrame
        """
        df_raw_data.set_index('date', inplace=True)

        frames = []
        for _ , row in df_meta.iterrows():
            experiment_start = row[col_start]
            experiment_stop = row[col_stop]
            df_sd = df_raw_data.loc[experiment_start: experiment_stop]
            df_sd['WF'] = row['WF']
            df_sd['FR[%]'] = row['FR [%]']
            df_sd['Q[W]'] = row['Q [W]']
            df_sd['alpha'] = row['alpha']
            df_sd['beta'] = row['beta']
            frames.append(df_sd)
            
        df_database = pd.concat(frames, ignore_index=True)
        df_raw_data.reset_index(inplace=True)

        return df_database
    
    def database_to_csv(self, df_database:pd.DataFrame, op_path:str):
        """
        to save database to csv (local)

        args:
            df_database: pd.DataFrame
            op_path: str

        returns:
            csv
        """
        # Directory and file path
        directory = os.path.join(op_path, 'database')
        file_path = os.path.join(op_path, directory, 'database.csv')

        # Check if directory exists and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the DataFrame to a CSV file in the specified directory
        df_database.to_csv(file_path, index=False)
        return None


@step
def step_initialize_DPE(dir_path:str)->Annotated[DataProcessingEngine, 'Data Processing Engine']:
    dpe = DataProcessingEngine(dir_path=dir_path)
    return dpe


@step
def step_loading_meta_table(dpe:DataProcessingEngine)->Annotated[pd.DataFrame, 'Meta Table Loaded']:
    df_meta = dpe.load_meta_table(file_name='meta_table_data.csv')
    return df_meta

@step
def step_meta_data_dt_process(dpe:DataProcessingEngine, 
                              df_meta:pd.DataFrame)->Annotated[pd.DataFrame, 'Meta Table - DT Processed']:
    df_meta_processed = dpe.processing_date_time(df=df_meta, col='dt_start', col_date='Date', col_time='t_start', format='%d-%m-%Y%H:%M:%S')
    df_meta_processed = dpe.processing_date_time(df=df_meta, col='dt_stop', col_date='Date', col_time='t_end', format='%d-%m-%Y%H:%M:%S')
    return df_meta_processed

@step
def step_database(dpe:DataProcessingEngine,
                  df_meta:pd.DataFrame,
                  df_raw:pd.DataFrame)->Annotated[pd.DataFrame, 'Experimental DataBase']:
    df_database = dpe.data_slicing_combine(df_meta=df_meta, df_raw_data=df_raw, col_start='dt_start', col_stop='dt_stop')
    return df_database

@step
def step_database_csv(dpe:DataProcessingEngine,
                      df_database:pd.DataFrame)->Annotated[None, 'Saved CSV locally']:
    dpe.database_to_csv(df_database=df_database, op_path=dpe.dir_path)
    return None