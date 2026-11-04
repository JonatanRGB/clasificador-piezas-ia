# Retroalimentacion

Esto lo llena tu asesor despues de cada revision de avances (semanas 9, 14 y
17). Lo ves haciendo un `git pull` normal de tu repositorio. No lo edites:
crece con una seccion nueva en cada revision, las anteriores no se borran.

Los niveles son los de la rubrica de `evaluacion/individual`: **Excelente**,
**Bueno**, **Suficiente**, **Insuficiente**.

Evidencias, en este curso, es tu codigo en `codigo/`, tus datos en `datos/`,
tus figuras en `figuras/` y la demo del bucle de control.

---

### Nota rápida (2026-09-14)
Tu `README.md` sigue con "Dominio: Eleccion del dominio" sin actualizar. En la `BITACORA` primero eliges color (azul/rojo/amarillo) y luego, ya en la sección de semana 2, cambias a peso con la celda HX711, pero el cambio de dominio no queda explícito en ningún lado ni se refleja en el README. Actualiza el README con tu dominio final y deja una línea en la bitácora explicando que cambiaste de dominio y por qué.

### Nota rápida (2026-09-14) - s02
Cambiaste de sensor de color a una celda de carga (HX711, peso), y el `README.md` sigue sin reflejarlo ("Dominio: Trabajar en los sensores especificados" es un texto genérico). Además, tus "tres líneas de ejemplo" del bloque 1 traen texto mezclado con el dato (`13:30:27.47	Peso: 0.272 Kg  Alto`), justo lo que la pregunta 3 del mismo bloque pide evitar: el Arduino solo debe mandar el número. Vale la pena corregir el formato de línea antes de conectar el Arduino de verdad el miércoles, y actualizar el README con el dominio final.

### Nota rápida (2026-09-14) - s03
Tu `datos/datos.csv` tiene un renglón corrupto: la fila 13 dice literalmente `1.252,2,Alto3,0,0.0,alto`, que es el fin de una fila (`...,Alto`) pegado sin salto de línea al inicio de la siguiente (`3,0,0.0,alto`). A partir de ahí el archivo cambia de esquema a mitad de camino: pasa de tus tres columnas planeadas (`peso,ventana,etiqueta`, con etiquetas `Bajo`/`Medio`/`Alto`) a cuatro columnas distintas (`ventana,t,valor,etiqueta`) con `valor` siempre en `0.0` y una sola etiqueta `alto` repetida en 80 filas. Con eso `pd.read_csv` no lo va a poder leer bien, y aunque lo leyera, gran parte del archivo no son datos reales sino algo que parece una prueba de otro script que se coló en el mismo archivo. Conviene revisar `adquirir.py` (probablemente sea el `'a'` de append juntando corridas de código distinto) y volver a capturar limpio antes de seguir. Aparte, tu protocolo (bloque 1) no incluye la columna `t` de tiempo dentro de la ventana, que es la que pide el formato del curso; si tu HX711 da una sola lectura de peso por pasada en vez de una serie, vale la pena decirlo explícitamente en la bitácora, porque para tu equipo (6) sí importa que las columnas de control coincidan a partir de la semana 4. El `README.md` también sigue con el "Dominio:" genérico ("Trabajar en los sensores especificados") en vez de describir tu clasificación por peso.

### Nota rápida (2026-09-14) - s04
Tu bloque 1 tiene un problema importante: `codigo/limpiar.py` filtra las columnas `valor`, `t` y `etiqueta`, pero tu `datos/datos.csv` real tiene columnas distintas (`peso,ventana,etiqueta`) y además sigue con el mismo renglón corrupto que te comenté la semana pasada (la fila `1.252,2,Alto3,0,0.0,alto`, dos filas pegadas sin salto de línea). Con ese desajuste de columnas el script no puede estar corriendo sobre tus datos reales; probablemente lo adaptaste de un ejemplo sin ajustarlo al tuyo. Eso explica que no haya bloque 2 ni sección de Semana 4 en tu `BITACORA.md` (salta directo a la nota de "Aclaración de dudas en clase"). Antes de seguir: corrige la fila corrupta de `datos.csv` y ajusta `limpiar.py` a tus columnas reales (`peso`, no `valor`).

### Nota rápida (2026-09-21) - s05
No veo commits de la semana 05 (`s05 bloque 1`/`s05 bloque 2`). Si tuviste un problema, cuéntamelo para que quede en la bitácora.

### Nota rápida (2026-10-19) - s06
No veo commits de la semana 06 (`s06 bloque 1`/`s06 bloque 2`). Si tuviste un problema, cuéntamelo para que quede en la bitácora.

### Nota rápida (2026-10-19) - s07
No veo commits de la semana 07 (`s07 bloque 1`/`s07 bloque 2`). Si tuviste un problema, cuéntamelo para que quede en la bitácora.
