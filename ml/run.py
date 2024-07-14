# to run all ML pipelines

from pipelines.data_ingestion_pipe import data_ingestion_pipeline, database_generation_pipeline

from zenml import pipeline
import sys, os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pipeline(enable_cache=False, name='main_pipeline')
def main_pipeline(path:str = '../data/'):
    # ingesting raw experimental data and combining them all
    data_ingestion = data_ingestion_pipeline(dir_path=path)

    # with help of the experimental metal table selecting/filtering data, combining, and cleaning
    database_generation = database = database_generation_pipeline(dir_path=path)
    
    # auto generation of plots for selected thermal properties

    # data pre-processing before ML

    # ML training and evaluation of ML model

    # auto generation of plots for ML-experimental data

# running main pipeline
main_pipeline()

