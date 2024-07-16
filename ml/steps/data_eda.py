# to perform eda and to save some important graphs

from PyPulseHeatPipe import PulseHeatPipe, DataVisualization
import pandas as pd
from zenml import step
from typing import Annotated, Tuple
import os

class DataVisualizationEngine:
    """
    to visualize thermal params

    # temperature plot @ FR, A, B

    # heat Q plot @ FR, A, B

    # pressure plot @ FR, A, B

    # Q vs TR @ FR, A, B
    """

    def __init__(self, 
                 dir_path: str, 
                 sample: str):
        """
        to initialize data visualization engine

        args:
            dir_path: str '../data/'
            sample: str

        returns:
            None
        """
        self.dir_path = dir_path
        self.sample = sample

        path = os.path.join(self.dir_path, 'plots')
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Directory '{path}' created.")
        else:
            print(f"Directory '{path}' already exists.")

        self.dv = DataVisualization(dir_path=path,
                                     sample=sample)
        
        # further data filter for plots at specific conditions

    def plot_thermal_property(self,
                              data: pd.DataFrame,
                              x_col: str,
                              y_col: str,
                              auto_data_chop: bool,
                              plot_method: str,
                              figsize = (15, 7),
                              save_figure: bool = True
                              ):
        """
        to plot thermal properties

        args:
            data: pd.DataFrame,
                x_col: str,
                y_col: str,
                auto_data_chop: bool = True,
                plot_method: str,
                figsize = (15, 7),
                save_figure: bool = True

        returns:
            saves pdf of selected properties

        """          
        self.dv.get_plots(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
        return print('completed auto plotting.')
#1
@step
def plot_Tc_vs_Te(data: pd.DataFrame,
                        x_col: str = 'Te_mean[K]',
                        y_col: str = 'Tc_mean[K]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of Tc vs Te']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#2
@step
def plot_P_vs_Te(data: pd.DataFrame,
                        x_col: str = 'Te_mean[K]',
                        y_col: str = 'P[bar]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of P vs Te']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#3
@step
def plot_TR_vs_Te(data: pd.DataFrame,
                        x_col: str = 'Te_mean[K]',
                        y_col: str = 'TR[K/W]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of TR vs Te']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#4
@step
def plot_TR_vs_Q(data: pd.DataFrame,
                        x_col: str = 'Q[W]',
                        y_col: str = 'TR[K/W]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of TR vs Q']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#5
@step
def plot_dG_vs_Te(data: pd.DataFrame,
                        x_col: str = 'Te_mean[K]',
                        y_col: str = 'dG[KJ/mol]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of dG vs Te']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#6
@step
def plot_dG_vs_P(data: pd.DataFrame,
                        x_col: str = 'P[bar]',
                        y_col: str = 'dG[KJ/mol]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of dG vs P']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None
#7
@step
def plot_dG_vs_TR(data: pd.DataFrame,
                        x_col: str = 'TR[K/W]',
                        y_col: str = 'dG[KJ/mol]',
                        auto_data_chop: bool = True,
                        plot_method: str = 'combined',
                        figsize = (15, 7),
                        save_figure: bool = True,
                        dir_path: str = '../data',
                        sample: str = 'DI_Water'
                    )->Annotated[None, 'Auto Plotting of dG vs TR']:
    dve = DataVisualizationEngine(dir_path=dir_path, sample=sample)
    dve.plot_thermal_property(data=data,
                            x_col=x_col,
                            y_col=y_col,
                            auto_data_chop=auto_data_chop,
                            plot_method=plot_method,
                            figsize=figsize,
                            save_figure = save_figure)
    return None