"""
Semanas 10 y 12: piezas raras -> datos/anomalias.csv (mismo formato que features.csv, etiqueta = anomalia)
Limpia datos/anomalias_crudas.csv con el MISMO limpiar.py, calcula sus caracteristicas con el
MISMO features.py y muestra que responde el clasificador de la semana 7 ante cada una.
Uso (desde la raiz del repo):  python codigo/anomalias.py
"""
import os
import sys
import joblib
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from limpiar import limpiar
from features import tabla_features

crudas = pd.read_csv('datos/anomalias_crudas.csv')
anomalias = tabla_features(limpiar(crudas))
anomalias.to_csv('datos/anomalias.csv', index=False)
print(f"datos/anomalias.csv: {len(anomalias)} ventanas de piezas raras")

# Que responde el clasificador ante cosas que no son ninguna de mis clases
clf = joblib.load('modelo.pkl')
X = clf['escalador'].transform(anomalias[clf['columnas']])
tipos = pd.read_csv('datos/anomalias_tipos.csv')
resultado = tipos.merge(anomalias[['ventana']], on='ventana')
resultado['clasificador_dice'] = clf['modelo'].predict(X)
resultado['confianza'] = clf['modelo'].predict_proba(X).max(axis=1)
print("\nRespuesta del clasificador:")
print(resultado.to_string(index=False))
