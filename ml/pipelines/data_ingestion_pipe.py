from zenml import pipeline
# imports
import pandas as pd
import numpy as np
import chardet
from typing import Annotated, Tuple, NoReturn
from zenml import step
from zenml.client import Client
import sys
import os

client = Client()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from steps.data_ingestion import (step_data_ingestion, 
                                  step_data_join, 
                                  step_electrical_data_dt_process, 
                                  step_thermal_data_dt_process, 
                                  step_get_file_list, 
                                  step_initialization_DIE,
                                  step_cleaning_data)

from steps.data_processing import (step_database,
                                  step_initialize_DPE,
                                  step_loading_meta_table,
                                  step_meta_data_dt_process,
                                  step_database_csv,
                                  step_stat_cols)

# individual thermal and electrical data ingestion pipeline
@pipeline(enable_cache=False)
def data_ingestion_pipeline(dir_path):
    di = step_initialization_DIE(path=dir_path)
    file_list = step_get_file_list(di=di)
    df_thermal, df_electrical = step_data_ingestion(file_list, di=di)
    df_thermal_clean = step_thermal_data_dt_process(df_thermal=df_thermal, di=di)
    df_electrical_clean = step_electrical_data_dt_process(df_electrical=df_electrical, di=di)
    df_join = step_data_join(df_thermal=df_thermal_clean, df_electrical=df_electrical_clean, di=di)
    df_join_clean = step_cleaning_data(df_join, di=di)
    return df_join_clean

# meta table ingestion and experimental database creation
@pipeline(enable_cache=False)
def database_generation_pipeline(dir_path):
    df_raw_data = client.get_artifact_version('Cleaning Joined Data').load()
    dpe = step_initialize_DPE(dir_path)
    df_meta = step_loading_meta_table(dpe=dpe)
    df_meta_processed = step_meta_data_dt_process(dpe=dpe,df_meta=df_meta)
    df_database = step_database(dpe=dpe, df_meta=df_meta_processed, df_raw=df_raw_data)
    df_database_ = step_stat_cols(dpe=dpe, df_database=df_database)
    step_database_csv(dpe=dpe, df_database=df_database_)
    return df_database_