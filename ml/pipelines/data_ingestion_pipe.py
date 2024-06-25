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

from steps.data_ingestion import step_data_ingestion, step_data_join, step_electrical_data_cleaning, step_thermal_data_cleaning

# individual thermal and electrical data ingestion pipeline
@pipeline(enable_cache=False)
def data_ingestion_pipeline(path):
    df_thermal, df_electrical = step_data_ingestion(path)
    df_thermal_clean = step_thermal_data_cleaning(path, df_thermal=df_thermal)
    df_electrical_clean = step_electrical_data_cleaning(path, df_electrical=df_electrical)
    df_join = step_data_join(path, df_thermal=df_thermal_clean, df_electrical=df_electrical_clean)
    return df_join
