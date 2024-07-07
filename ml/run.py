# to run all ML pipelines

from pipelines.data_ingestion_pipe import data_ingestion_pipeline, database_generation_pipeline

from zenml import pipeline

@pipeline(enable_cache=False, name='main_pipeline')
def main_pipeline(path:str = '../data/'):
    data_ingestion = data_ingestion_pipeline(dir_path=path)
    database_generation = database = database_generation_pipeline(dir_path=path)

# running main pipeline
main_pipeline()
