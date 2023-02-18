import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import calendar

from datetime import datetime

def comparativos(reporte):
    
    months = ['Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    copy_report  = reporte

    
    copy_report['año'] = reporte['Fecha de Pago'].dt.year
    copy_report['mes'] = reporte['Fecha de Pago'].dt.month    

    compare_df = copy_report[['año','mes','Precio']].groupby(['año','mes']).sum().reset_index()
    compare_df['mes'] = compare_df['mes'].apply(lambda x: months[x-1])
    fig_compare = px.line(
        compare_df, 
        title="Comparativo por año",
        x="mes", 
        y="Precio", 
        color="año", 
        labels={'Año':'Año','Mes':'Mes', 'Ventas':'Ventas'})

    st.plotly_chart(fig_compare)

    #st.dataframe(copy_report.style.format({'Precio':'{:.2f}'}))
    #Filtro por año
    #years = [""] + list(reporte['Fecha de Pago'].dt.year.unique())
    #selected_year = st.selectbox('Año', years)
    años_disponibles = copy_report['año'].unique()
    años_seleccionados = st.multiselect('Selecciona los años a comparar', años_disponibles)


    #Filtro por mes
    set_months = {'Enero':1, 'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
    
    selected_month = st.multiselect('Mes', months, months)
    ventas_por_mes_filtrado = compare_df[(compare_df['año'].isin(años_seleccionados)) & (compare_df['mes'].isin(selected_month))]
    # Creación de la tabla comparativa
    if len(años_seleccionados) > 1 and len(selected_month) > 0:
        df_comparativa = ventas_por_mes_filtrado.pivot_table(index='mes', columns='año', values='Precio')

        # Agregar una columna con la diferencia porcentual entre los años
        df_comparativa['Crecimiento %'] = (1-(df_comparativa[años_seleccionados[1]] / df_comparativa[años_seleccionados[0]])) * 100

        # Redondear los valores a dos decimales
        #df_comparativa = df_comparativa.round(2)
        st.dataframe(df_comparativa.style.format({'Crecimiento %':'{:.2f}', 'año':'{:.2f}'}))
        ventas_agrupadas = ventas_por_mes_filtrado.groupby(['año', 'mes'])['Precio'].sum().reset_index()
        ventas_agrupadas = ventas_agrupadas.rename(columns={'Precio': 'Ventas', 'mes':'Mes', 'año':'Año'})
        ventas_agrupadas['Año'] = ventas_agrupadas['Año'].astype(str)
        fig = px.bar(ventas_agrupadas, 
                     x='Mes', 
                     y='Ventas', 
                     color='Año',
                     barmode ='group')
        st.plotly_chart(fig)
    #reporte_filter_year = copy_report[copy_report['Fecha de Pago'].dt.year == selected_year]
    #reporte_filter_month = reporte_filter_year[reporte_filter_year['Fecha de Pago'].dt.month == number_month]
    #reporte_filter_month = reporte_filter_year[reporte_filter_year['Fecha de Pago'].dt.month.isin(replace_months)]
