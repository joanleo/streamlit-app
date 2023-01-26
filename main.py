import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px

from datetime import datetime
import calendar


st.write("""
# Magica Escultura
# """)

from io import StringIO

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    reporte = pd.read_excel(uploaded_file, 'Produccion', thousands='.', header=None)
    columns = reporte.iloc[0]
    reporte = reporte.drop(0)
    reporte = reporte.reset_index(drop=True)
    reporte.columns = columns
    reporte=reporte.mask(reporte == '')
    reporte.fillna(method="ffill", inplace=True)
    reporte.drop(columns='Local', inplace=True)
    reporte.drop(columns='Total', inplace=True)
    reporte['Precio'] = reporte['Precio'].round(2)
    reporte['Fecha de Pago'] = pd.to_datetime(reporte['Fecha de Pago'])
    reporte['Servicio/Producto'] = reporte['Servicio/Producto'].str.split(',').str.get(1).fillna(reporte['Servicio/Producto'])

    st.sidebar.header("User Input Features")

    years = reporte['Fecha de Pago'].dt.year.unique()
    selected_year = st.sidebar.selectbox('Año', years)

    reporte_filter_year = reporte[reporte['Fecha de Pago'].dt.year == selected_year]

    copy_report  = reporte

    copy_report['year'] = reporte['Fecha de Pago'].dt.year
    copy_report['month'] = reporte['Fecha de Pago'].dt.month    

    compare_df = copy_report[['year','month','Precio']].groupby(['year','month']).sum().reset_index()
    compare_df['month'] = compare_df['month'].apply(lambda x: calendar.month_name[x])
    st.write(compare_df)
    fig_compare = px.line(
        compare_df, 
        x="month", 
        y="Precio", 
        color="year", 
        title="Comparativo ventas  por mes y año",
        labels={'year':'Año','month':'Mes', 'Precio':'Venta'})

    st.write(fig_compare)


    set_months = {'Enero':1, 'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
    selected_month = st.sidebar.selectbox('Mes', ['Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],index=datetime.now().month-1)
    number_month = set_months[selected_month]

    reporte_filter_month = reporte_filter_year[reporte_filter_year['Fecha de Pago'].dt.month == number_month]


    df_group_type = (reporte_filter_month.groupby('Items').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .reset_index())

    st.dataframe(df_group_type)

    categoria = df_group_type['Items']
    total = df_group_type['Precio']

    # This is an example of a plotly pie chart
    fig = px.pie(total, values=total, names = categoria, hover_name=total)

    # TODO: change the values of the update_layout function and see the effect
    fig.update_layout(showlegend=False,
        width=400,
        height=400,
        margin=dict(l=1,r=1,b=1,t=1),
        font=dict(color='#383635', size=15))

    # this function adds labels to the pie chart
    # for more information on this chart, visit: https://plotly.com/python/pie-charts/
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # after creating the chart, we display it on the app's screen using this command
    st.write(fig)


    ''' st.write("### Se muestran todos los datos del mes de ",reporte_filter_month)

    st.write("### Total por servicio")
    df_group_service = (reporte_filter_month.groupby('Servicio/Producto').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .reset_index()
                                    .rename(columns={'fecha':'Cant', 'precio':'Total'}))

    #st.dataframe(df_group)
    st.dataframe(df_group_service) '''


    ''' tipos = reporte['Items'].unique()
    selected_type = st.sidebar.selectbox('Tipo', tipos)

    reporte_filter_type = reporte_filter_month[reporte_filter_month['Items'] == selected_type] '''
    #st.write("""### Tipo """,selected_type)
    #st.dataframe(reporte_filter_month)