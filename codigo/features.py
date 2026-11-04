"""
Semana 5: caracteristicas en el dominio del tiempo -> datos/features.csv (una fila por ventana)
Uso (desde la raiz del repo):  python codigo/features.py
"""
import os
import numpy as np
import pandas as pd

UMBRAL = 0.05       # valor normalizado a partir del cual "hay pieza" (para duracion)

# Las calculo todas, pero estas NO entran al modelo (ver BITACORA semana 5):
DESCARTADAS = [
    'minimo',             # siempre ~0.02: todas las ventanas empiezan en la linea base
    'energia',            # repite a la media (es casi media al cuadrado)
    'duracion',           # ~196 en todas: la pieza se queda encima toda la ventana
]


def calcular_features(x):
    """x = valores de UNA ventana ya limpia, en orden de t. Devuelve un diccionario."""
    x = np.asarray(x, dtype=float)
    fila = {}
    # ---- tiempo (semana 5) ----
    fila['media'] = np.mean(x)
    fila['desv'] = np.std(x)
    fila['minimo'] = np.min(x)
    fila['maximo'] = np.max(x)
    fila['rango'] = np.max(x) - np.min(x)
    fila['energia'] = np.sum(x ** 2)
    fila['duracion'] = int(np.sum(np.abs(x) > UMBRAL))
    # propias del dominio: el peso ya asentado y cuanto se pasa el golpe de ese peso
    fila['meseta'] = np.median(x[len(x) // 2:])
    fila['sobrepaso'] = fila['maximo'] - fila['meseta']
    return fila


def tabla_features(datos_limpios):
    """Aplica calcular_features a cada ventana de un DataFrame limpio."""
    filas = []
    for ventana, g in datos_limpios.groupby('ventana'):
        fila = {'ventana': ventana}
        fila.update(calcular_features(g.sort_values('t')['valor']))
        fila['etiqueta'] = g['etiqueta'].iloc[0]
        filas.append(fila)
    return pd.DataFrame(filas).drop(columns=DESCARTADAS)


def tabla_todas(datos_limpios):
    """Igual que tabla_features pero sin descartar nada (para analizar)."""
    filas = []
    for ventana, g in datos_limpios.groupby('ventana'):
        fila = calcular_features(g.sort_values('t')['valor'])
        fila['etiqueta'] = g['etiqueta'].iloc[0]
        filas.append(fila)
    return pd.DataFrame(filas)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    datos = pd.read_csv('datos/datos_limpios.csv')
    features = tabla_features(datos)
    features.to_csv('datos/features.csv', index=False)
    print(f"datos/features.csv: {features.shape[0]} filas x {features.shape[1]} columnas")
    print("Todas las candidatas (promedio y desviacion por clase):")
    todas = tabla_todas(datos)
    print(todas.groupby('etiqueta').agg(['mean', 'std']).T.round(3).to_string())
    print(f"\nSe quedan: {[c for c in features.columns if c not in ('ventana', 'etiqueta')]}")

    os.makedirs('figuras', exist_ok=True)
    clases = sorted(features['etiqueta'].unique())
    colores = {c: f'C{i}' for i, c in enumerate(clases)}

    # Mejor par de caracteristicas (figuras/features.png)
    plt.figure(figsize=(6, 5))
    for c, g in features.groupby('etiqueta'):
        plt.scatter(g['meseta'], g['sobrepaso'], label=c, color=colores[c])
    plt.xlabel('meseta (peso asentado, normalizado)')
    plt.ylabel('sobrepaso (pico - meseta)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figuras/features.png', dpi=150)

    # Matriz de dispersion completa (figuras/scatter_matrix.png)
    columnas = [c for c in features.columns if c not in ('ventana', 'etiqueta')]
    pd.plotting.scatter_matrix(features[columnas], c=features['etiqueta'].map(colores),
                               figsize=(12, 12), diagonal='hist', alpha=0.8)
    plt.savefig('figuras/scatter_matrix.png', dpi=100)

    print("Figuras: features.png, scatter_matrix.png")
