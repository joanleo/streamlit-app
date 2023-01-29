import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px

from datetime import datetime
import calendar

from util import *

st.write("""
# Magica Escultura
# """)

from io import StringIO

uploaded_file = st.file_uploader("Choose a file")

reporte = checkFileUPloaded(uploaded_file)
if reporte is not None:
    #Todos los filtro aqui

    st.sidebar.header("Filtros")

    #Filtro por año
    years = [""] + list(reporte['Fecha de Pago'].dt.year.unique())
    selected_year = st.sidebar.selectbox('Año', years)

    #Filtro por mes
    #number_month = ''
    set_months = {'Enero':1, 'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
    #selected_month = st.sidebar.multiselect('Mes', ['','Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],index=datetime.now().month-1)
    months = ['Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    selected_month = st.sidebar.multiselect('Mes', months, months)

    replace_months = [set_months[x] for x in selected_month if x in set_months]
    #if selected_month != '':
    #    number_month = set_months[selected_month]

    #filtro por item
    tipos = reporte['Items'].unique()
    selected_type = st.sidebar.multiselect('Tipo', tipos, tipos)

    #Filtro por servicio o producto
    serv_produc = ''
    lista = reporte['Items'].unique()

    if set(lista) == set(selected_type):
        serv_produc = [""] + list(reporte['Servicio/Producto'].unique())
    elif set(selected_type).issubset(lista):
        serv_produc = [""] + list(reporte.loc[reporte['Items'].isin(selected_type)]['Servicio/Producto'].unique())
    #elif 'Producto' in selected_type:
    #    serv_produc = reporte.loc[reporte['Items'] == 'Producto']['Servicio/Producto'].unique()
    #elif 'Servicio' in selected_type  or 'Reserva' in selected_type:
    #    serv_produc = reporte.loc[reporte['Items'].isin(['Servicio','Reserva'])]['Servicio/Producto'].unique()

    selected_serv_produc = st.sidebar.selectbox('Servicio/Producto',serv_produc)

    #Filtro por Metodo de pago
    metodos_pago = [""] + list(reporte['Medio de Pago'].unique())
    selected_metodo = st.sidebar.selectbox('Medios de pago', metodos_pago)

    #Filtro por prestador
    prestadores = reporte['Prestador/Vendedor'].unique()
    selected_provider = st.sidebar.multiselect('Prestadores', prestadores, 'BEATRIZ CERON')

    
    copy_report  = reporte

    reporte_filter_year = copy_report[copy_report['Fecha de Pago'].dt.year == selected_year]
    #reporte_filter_month = reporte_filter_year[reporte_filter_year['Fecha de Pago'].dt.month == number_month]
    reporte_filter_month = reporte_filter_year[reporte_filter_year['Fecha de Pago'].dt.month.isin(replace_months)]

    copy_report['year'] = reporte['Fecha de Pago'].dt.year
    copy_report['month'] = reporte['Fecha de Pago'].dt.month    

    compare_df = copy_report[['year','month','Precio']].groupby(['year','month']).sum().reset_index()
    compare_df['month'] = compare_df['month'].apply(lambda x: calendar.month_name[x])
    fig_compare = px.line(
        compare_df, 
        title="Comparativo por año",
        x="month", 
        y="Precio", 
        color="year", 
        labels={'year':'Año','month':'Mes', 'Precio':'Venta'})

    st.plotly_chart(fig_compare)


    dict_filters = {
        'año': selected_year,
        #'mes': number_month,
        'mes': replace_months,
        'item': selected_type,
        'serv_product': selected_serv_produc,
        'metodo_pago': selected_metodo,
        'prestador': selected_provider
    }
    
    reporte_filter = createFilter(copy_report, dict_filters)

    st.write("""
    # Resumen de tipos
    # """)
    
    reporte_filter.drop(columns='index', inplace=True)

    report_show = reporte_filter.copy()
    report_show['Precio'] = report_show['Precio'].astype('int64')

    #st.dataframe(report_show)
    col1, col2 = st.columns(2)
    df_group_type = (reporte_filter.groupby('Items').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .rename(columns={'Precio':'Total'})
                                    .reset_index())
    #report_show = df_group_type.copy()
    #report_show['Total'] = report_show['Total'].apply("{:,.2f}".format)
    df_group_type['Total'] = df_group_type['Total'].astype('int64')
    col1.dataframe(df_group_type)

    categoria = df_group_type['Items']
    total = df_group_type['Total']

    # Creando el grafico
    fig = px.pie(total, values=total, names = categoria, hover_name=categoria)

    fig.update_layout(showlegend=False,
        width=400,
        height=400,
        margin=dict(l=1,r=1,b=1,t=1),
        font=dict(color='#383635', size=15)
        )

    fig.update_traces(textposition='inside', textinfo='percent+label')

    col2.plotly_chart(fig)


    st.write("""
    # Resumen por prestador(s)
    # """)

    col3, col4 = st.columns(2)

    df_group_prestador = (reporte_filter.groupby('Prestador/Vendedor').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .rename(columns={'Precio':'Total'})
                                    .reset_index())

    #report_show = df_group_prestador.copy()
    #report_show['Total'] = report_show['Total'].apply("{:,.2f}".format)
    df_group_prestador['Total'] = df_group_prestador['Total'].astype('int64')
    col3.dataframe(df_group_prestador)

    categoria = df_group_prestador['Prestador/Vendedor'].unique()
    total = df_group_prestador['Total']

    # Creando el grafico
    fig_provider = px.pie(total, values=total, names = categoria, hover_name=categoria)

    fig_provider.update_layout(showlegend=False,
        width=400,
        height=400,
        margin=dict(l=1,r=1,b=1,t=1),
        font=dict(color='#383635', size=15)
        )

    fig_provider.update_traces(textposition='inside', textinfo='percent+label')
    col4.plotly_chart(fig_provider)


    st.write("""
    # Resumen por servicio(s) / producto(s)
    # """)

    df_group_serv_product = (reporte_filter.groupby('Servicio/Producto').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .rename(columns={'Precio':'Total'})
                                    .reset_index())
    col5, col6 = st.columns(2)

    report_show = df_group_serv_product.copy()
    report_show['Total'] = report_show['Total'].astype('int64')

    col5.dataframe(report_show)

    categoria = df_group_serv_product['Servicio/Producto'].unique()
    total = df_group_serv_product['Total']

    # Creando el grafico
    fig_serv_product = px.pie(total, values=total, names = categoria, hover_name=categoria)

    fig_serv_product.update_layout(showlegend=False,
        width=400,
        height=400,
        margin=dict(l=1,r=1,b=1,t=1),
        font=dict(color='#383635', size=15)
        )

    fig_serv_product.update_traces(textposition='inside', textinfo='percent+label')
    col6.plotly_chart(fig_serv_product)

    st.write("""
    # Resumen por metodo de pago
    ##### AÑO: {temp1} 
    ##### MES(ES): {temp2}
    ###### METODO(S) DE PAGO: {temp3}""".format(temp1=selected_year, temp2=', '.join([x.lower() for x in selected_month]),
                                               temp3= "Todos" if len(selected_metodo) == 0 else selected_metodo))

    df_group_metodo_pago = (reporte_filter.groupby('Medio de Pago').agg({'Cantidad':'count', 'Precio':'sum'})
                                    .rename(columns={'Precio':'Total'})
                                    .reset_index())
    col7, col8 = st.columns(2)

    report_show = df_group_metodo_pago.copy()
    report_show['Total'] = report_show['Total'].astype('int64')

    col7.dataframe(report_show)

    categoria = df_group_metodo_pago['Medio de Pago'].unique()
    total = df_group_metodo_pago['Total']

    # Creando el grafico
    fig_metodo_pago = px.pie(total, values=total, names = categoria, hover_name=categoria)

    fig_metodo_pago.update_layout(showlegend=False,
        width=400,
        height=400,
        margin=dict(l=1,r=1,b=1,t=1),
        font=dict(color='#383635', size=15)
        )

    fig_metodo_pago.update_traces(textposition='inside', textinfo='percent+label')
    col8.plotly_chart(fig_metodo_pago)


    #selected_provider = st.multiselect('Prestadores', prestadores, prestadores)

    #df_filter_provider = reporte_filter_month[reporte_filter_month['Prestador/Vendedor'].isin(selected_provider)].reset_index()
    #st.write(reporte_filter)


        
        

        #st.write("### Se muestran todos los datos del mes de ",reporte_filter_month)

        #st.write("### Total por servicio")
        #df_group_service = (reporte_filter_month.groupby('Servicio/Producto').agg({'Cantidad':'count', 'Precio':'sum'})
        #                                .reset_index()
        #                                .rename(columns={'fecha':'Cant', 'precio':'Total'}))

        #st.dataframe(df_group)
        #st.dataframe(df_group_service)


        

        #reporte_filter_type = reporte_filter_month[reporte_filter_month['Items'] == selected_type] '''
        #st.write("""### Tipo """,selected_type)
        #st.dataframe(reporte_filter_month)