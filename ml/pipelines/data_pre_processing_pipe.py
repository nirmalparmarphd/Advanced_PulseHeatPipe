# for data pre-processing for ML

import pandas as pd

class DataPreProcessingEngine():
    '''
    Pre-processing experimental data

    standardization

    handling categorical data

    handling datetime data
    '''

    def __init__(self,
                 data: pd.DataFrame):
        self.data = data

    def do_standardization(self):
        pass

    def do_categorization(self):
        pass

    def do_train_test_split(self):
        pass

    def do_drop_cols(self):
        pass

    def do_save_to_csv(self):
        pass