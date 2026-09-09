import pandas as pd

# 1. Cargar el dataset recabado
datos = pd.read_csv('datos/datos.csv')

# 2. Eliminar valores atípicos (Rango físico plausible de la celda de carga)
# La celda de carga registra tara en 0.0 kg y un límite seguro máximo de 2.0 kg
datos = datos[(datos['valor'] >= 0.0) & (datos['valor'] <= 2.0)]

# 3. Aplicar filtro de media móvil (window=5) POR VENTANA
# Se usa groupby('ventana') para evitar mezclar bordes de diferentes capturas
K = 5
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor']
    .transform(lambda s: s.rolling(window=K, center=True).mean())
)

# 4. Manejo de NaN en las orillas
# Se rellenan los extremos usando los valores válidos más cercanos dentro del evento
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor_filtrado']
    .transform(lambda s: s.bfill().ffill())
)

print("[-] Muestra del filtrado aplicado:")
print(datos[['ventana', 't', 'valor', 'valor_filtrado', 'etiqueta']].head(10))