import pandas as pd
datos = pd.read_csv('datos/datos.csv')
v0 = datos[datos['ventana'] == 0]     # todas las muestras de la ventana 0
print(v0['etiqueta'].iloc[0])         # su etiqueta