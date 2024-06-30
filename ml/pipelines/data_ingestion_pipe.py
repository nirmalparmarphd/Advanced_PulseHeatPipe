from zenml import pipeline
# imports
import pandas as pd
import numpy as np
import chardet
from typing import Annotated, Tuple, NoReturn
from zenml import step


import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from steps.data_ingestion import (step_data_ingestion, 
                                  step_data_join, 
                                  step_electrical_data_dt_process, 
                                  step_thermal_data_dt_process, 
                                  step_get_file_list, 
                                  step_initialization,
                                  step_cleaning_data)

# individual thermal and electrical data ingestion pipeline
@pipeline(enable_cache=False)
def data_ingestion_pipeline(dir_path):
    di = step_initialization(path=dir_path)
    file_list = step_get_file_list(di=di)
    df_thermal, df_electrical = step_data_ingestion(file_list, di=di)
    df_thermal_clean = step_thermal_data_dt_process(df_thermal=df_thermal, di=di)
    df_electrical_clean = step_electrical_data_dt_process(df_electrical=df_electrical, di=di)
    df_join = step_data_join(df_thermal=df_thermal_clean, df_electrical=df_electrical_clean, di=di)
    df_join_clean = step_cleaning_data(df_join, di=di)
    return df_join_clean
