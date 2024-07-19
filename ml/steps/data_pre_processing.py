from zenml import steps
import pandas as pd

class DataPreProcessing():
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
    
    def get_features(self, cols:list = ['voltage', 'current', 'power', 'FR[%]', 'Q[W]', 'alpha', 'beta', 
                                        'P[bar]','Te_mean[K]', 'Tc_mean[K]', 'Te_std[K]', 'Tc_std[K]', 'T_pulse[K]',
                                        'TR[K/W]', 'GFE_Te[KJ/mol]', 'GFE_Tc[KJ/mol]', 'dG[KJ/mol]']):
        df = df[cols]
        return df
    