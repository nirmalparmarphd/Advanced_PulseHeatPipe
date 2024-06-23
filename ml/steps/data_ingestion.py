# data ingestion rom experimental raw data to ML project

# imports
import pandas as pd
import numpy as np
import chardet
from typing import Annotated, Tuple, NoReturn
from zenml import step


class DataIngestion:
    """
    DataIngestion is used for various methods as mentioned below

        # identify utf type

        # load csv (thermal and electrical)

        # handle date-time cols, basic data cleaning

        # join thermal and electrical data on date-time cols
    """
    
    def __init__(self, path:str) -> None:

        self.path = path
        if self.path.split('_')[1]=='E':
            self.path_thermal = self.path.replace('_E_', '_T_')
            self.path_electrical = self.path
        elif self.path.split('_')[1]=='T':
            self.path_electrical = self.path.replace('_T_', '_E_')
            self.path_thermal = self.path
        else:
            raise ValueError('### check raw data file name!')
        
    # identify utf type
    def identify_utf_type(self)-> Annotated[str, 'UTF-type']:
        """
        to identify UTF type and feed to csv load function.
        for internal calling
        
        args:
            None

        use:
            utf_type = identify_utf_type()

        """
        # Detect the encoding
        with open(self.path, "rb") as file:
            result = chardet.detect(file.read())
            utf_type = result['encoding']
        
        return utf_type

    # load csv (thermal and electrical)
    def loading_csv_data(self, utf_type:str)->Tuple[Annotated[pd.DataFrame, 'RAW Data Thermal'],
                                                    Annotated[pd.DataFrame, 'Raw Data Electrical']]:
        """
        to load experimental csv data for each Q[W] heat and Alpha-Beta combinations.

        args:
            utf_type:str # 'UTF-16'

        use:
            df = loading_csv_data(utf_type='UTF_16')

        """
        df_thermal = pd.read_csv(self.path_thermal, encoding=utf_type ,delimiter='\t')
        df_electrical = pd.read_csv(self.path_electrical, encoding=utf_type ,delimiter='\t')
        return df_thermal, df_electrical

    # handle date-time cols, basic data cleaning
    def processing_date_time(self, df:pd.DataFrame, col:str='date', format:str='%d/%m/%Y%H:%M:%S')-> Annotated[pd.DataFrame,'Process Data']:
        """
        to process date time cols from row data and returns timestamp col for further analysis

        args:
            df:pd.DataFrame # experimental raw data
            col:str # col name
            format:str # datetime expected format

        use:
            df = processing_date_time(df, col, format)

        """
        df[col] = df['DATE'] + df['TIME']
        df[col] = pd.to_datetime(df[col], format=format)
        return df
    
    # join thermal and electrical data on date-time cols
    def join_thermal_electrical_df(self, df_thermal:pd.DataFrame, df_electrical:pd.DataFrame) -> Annotated[pd.DataFrame, 'Joined Data']:
        """
        to join cleaned thermal and electrical data sets for each set of experiment

        args:

        use:

        """
        df_join = pd.merge(left=df_thermal, right=df_electrical, on=['date', 'TIME', 'DATE'])
        df_join.rename(columns=lambda x: x.replace('-', '_'), inplace=True)
        df_join.dropna(axis=0, how='any', inplace=True)
        df_join.dropna(axis=1, how='all', inplace=True)
        return df_join



@step
def step_data_ingestion(path:str)->Tuple[Annotated[pd.DataFrame, 'RAW Data Thermal'],
                                        Annotated[pd.DataFrame, 'Raw Data Electrical']]:
    di = DataIngestion(path=path)
    utf_type = di.identify_utf_type()
    df_thermal, df_electrical = di.loading_csv_data(utf_type=utf_type)
    return df_thermal, df_electrical

@step
def step_thermal_data_cleaning(path:str, df_thermal:pd.DataFrame)->Annotated[pd.DataFrame,'Cleaned Thermal Data']:
    di = DataIngestion(path=path)
    df_ = di.processing_date_time(df=df_thermal)
    return df_

@step
def step_electrical_data_cleaning(path:str, df_electrical:pd.DataFrame)->Annotated[pd.DataFrame,'Cleaned Electrical Data']:
    di = DataIngestion(path=path)
    df_ = di.processing_date_time(df=df_electrical)
    return df_

@step
def step_data_join(path, df_thermal:pd.DataFrame, df_electrical:pd.DataFrame)->Annotated[pd.DataFrame, 'Joined Data']:
    di = DataIngestion(path=path)
    df_join = di.join_thermal_electrical_df(df_thermal=df_thermal, df_electrical=df_electrical)
    return df_join