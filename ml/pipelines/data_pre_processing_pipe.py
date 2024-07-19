from zenml import pipeline
from zenml.client import Client
import os, sys
import pandas as pd
client = Client()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from steps.data_pre_processing import (step_get_database,
                                       step_get_features,
                                       step_initialize_DPPE)

@pipeline(enable_cache=False, name='ML Data Pre Processing')
def data_preprocessing_pipeline(data_path:str):
    dppe = step_initialize_DPPE(data_path)
    df = step_get_database(dppe)
    data = step_get_features(dppe, df=df)
    return data

