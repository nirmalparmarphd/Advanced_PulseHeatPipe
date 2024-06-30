# to perform eda and to save some important graphs

class DataVisualizationEngine:
    """
    to visualize thermal params

    # temperature plot @ FR, A, B

    # heat Q plot @ FR, A, B

    # pressure plot @ FR, A, B

    # Q vs TR @ FR, A, B
    """

    def __init__(self, dir_path: str):
        """
        to initialize data visualization engine

        args:
            dir_path: str '../data/'

        returns:
            None
        """
        self.dir_path = dir_path

    