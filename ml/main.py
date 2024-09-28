from fastapi import FastAPI
from enum import Enum
from run import main_pipeline_php

# class for ML model selection
class ModelSelection(str, Enum):
    RandomForestRegressor = 'rfr'
    AdaBoostRegressor = 'abr'

app = FastAPI(title="Pulsating Heat Pipe - Advanced Data Analytics and Machine Learning",
              description="""Web browser base interface to interact and trigger advanced analytics and machine learning pipelines for PHP experimental data.

website - www.nirmalparmar.info \n
mail - nirmalparmarphd@gmail.com

    Author - Dr.Nirmal Parmar, PhD
""")

@app.get("/items/{ml_model}")
async def trigger_ml_pipeline(ml_model: ModelSelection = 'Random Forest Regressor',
                               data_path: str = "../data/",
                               meta_file: str = "meta_table_data.csv",
                               ):

    results = main_pipeline_php(path = data_path,
                                meta_table = meta_file,
                                ml_model = ml_model)
    return results