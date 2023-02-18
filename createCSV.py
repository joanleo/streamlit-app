from bd.connectMysql import conexionDb
import os

def getTable(table):
    try:
        cnx = conexionDb()
        cursor = cnx.cursor()
        cursor.execute(f'SELECT * FROM {table}')
        columnas = [columna[0] for columna in cursor.description]
        detalle_pagos = cursor.fetchall()
        return columnas, detalle_pagos
    except Exception as err:
        print("Ocurrio un error createDb: ", err)
    finally:
        cursor.close()
        cnx.close()

def createCSV(table):
    columnas, tabla = getTable(table)
    path = os.getcwd() + f'\{table}.csv'
    with open(path, 'w', encoding='utf-8') as archivo:
        archivo.write(';'.join(columnas))
        archivo.write('\n')
        for registro in tabla:
            registro = [val if val != "" else f"sin {col}" for col, val in zip(columnas,registro)]
            archivo.write(';'.join([str(campo).upper() for campo in registro]))
            archivo.write('\n')

createCSV('ultimopago')