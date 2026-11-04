"""
Limpieza y normalizacion -> datos/datos_limpios.csv  (semana 4; en la semana 8 se
paso a funciones para que control.py, pca.py, clustering.py y autoencoder.py limpien
EXACTAMENTE igual que el entrenamiento).

Orden: 1) valores atipicos  2) linea base (3 primeras muestras)  3) media movil por ventana
       4) restar linea base   5) normalizacion min-max global
Salida con las MISMAS columnas que datos.csv: ventana, t, valor, etiqueta
Uso (desde la raiz del repo):  python codigo/limpiar.py
"""
import os
import json
import numpy as np
import pandas as pd

VALOR_MIN = -0.05   # kg (la tara deja lecturas un poco negativas)
VALOR_MAX = 1.0     # kg (capacidad de la celda)
K = 3               # media movil: 3 muestras = 60 ms a 50 Hz
N_BASE = 3          # muestras iniciales en 0 (antes de que caiga el material)
FS = 50.0           # Hz: 200 muestras en 4 s
ARCHIVO_NORM = 'datos/normalizacion.json'


def quitar_atipicos(datos):
    """Quita las filas con lecturas imposibles para la celda."""
    return datos[(datos['valor'] >= VALOR_MIN) & (datos['valor'] <= VALOR_MAX)].copy()


def filtrar_y_quitar_base(datos):
    """Media movil por ventana y resta de la linea base de cada ventana.
    La base se mide ANTES del filtro: con la media movil la muestra t=2 ya se
    mezcla con el inicio de la caida."""
    datos = datos.sort_values(['ventana', 't']).copy()
    base = datos[datos['t'] < N_BASE].groupby('ventana')['valor'].mean()
    datos['valor'] = datos.groupby('ventana')['valor'].transform(
        lambda s: s.rolling(window=K, center=True).mean().bfill().ffill()
    )
    datos['valor'] = datos['valor'] - datos['ventana'].map(base)
    return datos, base


def normalizar(datos, x_min, x_max):
    datos = datos.copy()
    datos['valor'] = (datos['valor'] - x_min) / (x_max - x_min)
    return datos


def cargar_normalizacion():
    with open(ARCHIVO_NORM) as f:
        p = json.load(f)
    return p['x_min'], p['x_max']


def limpiar(datos):
    """Limpia un DataFrame (ventana,t,valor,etiqueta) con la normalizacion YA guardada.
    Es lo que usan control.py, pca.py, clustering.py, autoencoder.py y evaluar.py."""
    x_min, x_max = cargar_normalizacion()
    limpios, _ = filtrar_y_quitar_base(quitar_atipicos(datos))
    return normalizar(limpios, x_min, x_max)


def limpiar_ventana(valores):
    """Limpia UNA ventana cruda (lista de pesos en kg, en orden) para el bucle de control."""
    datos = pd.DataFrame({'ventana': 0, 't': np.arange(len(valores)), 'valor': valores})
    return limpiar(datos)['valor'].to_numpy()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    datos = pd.read_csv('datos/datos.csv')
    crudos = datos.copy()

    fuera = datos[(datos['valor'] < VALOR_MIN) | (datos['valor'] > VALOR_MAX)]
    print(f"Lecturas imposibles eliminadas: {len(fuera)} "
          f"(ventanas {sorted(int(v) for v in fuera['ventana'].unique())})")
    datos = quitar_atipicos(datos)

    datos, base = filtrar_y_quitar_base(datos)
    print(f"Linea base: primera ventana {base.iloc[0]*1000:.2f} g, ultima {base.iloc[-1]*1000:.2f} g, "
          f"minima {base.min()*1000:.2f} g, maxima {base.max()*1000:.2f} g")

    # Normalizacion min-max GLOBAL (los mismos x_min y x_max para todas las ventanas)
    x_min, x_max = datos['valor'].min(), datos['valor'].max()
    with open(ARCHIVO_NORM, 'w') as f:
        json.dump({'x_min': float(x_min), 'x_max': float(x_max)}, f, indent=2)
    print(f"Normalizacion min-max: x_min = {x_min*1000:.2f} g, x_max = {x_max*1000:.2f} g "
          f"(guardados en {ARCHIVO_NORM})")
    datos = normalizar(datos, x_min, x_max)

    datos.to_csv('datos/datos_limpios.csv', index=False)
    print(f"Guardado datos/datos_limpios.csv ({len(datos)} filas)")

    os.makedirs('figuras', exist_ok=True)
    v = int(fuera['ventana'].iloc[0]) if len(fuera) else 0
    antes = crudos[crudos['ventana'] == v]
    despues = datos[datos['ventana'] == v]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    a1.plot(antes['t'] / FS, antes['valor'] * 1000)
    a1.set_title(f'Ventana {v} ({antes["etiqueta"].iloc[0]}) cruda')
    a1.set_ylabel('peso (g)')
    a2.plot(despues['t'] / FS, despues['valor'], color='C1')
    a2.set_title('Limpia: sin atipicos, filtrada, sin linea base y normalizada')
    a2.set_ylabel('valor normalizado')
    a2.set_xlabel('tiempo (s)')
    for a in (a1, a2):
        a.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figuras/limpieza.png', dpi=150)

    clases = sorted(datos['etiqueta'].unique())
    fig, ejes = plt.subplots(1, len(clases), figsize=(5 * len(clases), 4), sharey=True)
    for ax, c in zip(ejes, clases):
        tabla = datos[datos['etiqueta'] == c].pivot(index='t', columns='ventana', values='valor')
        ax.plot(tabla.index / FS, tabla.values, color='0.8', linewidth=0.7)
        ax.plot(tabla.index / FS, tabla.mean(axis=1), color='black', linewidth=2)
        ax.set_title(f'{c} ({tabla.shape[1]} ventanas)')
        ax.set_xlabel('tiempo (s)')
        ax.grid(alpha=0.3)
    ejes[0].set_ylabel('valor normalizado')
    plt.tight_layout()
    plt.savefig('figuras/galeria.png', dpi=150)
    print("Figuras guardadas: figuras/limpieza.png y figuras/galeria.png")
