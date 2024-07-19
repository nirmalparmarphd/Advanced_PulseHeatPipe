from zenml import step
import pandas as pd
from typing import Annotated

class DataPreProcessingEngine():
    '''
    data pre-processing for ML
    
        handling categorical value

        dropping redundant features

        feature standardization
    '''

    def __init__(self, data_path:str = '../data/database/database.csv') -> None:
        self.data_path = data_path

    def get_database(self)->pd.DataFrame:
        df = pd.read_csv(self.data_path)
        return df
    
    def get_features(self, 
                     df:pd.DataFrame,
                     cols:list = ['voltage', 'current', 'power', 'FR[%]', 'Q[W]', 'alpha', 'beta', 
                                        'P[bar]','Te_mean[K]', 'Tc_mean[K]', 'Te_std[K]', 'Tc_std[K]', 
                                        'T_pulse[K]', 'TR[K/W]']):
        '''
        features without gfe 'GFE_Te[KJ/mol]', 'GFE_Tc[KJ/mol]', 'dG[KJ/mol]'
        '''
        df = df[cols]
        return df
    
    def get_features_with_gfe(self,
                              df: pd.DataFrame,
                              cols: list = ['voltage', 'current', 'power', 'FR[%]', 'Q[W]', 'alpha', 'beta', 
                                        'P[bar]','Te_mean[K]', 'Tc_mean[K]', 'Te_std[K]', 'Tc_std[K]', 
                                        'GFE_Te[KJ/mol]', 'GFE_Tc[KJ/mol]', 'dG[KJ/mol]', 'T_pulse[K]', 'TR[K/W]']):
        df = df[cols]
        return df
    
@step
def step_initialize_DPPE(data_path:str)->Annotated[DataPreProcessingEngine, 'Data Pre-Processing for ML']:
    dppe = DataPreProcessingEngine(data_path=data_path)
    return dppe

@step
def step_get_database(dppe:DataPreProcessingEngine)->Annotated[pd.DataFrame, 'Load Experimental DataBase']:
    df = dppe.get_database()
    return df

@step
def step_get_features(dppe:DataPreProcessingEngine,
                      df:pd.DataFrame)->Annotated[pd.DataFrame, 'Features Selection']:
    df = dppe.get_features(df)
    return df