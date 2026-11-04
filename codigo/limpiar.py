"""
Semana 4: limpieza y normalizacion -> datos/datos_limpios.csv
Orden: 1) valores atipicos  2) media movil por ventana  3) linea base  4) normalizacion
Salida con las MISMAS columnas que datos.csv: ventana, t, valor, etiqueta
Uso (desde la raiz del repo):  python codigo/limpiar.py
"""
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

VALOR_MIN = -0.05   # kg (la tara deja lecturas un poco negativas)
VALOR_MAX = 1.0     # kg (capacidad de la celda; ajustala a la tuya)
K = 3               # media movil: 3 muestras = 60 ms a 50 Hz
N_BASE = 3          # muestras iniciales en 0 (antes de que caiga el material)

datos = pd.read_csv('datos/datos.csv')
crudos = datos.copy()   # copia para la figura de antes/despues

# ---------------- Bloque 1 ----------------
# 1. Valores atipicos (lecturas imposibles para la celda)
fuera = datos[(datos['valor'] < VALOR_MIN) | (datos['valor'] > VALOR_MAX)]
print(f"Lecturas imposibles eliminadas: {len(fuera)} (ventanas {sorted(int(v) for v in fuera['ventana'].unique())})")
datos = datos[(datos['valor'] >= VALOR_MIN) & (datos['valor'] <= VALOR_MAX)].copy()

# La linea base se mide aqui, ANTES del filtro: con la media movil, la muestra t=2
# ya se mezcla con el inicio de la caida y la base saldria inflada.
base = datos[datos['t'] < N_BASE].groupby('ventana')['valor'].mean()

# 2. Media movil por ventana + orillas rellenadas con el valor mas cercano
datos['valor'] = datos.groupby('ventana')['valor'].transform(
    lambda s: s.rolling(window=K, center=True).mean().bfill().ffill()
)

# ---------------- Bloque 2 ----------------
# 3. Linea base: promedio de las primeras N_BASE muestras de cada ventana
#    (los ms en que la plataforma esta vacia mientras cae el material), restada a toda la ventana
print(f"Linea base: primera ventana {base.iloc[0]*1000:.2f} g, ultima {base.iloc[-1]*1000:.2f} g, "
      f"minima {base.min()*1000:.2f} g, maxima {base.max()*1000:.2f} g")
datos['valor'] = datos['valor'] - datos['ventana'].map(base)

# 4. Normalizacion min-max GLOBAL (los mismos x_min y x_max para todas las ventanas).
#    No se normaliza cada ventana por separado: eso borraria la diferencia de peso
#    entre materiales, que es justo lo que distingue a mis clases.
x_min = datos['valor'].min()
x_max = datos['valor'].max()
datos['valor'] = (datos['valor'] - x_min) / (x_max - x_min)
with open('datos/normalizacion.json', 'w') as f:
    json.dump({'x_min': float(x_min), 'x_max': float(x_max)}, f, indent=2)
print(f"Normalizacion min-max: x_min = {x_min*1000:.2f} g, x_max = {x_max*1000:.2f} g "
      f"(guardados en datos/normalizacion.json para usarlos igual en produccion)")

datos.to_csv('datos/datos_limpios.csv', index=False)
print(f"Guardado datos/datos_limpios.csv ({len(datos)} filas, columnas {list(datos.columns)})")

# ---------------- Figuras ----------------
os.makedirs('figuras', exist_ok=True)

# Misma ventana antes y despues (figuras/limpieza.png)
v = int(fuera['ventana'].iloc[0]) if len(fuera) else 0   # de preferencia una con atipico
antes = crudos[crudos['ventana'] == v]
despues = datos[datos['ventana'] == v]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
a1.plot(antes['t'] / 50, antes['valor'] * 1000)
a1.set_title(f'Ventana {v} ({antes["etiqueta"].iloc[0]}) cruda')
a1.set_ylabel('peso (g)')
a2.plot(despues['t'] / 50, despues['valor'], color='C1')
a2.set_title('Limpia: sin atipicos, filtrada, sin linea base y normalizada')
a2.set_ylabel('valor normalizado')
a2.set_xlabel('tiempo (s)')
for a in (a1, a2):
    a.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figuras/limpieza.png', dpi=150)

# Galeria por clase: ventanas en gris y su promedio en negro (figuras/galeria.png)
clases = sorted(datos['etiqueta'].unique())
fig, ejes = plt.subplots(1, len(clases), figsize=(5 * len(clases), 4), sharey=True)
for ax, c in zip(ejes, clases):
    tabla = datos[datos['etiqueta'] == c].pivot(index='t', columns='ventana', values='valor')
    ax.plot(tabla.index / 50, tabla.values, color='0.8', linewidth=0.7)
    ax.plot(tabla.index / 50, tabla.mean(axis=1), color='black', linewidth=2)
    ax.set_title(f'{c} ({tabla.shape[1]} ventanas)')
    ax.set_xlabel('tiempo (s)')
    ax.grid(alpha=0.3)
ejes[0].set_ylabel('valor normalizado')
plt.tight_layout()
plt.savefig('figuras/galeria.png', dpi=150)
print("Figuras guardadas: figuras/limpieza.png y figuras/galeria.png")
