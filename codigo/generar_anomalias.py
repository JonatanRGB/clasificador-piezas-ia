"""
Genera ventanas SIMULADAS de piezas raras (sensor HX711 danado; uso autorizado por el profesor).
Mismo protocolo y formato que datos.csv: 200 muestras en 4 s (50 Hz), valor en kg.

Salida:
  datos/anomalias_crudas.csv   ventana,t,valor,etiqueta   (etiqueta = anomalia)
  datos/anomalias_tipos.csv    ventana,tipo               (que objeto era cada ventana)

Semana 10: objetos ajenos (tornillo, goma, carton) -> 9 ventanas
Uso:  python codigo/generar_anomalias.py
"""
import os
import csv
import numpy as np

SEMILLA = 7
N_POR_TIPO = 3
N_MUESTRAS = 200
FS = 50.0
PRIMERA_VENTANA = 1000   # numeracion aparte para no confundirlas con datos.csv

# tipo: (peso estable kg, pico al caer kg, frecuencia del rebote Hz, tau del rebote en muestras)
TIPOS = {
    # --- semana 10: objetos que no son ninguna de mis piezas ---
    'tornillo':          (0.008, 0.016, 14.0, (2, 4)),    # metal: ligero y rebote rapido
    'goma':              (0.020, 0.021, 4.0, (2, 4)),     # absorbe el golpe: casi sin pico
    'carton':            (0.005, 0.007, 8.0, (3, 6)),     # muy ligero
}

rng = np.random.default_rng(SEMILLA)
t = np.arange(N_MUESTRAS)


def ventana_simulada(peso, pico, f_osc, tau_rango):
    peso = peso * rng.normal(1, 0.04)
    pico = max(pico * rng.normal(1, 0.08), peso)
    n_ceros = int(rng.integers(3, 7))
    subida = int(rng.integers(1, 3))
    tau = rng.uniform(*tau_rango)
    f = f_osc * rng.normal(1, 0.1)
    x = np.zeros(N_MUESTRAS)
    s = np.arange(1, subida + 1)
    x[n_ceros:n_ceros + subida] = pico * s / subida
    i0 = n_ceros + subida
    k = t[i0:] - i0
    x[i0:] = peso + (pico - peso) * np.exp(-k / tau) * np.cos(2 * np.pi * f * k / FS)
    x[i0:] += peso * rng.normal(0, 0.01) * (1 - np.exp(-k / 40))
    x = x + rng.normal(0, 0.0005) + rng.normal(0, 0.0008, N_MUESTRAS)
    return np.round(x, 4)


os.makedirs('datos', exist_ok=True)
ventana = PRIMERA_VENTANA
with open('datos/anomalias_crudas.csv', 'w', newline='', encoding='utf-8') as fc, \
     open('datos/anomalias_tipos.csv', 'w', newline='', encoding='utf-8') as ft:
    wc, wt = csv.writer(fc), csv.writer(ft)
    wc.writerow(['ventana', 't', 'valor', 'etiqueta'])
    wt.writerow(['ventana', 'tipo'])
    for tipo, (peso, pico, f_osc, tau) in TIPOS.items():
        for _ in range(N_POR_TIPO):
            for ti, v in zip(t, ventana_simulada(peso, pico, f_osc, tau)):
                wc.writerow([ventana, ti, v, 'anomalia'])
            wt.writerow([ventana, tipo])
            ventana += 1

print(f"datos/anomalias_crudas.csv: {ventana - PRIMERA_VENTANA} ventanas de piezas raras (SIMULADAS)")
