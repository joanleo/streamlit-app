import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px

from datetime import datetime
import calendar

from util import *

from comparativos import comparativos

st.write("""## Magica Escultura """)


uploaded_file = st.file_uploader("Seleccionar el archivo del reporte")
reporte = checkFileUPloaded(uploaded_file)

tab1, tab2, tab3 = st.tabs(["📈 Graficos", "🗃 Data", "Comparativos"])
if reporte is not None:
    comparativo = comparativos(reporte)