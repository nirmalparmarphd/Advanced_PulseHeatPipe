import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
from streamlit.components.v1 import components
import pandas as pd

st.set_page_config(page_title='Pulsating Heat Pipe - Data Visualization Dash-Board',
                   layout='wide')

st.title('Pulsating Heat Pipe - Data Visualization Dash-Board')

db = pd.read_csv('../../data/database/database.csv')
db.head()

pyg_app = StreamlitRenderer(db,
                            use_kernel_calc=True,
                            )
 
pyg_app.explorer()