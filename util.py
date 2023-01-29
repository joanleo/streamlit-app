import pandas as pd

def checkFileUPloaded(uploaded_file):
    if uploaded_file is not None:
        
        reporte = pd.read_excel(uploaded_file, 'Produccion', thousands='.', header=None)
        medios_pago = pd.read_excel(uploaded_file,'Medios de Pago', thousands='.', header=None)

        reporte = cleanSheet(reporte)
        medios_pago = cleanSheet(medios_pago)
        columns = []
        for col in  reporte.columns:
            columns.append(col)
        columns.append('Medio de Pago')
        merged_df = pd.merge(reporte, medios_pago, left_on='Identificador', right_on='Identificador', suffixes=('_x', '_y'))
        col_merge = merged_df.columns
        for col in col_merge:
            if '_y' in col:
                merged_df.drop(columns=col, inplace=True)
            if '_x' in col:
                merged_df.rename(columns={col:col.split('_')[0]}, inplace=True)
        merged_df = merged_df[columns]
        

        return merged_df

def cleanSheet(hoja):
    columns = hoja.iloc[0]
    hoja = hoja.drop(0)
    hoja = hoja.reset_index(drop=True)
    hoja.columns = columns
    #hoja.fillna(method="ffill", inplace=True)
    columns_to_fill = ['Identificador', 'Items', 'Nombre cliente', 'Fecha de Pago']
    #hoja[columns_to_fill] = hoja[columns_to_fill].fillna(method='ffill') 
    hoja = fill_missing_values(hoja, columns_to_fill)
    col_delete = ['index','Local','c.i. cliente','Email cliente','Teléfono cliente','Total','Reserva']
    for col in columns:
        if col in col_delete:
            hoja.drop(columns=col, inplace=True)
    hoja=hoja.mask(hoja == '')
    
    esta_m = [x for x in columns if x == 'Medio de Pago']

    if not esta_m:
        hoja = hoja.dropna(subset=['Precio'])
        hoja = hoja[hoja['Precio'] != 0]
        hoja['Precio'] = pd.to_numeric(hoja['Precio'])
        hoja['Fecha de Pago'] = pd.to_datetime(hoja['Fecha de Pago'])
        hoja['Servicio/Producto'] = hoja['Servicio/Producto'].str.split(',').str.get(1).fillna(hoja['Servicio/Producto'])
        hoja['Prestador/Vendedor'] = hoja['Prestador/Vendedor'].str.split('(').str.get(0)
        hoja['Prestador/Vendedor'] = hoja['Prestador/Vendedor'].str.strip().str.upper()

    return hoja

def fill_missing_values(df, columns_to_fill):
    existing_columns = set(df.columns)
    columns_to_fill = set(columns_to_fill)
    if columns_to_fill.issubset(existing_columns):
        columns_to_fill = list(columns_to_fill)
        df[columns_to_fill] = df[columns_to_fill].fillna(method='ffill')
    
    return df

def createFilter(reporte, dict_filters):
    
    for k,v in dict_filters.items():
            #print(f"{k} : {v}")
        if k == 'año' and v != '':
            reporte = reporte[reporte['Fecha de Pago'].dt.year == v]
        if k == 'mes' and len(v) > 0:
            #reporte = reporte[reporte['Fecha de Pago'].dt.month == v]
            reporte = reporte[reporte['Fecha de Pago'].dt.month.isin(v)]
        if k == 'item' and len(v) > 0:
            reporte = reporte[reporte['Items'].isin(v)].reset_index()
        if k == 'prestador' and len(v) > 0:
            reporte = reporte[reporte['Prestador/Vendedor'].isin(v)]
        if k == 'serv_product' and v != '':
            reporte = reporte[reporte['Servicio/Producto'] == v]
        if k == 'metodo_pago' and v != '':
            reporte = reporte[reporte['Medio de Pago'] == v]

    return reporte


