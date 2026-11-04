"""
Caracteristicas por ventana -> datos/features.csv (una fila por ventana)
Semana 5: dominio del tiempo.  Semana 6: dominio de la frecuencia (FFT).
calcular_features() la usan tambien control.py, pca.py, clustering.py y autoencoder.py,
para que todos calculen exactamente lo mismo.
Uso (desde la raiz del repo):  python codigo/features.py
"""
import os
import numpy as np
import pandas as pd

FS = 50.0           # Hz (200 muestras en 4 s). Nyquist = 25 Hz
BANDA_CORTE = 3.0   # Hz: abajo esta el escalon del peso, arriba el rebote del impacto
UMBRAL = 0.05       # valor normalizado a partir del cual "hay pieza" (para duracion)

# Las calculo todas, pero estas NO entran al modelo (ver BITACORA semanas 5 y 6):
DESCARTADAS = [
    'minimo',             # siempre ~0.02: todas las ventanas empiezan en la linea base
    'energia',            # repite a la media (es casi media al cuadrado)
    'duracion',           # ~196 en todas: la pieza se queda encima toda la ventana
    'f_dominante',        # salta entre 0.25 y 9 Hz sin patron: es ruido, no fisica
    'centroide',          # ~7.2 Hz en las tres clases: no separa
    'energia_espectral',  # = banda_baja + banda_alta, informacion repetida
    'banda_baja',         # es el escalon del peso: repite a la media
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
    # ---- frecuencia (semana 6) ----
    espectro = np.abs(np.fft.rfft(x))[1:]
    frecuencias = np.fft.rfftfreq(len(x), 1 / FS)[1:]
    fila['f_dominante'] = frecuencias[np.argmax(espectro)]
    fila['centroide'] = np.sum(frecuencias * espectro) / np.sum(espectro)
    fila['energia_espectral'] = np.sum(espectro ** 2)
    fila['banda_baja'] = np.sum(espectro[frecuencias < BANDA_CORTE] ** 2)
    fila['banda_alta'] = np.sum(espectro[frecuencias >= BANDA_CORTE] ** 2)
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

    # Espectro de una ventana por clase (figuras/espectro.png) y promedio por clase
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4))
    for c in clases:
        ventanas = datos[datos['etiqueta'] == c].pivot(index='t', columns='ventana', values='valor')
        ventanas = ventanas.ffill().bfill()
        fr = np.fft.rfftfreq(len(ventanas), 1 / FS)[1:]
        esp = np.abs(np.fft.rfft(ventanas.values, axis=0))[1:]
        a1.plot(fr, esp[:, 0], label=c, color=colores[c])
        a2.plot(fr, esp.mean(axis=1), label=c, color=colores[c])
    for a, titulo in ((a1, 'Una ventana por clase'), (a2, 'Promedio por clase')):
        a.axvline(BANDA_CORTE, color='k', ls='--', lw=1)
        a.set_yscale('log')
        a.set_xlabel('frecuencia (Hz)')
        a.set_title(titulo)
        a.grid(alpha=0.3)
        a.legend()
    a1.set_ylabel('magnitud')
    plt.tight_layout()
    plt.savefig('figuras/espectro.png', dpi=150)

    # Una de frecuencia contra una de tiempo (figuras/frecuencia_vs_tiempo.png)
    plt.figure(figsize=(6, 5))
    for c, g in features.groupby('etiqueta'):
        plt.scatter(g['meseta'], g['banda_alta'], label=c, color=colores[c])
    plt.xlabel('meseta (tiempo)')
    plt.ylabel(f'energia de {BANDA_CORTE:.0f} a 25 Hz (frecuencia)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figuras/frecuencia_vs_tiempo.png', dpi=150)
    print("Figuras: features.png, scatter_matrix.png, espectro.png, frecuencia_vs_tiempo.png")
