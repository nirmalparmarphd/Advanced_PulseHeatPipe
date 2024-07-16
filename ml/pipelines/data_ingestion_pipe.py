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
                                  step_stat_cols,
                                  step_dropping_garbage_date,
                                  step_gfe_calculation,
                                  step_to_abs_pressure,
                                  step_to_si_units,
                                  step_TR_calculation)

from steps.data_eda import (plot_dG_vs_P,
                            plot_dG_vs_Te,
                            plot_dG_vs_TR,
                            plot_P_vs_Te,
                            plot_Tc_vs_Te,
                            plot_TR_vs_Q,
                            plot_TR_vs_Te,)

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
def database_generation_pipeline(dir_path, database):
    # df_raw_data = client.get_artifact_version('Cleaning Joined Data').load()
    dpe = step_initialize_DPE(dir_path)
    df_meta = step_loading_meta_table(dpe=dpe)
    df_meta_processed = step_meta_data_dt_process(dpe=dpe,df_meta=df_meta)
    df_database = step_database(dpe=dpe, df_meta=df_meta_processed, df_raw=database)
    df_database_ = step_stat_cols(dpe=dpe, df_database=df_database)
    df_database_f = step_dropping_garbage_date(dpe=dpe, df_database=df_database_)
    df_database = step_to_abs_pressure(dpe=dpe, database=df_database_f)
    df_database = step_to_si_units(dpe=dpe, database=df_database)
    df_database = step_TR_calculation(dpe=dpe, database=df_database)
    df_database = step_gfe_calculation(dpe=dpe, database=df_database)
    step_database_csv(dpe=dpe, df_database=df_database)
    return df_database_

# data visualization pipeline
@pipeline(enable_cache=False)
def auto_eda_plots(dir_path, database):
    database = client.get_artifact_version('Calculating Gibbs Free Energy').load()
    plot_dG_vs_P(data=database, dir_path=dir_path, sample='DI_Water')
    plot_dG_vs_Te(data=database, dir_path=dir_path, sample='DI_Water')
    plot_dG_vs_TR(data=database, dir_path=dir_path, sample='DI_Water')
    plot_P_vs_Te(data=database, dir_path=dir_path, sample='DI_Water')
    plot_Tc_vs_Te(data=database, dir_path=dir_path, sample='DI_Water')
    plot_TR_vs_Q(data=database, dir_path=dir_path, sample='DI_Water')
    plot_TR_vs_Te(data=database, dir_path=dir_path, sample='DI_Water')
    return None

# data pre-processing pipeline

# ml pipeline

# ml evaluation pipeline