# data ingestion rom experimental raw data to ML project

# imports
import pandas as pd
import numpy as np
import chardet
from typing import Annotated, Tuple, NoReturn
from zenml import step
import glob


class DataIngestionEngine:
    """
    DataIngestionEngine is used for data ingestion - various methods as mentioned below

        # get a list of each experimental files
    
        # identify utf type

        # load csv (thermal and electrical)

        # handle date-time cols, basic data cleaning

        # join thermal and electrical data on date-time cols

        # combine all experimental data to create a database
    """

    def __init__(self, data_directory:str='../data/'):
        """
        initialization of the class DataIngestionEngine

        Arg:
            data_directory:str

        Returns:
            None
        """
        self.data_path = data_directory

    def get_list_files(self, name:str='*', ext:str=".csv")->Annotated[list, 'file list']:
        """
        to get a list of experimental files names

        Arg:
            name:str "*"
            ext:str ".csv"

        Return:
            List of experimental file
        """
        self.name = name
        self.ext = ext
        data_filenames_list = glob.glob((self.data_path + self.name + self.ext))

        file_list = []
        for file in data_filenames_list:
            if 'T' in file.split('_'):
                file_list.append(file)
                
        return file_list

        return data_filenames_list
        # df_frames = []
        # for i in data_filenames_list:
        #     df = pd.read_csv(data_filenames_list[i])
        #     df_frames.append(df)
        # df = pd.concat(df_frames, axis=0, ignore_index=True)

    # identify utf type
    def identify_utf_type(self, path)-> Annotated[str, 'UTF-type']:
        """
        to identify UTF type and feed to csv load function.
        for internal calling
        
        args:
            path:str # file path

        use:
            utf_type = identify_utf_type()

        """
        # Detect the encoding
        with open(path, "rb") as file:
            result = chardet.detect(file.read())
            utf_type = result['encoding']
        return utf_type

    # load csv (thermal and electrical)
    def loading_csv_data(self, utf_type:str, path:str)->Tuple[Annotated[pd.DataFrame, 'RAW Data Thermal'],
                                                    Annotated[pd.DataFrame, 'Raw Data Electrical']]:
        """
        to load experimental csv data for each Q[W] heat and Alpha-Beta combinations.

        args:
            utf_type:str # 'UTF-16'
            path:str # file path

        use:
            df = loading_csv_data(utf_type='UTF_16')

        """

        self.path = path
        if 'E' in self.path.split('_')[1]:
            self.path_thermal = self.path.replace('_E_', '_T_')
            self.path_electrical = self.path
        elif 'T' in self.path.split('_')[1]:
            self.path_electrical = self.path.replace('_T_', '_E_')
            self.path_thermal = self.path
        else:
            raise ValueError('### check raw data file name!')
        df_thermal = pd.read_csv(self.path_thermal, encoding=utf_type ,delimiter='\t')
        df_electrical = pd.read_csv(self.path_electrical, encoding=utf_type ,delimiter='\t')
        return df_thermal, df_electrical

    # handle date-time cols, basic data cleaning
    def processing_date_time(self, df:pd.DataFrame, 
                             col:str='date', 
                             format:str='%d/%m/%Y%H:%M:%S')-> Annotated[pd.DataFrame,'Process DateTime col']:
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
    def join_thermal_electrical_df(self, df_thermal:pd.DataFrame, df_electrical:pd.DataFrame) -> Annotated[pd.DataFrame, 'Joined All Experimental Data']:
        """
        to join cleaned thermal and electrical data sets for each set of experiment

        args:
            df_thermal:pd.DataFrame
            df_electrical:pd.DataFrame
        
        return:
            df_joined:pd.DataFrame

        """
        df_join = pd.merge(left=df_thermal, right=df_electrical, on=['date', 'TIME', 'DATE'], how='inner')
        return df_join

    def cleaning_data(self, df_join:pd.DataFrame):
        """
        to clean joined data, drop rows with Nan or 0, removing false entries, etc.

        args:
            df:pd.DataFrame

        returns:
            df:pd.DataFrame
        """

        df_join.rename(columns=lambda x: x.replace('-', '_'), inplace=True)
        df_join.dropna(axis=1, how='all', inplace=True)
        df_join.dropna(axis=0, inplace=True)
        df_join.fillna(0, inplace=True)
        df_join.drop_duplicates(inplace=True)
        return df_join

@step
def step_initialization_DIE(path:str)->Annotated[DataIngestionEngine, 'Data Ingestion Engine']:
    ig = DataIngestionEngine(data_directory=path)
    return ig

@step 
def step_get_file_list(di:DataIngestionEngine)->Annotated[list, 'List of Experimental Files']:
    file_list = di.get_list_files()
    return file_list

@step
def step_data_ingestion(file_list:list, di:DataIngestionEngine)->Tuple[Annotated[pd.DataFrame, 'RAW Data Thermal'],
                                                        Annotated[pd.DataFrame, 'Raw Data Electrical']]:
    df_t = []
    df_e = []
    for file in file_list:
        utf_type = di.identify_utf_type(path=file)
        df_thermal, df_electrical = di.loading_csv_data(utf_type=utf_type, path=file)
        df_t.append(df_thermal)
        df_e.append(df_electrical)
    df_thermal_combined = pd.concat(df_t, ignore_index=True)
    df_electrical_combined = pd.concat(df_e, ignore_index=True)
    return df_thermal_combined, df_electrical_combined

@step
def step_thermal_data_dt_process(df_thermal:pd.DataFrame, di:DataIngestionEngine)->Annotated[pd.DataFrame,'Thermal Data - DT Process']:
    df_ = di.processing_date_time(df=df_thermal)
    return df_

@step
def step_electrical_data_dt_process(df_electrical:pd.DataFrame, di:DataIngestionEngine)->Annotated[pd.DataFrame,'Electrical Data - DT Process']:
    df_ = di.processing_date_time(df=df_electrical)
    return df_

@step
def step_data_join(df_thermal:pd.DataFrame, df_electrical:pd.DataFrame, di:DataIngestionEngine)->Annotated[pd.DataFrame, 'Joined Data']:
    df_join = di.join_thermal_electrical_df(df_thermal=df_thermal, df_electrical=df_electrical)
    return df_join

@step
def step_cleaning_data(df_join:pd.DataFrame, di:DataIngestionEngine)->Annotated[pd.DataFrame, 'Cleaning Joined Data']:
    df_join_clean = di.cleaning_data(df_join=df_join)
    return df_join_clean 