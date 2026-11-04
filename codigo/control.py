"""
Bucle de control: celda de carga -> Python -> detector + clasificador -> Arduino
Semana 8: captura, limpia, calcula caracteristicas, decide y actua.
Uso: carga codigo/control/control.ino en el Arduino y luego
     python codigo/control.py          (Ctrl+C para salir)
"""
import os
import sys
import time
import joblib
try:
    import serial
except ImportError:      # permite importar decidir() sin pyserial
    serial = None
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from limpiar import limpiar_ventana          # la MISMA limpieza que limpiar.py
from features import calcular_features       # las MISMAS caracteristicas que features.py

PUERTO = 'COM3'          # <-- tu puerto
BAUDIOS = 115200
N_MUESTRAS = 200         # 4 s a 50 Hz, igual que en adquirir.py

ordenes = {
    'resina': b'A',      # LED rojo
    'mdf': b'B',         # LED amarillo
    'pla': b'C',         # LED azul
}


def capturar_ventana(ser, n):
    """Igual que adquirir.py, convertido en funcion: n lecturas en kg."""
    ser.reset_input_buffer()
    valores = []
    while len(valores) < n:
        linea = ser.readline().decode('utf-8', errors='ignore').strip()
        try:
            valores.append(float(linea.split(',')[0]))
        except ValueError:
            continue      # ignora lineas que no son numero
    return valores


def actuar(ser, orden, texto):
    ser.write(orden)
    print(texto)
    time.sleep(0.5)
    ser.write(b'0')       # reposo


clf = joblib.load('modelo.pkl')


def decidir(crudo):
    """Pasos 2 a 4 del bucle. Devuelve (clase, texto)."""
    limpio = limpiar_ventana(crudo)                          # 2. limpiar igual que limpiar.py
    fila = pd.DataFrame([calcular_features(limpio)])         # 3. caracteristicas, mismo orden
    X = clf['escalador'].transform(fila[clf['columnas']])    # 4. decidir
    clase = clf['modelo'].predict(X)[0]
    return clase, clase

if __name__ == '__main__':
    ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    time.sleep(2)            # el Arduino se reinicia al abrir el puerto
    try:
        while True:
            input("\nEnter y suelta el siguiente material...")
            crudo = capturar_ventana(ser, N_MUESTRAS)        # 1. capturar
            decision, texto = decidir(crudo)                 # 2-4. limpiar, caracteristicas, decidir
            actuar(ser, ordenes[decision], f"{texto} -> {ordenes[decision].decode()}")   # 5. actuar
    except KeyboardInterrupt:
        print("\nFin del bucle")
    finally:
        ser.write(b'0')
        ser.close()
