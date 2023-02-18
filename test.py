import pandas as pd

detalle = pd.read_csv("detalle.csv", sep=';')
pago = pd.read_csv('ultimopago.csv', sep=';')
print("detalle")
print(detalle.isna().sum())
print("Pagos")
print(pago.isna().sum())