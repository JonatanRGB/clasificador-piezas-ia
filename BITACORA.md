# Bitácora del proyecto

## Semana 1 - Encuadre y configuración del entorno

### Antes de la clase

Realice la actualizacion y complete ya por completo todo el bloque 1 de la semana 1, solamente aun no aparecen hasta que ya lo actualice.
Ya realice el dirt para codigo, datos y las figuras, completando asi los datos necesarios para dejar ya terminado el bloque 1


Bloque 2
¿Cuál es la diferencia entre programar la regla y aprender la regla? Un ejemplo tuyo, no el de la guía. 
Programar una regla implica que debes de ingresar los datos sufientes para qie la maquina trabaje de manera automatica, tomando en cuenta los datos que va a trabajar la maquina y usando una serie de reglas que siempre nos daran un resultado, en cambio si aprendemos la regla implica que esos datos necesitaran resultados para que aprenda la maquina y as pueda diseñar esta sus propias reglas.

¿Cuál es tu dominio y cuáles son tus tres tipos de pieza?
color piezas azules, rojas y amarillas

Describe el bucle de control de tu sistema: qué mide tu sensor, qué tiene que decidir el modelo y qué haría el actuador con cada uno de tus tres tipos.
 Bucle de Control del Sistema (Dominio: Color)

Qué mide el sensor: Mide la lectura física del color de la pieza a su paso por el punto de control (los componentes de luz o niveles de intensidad que determinan su tonalidad).

Qué tiene que decidir el modelo: Evalúa la señal del sensor para determinar a cuál de las tres clases pertenece la pieza: Azul, Rojo o Amarillo.

Qué hace el actuador con cada tipo:

-Azul: El actuador se mantiene en su posición de reposo (inactivo) para dejar pasar la pieza azul por el trayecto principal.

-Rojo: El actuador se activa para accionar un mecanismo (como un pistón o brazo deslumbrador) y desviar la pieza roja hacia su canal o contenedor correspondiente.

-Amarillo: El actuador activa un mecanismo secundario (o realiza un pulso de desvío distinto) para enviar la pieza amarilla a su zona específica de almacenamiento.

## Semana 2 - La primera señal del sensor (U1)
Bloque 1

Qué sensor vas a usar y qué tipo de salida tiene.
voy a usar una celda de carga con modulo Hx711, con una salida de tipo digital serie de dos hilos. Cambie el sensor de color por uno de peso para tomar muestra 


Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso.
13:30:27.47	Peso: 0.272 Kg  Alto	
13:30:29.81	Peso: 0.258 kg	Medio
13:30:32.14	Peso: 0.212 kg	Bajo

Por qué el Arduino no puede mandar Serial.println("Leyendo...").
Se debe principalmente debido a que en python se espera que procese los daros de manera exacta, pero para que funcione necesita que empiece con un caracter especial y que ignore esas lineas. 
La otra manera mas facil es que Arduino se encargue de mandar los numeros y que python se encargue de imprimir los mensajes, en mi caso yo lo trabajado todo con aduino, y alli me imrime los datos y mensajes.

Bloque 2
¿Cuánto tarda tu pieza en cruzar frente al sensor? aproximadamente tarda en recorrer la banda de manera hipotetica unos 2 segundos.

Con ese tiempo, ¿qué delay() eliges para tener al menos 20 muestras del evento? Para obtener al menos $N = 20$ muestras durante un tiempo transcurrido de $T = 2.0\text{ s}$, el periodo entre muestras ($T_s$) se calcula dividiendo el tiempo total entre el número deseado de muestras: delay(100);

¿Cuántas muestras te da eso mientras la pieza pasa? Con un retardo de $100\text{ ms}$ entre lecturas, el sistema tomará exactamente 20 muestras mientras la pieza cruce la zona del sensor en los 2 segundos estimados

Nota de cambio de dominio: Se decidió modificar el sensor del proyecto, pasando del sensor de color (detector de tono azul/rojo/amarillo) a una celda de carga con amplificador HX711 para clasificación por peso. Este cambio se realizó para mejorar la repetibilidad y estabilidad de las mediciones físicas de las piezas

## Semana 3 - Recolección de datos etiquetados (U2)
Bloque 1

Las columnas exactas de tu datos.csv, con el nombre de cada una y qué guarda.
Las columnas en las que se van a clasificar mis datos son las siguienstes: 
peso: Guarda la lectura física numérica del peso capturada por la celda de carga HX711 (en kilogramos, ej. 0.272).

ventana: Guarda el identificador numérico de la ventana de tiempo o ráfaga de muestras asociada al paso de una pieza específica (ej. 0, 1, 2).

etiqueta: Guarda la categoría asignada a la pieza en minúsculas y sin acentos según los umbrales de peso definidos (ej. bajo, medio, alto).

Tus tres etiquetas, escritas tal como van a aparecer en el archivo (una palabra, minúsculas, sin acentos).
bajo

medio

alto

Cinco filas de ejemplo de tu tabla, con valores plausibles para tu sensor.
peso,ventana,etiqueta
0.002,0,bajo
0.272,0,bajo
0.650,1,medio
0.758,1,medio
1.345,2,alto

Nota: el error de por que se sobre escribio el codigo fue debido a que se empezo a correr el IDE de arduino junto al ultimo dato que se corrio, pero al eliminar ese segmento corrupto ya no deberia de ejecutar ese error.

Bloque 2

Cuántas ventanas por clase vas a capturar.
Capturaré 10 ventanas por clase, dando un total de 30 ventanas para todo el dataset (10 para bajo, 10 para medio y 10 para alto).  
Como cada ventana registra 20 muestras, tendré un total de 200 lecturas puntuales de peso por categoría.  

En qué orden.
Lo haré de forma intercalada: bajo, medio, alto

Cómo vas a mantener pareja la velocidad de la mano, en concreto: qué vas a marcar, medir o fijar.
Marcaré dos líneas en la plataforma separadas a una distancia fija, la pieza iniciará el recorrido en la marca A con el primer pulso sonoro y deberá cruzar la marca B exactamente al escuchar el segundo pulso.

A qué distancia del sensor va a pasar la pieza.
La pieza pasará en contacto físico directo (0 cm), deslizándose centrada sobre la base de la celda de carga. Al ser un sensor mecánico (HX711), es indispensable que la pieza apoye todo su peso directamente sobre la plataforma durante su paso.

## Aclaracion de dudas en clase sobre el funcionamiento y correccion de las tablas para la recopilacion de datos
se definio como corregir las señales, ademas de como podremos diferenciar ruido de anomalias y calcular nuestros datos estadisticos


## correciones de REVISION.md 
corregi los datos corruptos de la captura de datos, ademas de ajustar el formato de las ventanas que se genere en la semana 3 para que asi los datos generados en la semana 4 no se corrompan

## volver a hacer las correcciones
al parecer la razon por la que mis datos salian corruptos en 0 fue debido a que el anterior modulo hx711 se habia quemado en un de las primeras purueba y ahora el modulo actual si funciona y me genera las ventanas con los datos de peso que deben de ser, solamente debo de corregir la entrada de la clasificacion de datos para que uncione correctamente todos los datos y los pueda depurar para la parte de limpiar que ya tenia hecha, pero debido a que estaban mal los datos la volvere a hacer

## Semana 4 - Limpieza y normalización de señales (U2)

Bloque 1
¿Qué ruido ves y de dónde crees que viene?
En la parte estable la lectura sube y baja alrededor de ±1 g entre muestras. Es ruido eléctrico del HX711 y de los cables de la celda.
También hay lecturas sueltas absurdas (8 kg o -1.5 kg) que son errores de lectura, no ruido.

¿Cuál es el rango físico de tu sensor y qué valores descartaste?
La celda mide de 0 a 1 kg; por la tara salen lecturas un poco
negativas, así que acepto de -0.05 a 1.0 kg. Eliminé 17 lecturas, une en cada una de 17 ventanas, así que ninguna ventana se perdió completa.

¿Qué tamaño de filtro usaste y por qué?
Media móvil de k = 3 muestras (60 ms a 50 Hz). El pico al caer dura unos 100 ms; con k más grande se aplasta. Se aplica por ventana (groupby) para no mezclar ventanas, y los NaN de las orillas se rellenan con el valor válido más cercano.

Bloque 2
¿Cuánto se movió la línea base entre la primera y la última ventana?
La primera empezó en -0.23 g y la última en -1.10 g; en toda la sesión estuvo entre -1.90 y 1.67 g. Es poco frente a mis piezas (14 a 55 g), pero en el PLA ya es más del 10 %, por eso la corrijo. La calculo con las 3 primeras muestras de cada ventana (antes de que caiga el material) y antes del filtro, porque la media móvil mezcla la muestra 2 con el inicio de la caída.

¿Qué normalización elegiste y por qué?
Min-max global: x' = (x - x_min)/(x_max - x_min), con x_min = -1.73 g y x_max = 76.53 g, guardados en datos/normalizacion.json para usar los mismos en producción. Es global porque si normalizara cada ventana sola, todas llegarían a 1 y se perdería la diferencia de peso, que es lo que distingue a mis materiales.

Después de limpiar, ¿las ventanas de la misma clase se parecen más?
Sí: desaparece el pico atípico, la base queda en 0 y baja el ruido. ![limpieza](figuras/limpieza.png

### Avance del proyecto

Pasos de limpieza en orden y por qué.
Quitar lecturas imposibles (primero, porque un 8 kg dentro del filtro contamina a sus vecinas). 2) Medir la línea base. 3) Media móvil por ventana. 4) Restar la base. 5) Normalizar y guardar x_min y x_max.

¿Las ventanas de la misma clase son más parecidas? (figura galería)
[galeria](figuras/galeria.png) Los tres materiales quedan en niveles separados (PLA ≈ 0.20, resina ≈ 0.53, MDF ≈ 0.72) y no se enciman.

Ventanas descartadas. Ninguna completa; siguen 40 por clase.

¿Qué harás si dos clases se enciman?
Revisaría cómo suelto la pieza (altura, posición) y repetiría esas capturas; si siguen encimadas, usaría otra característica además del peso o un segundo sensor.

Realice pruebas en la maquina de desgaste del laboratorio de superficies y triboligia, debido a que alli es donde empece a trabajar con un sistema parecido al que estoy trabajando actualmente co esta celda de carga

## Semana 5 - Características en el dominio del tiempo (U2)

Bloque 1

| Característica | Por qué debería distinguir mis clases |
|---|---|
| media | Es casi el peso promedio de la ventana: 14, 40 y 55 g son muy distintos |
| desv | La caída y el rebote mueven más la señal en piezas más pesadas |
| máximo | El pico al caer: 22, 50 y 68 g |
| rango | Máximo menos mínimo; no le afecta la línea base |
| meseta (propia) | El peso ya asentado (mediana de la segunda mitad de la ventana) |
| sobrepaso (propia) | Cuánto se pasa el golpe del peso final (máximo − meseta) |
| mínimo, energía, duración | Las calculo, pero espero que no sirvan |

Predicción: ¿cuál será la mejor y cuál la más inútil?
La mejor será la meseta (es el peso directo) y la más inútil la duración, porque la pieza se queda encima toda la ventana.

Bloque 2

¿Cuántas filas y columnas tiene features.csv y por qué? 
 120 filas (una por ventana: 40 x 3 materiales) y 8 columnas (ventana, 6 características y etiqueta).

¿Qué par de características separa mejor tus clases?
Meseta contra sobrepaso: la meseta separa sola los tres materiales y el sobrepaso agrega cómo cayó la pieza. También probé media–rango y máximo–desv; también separan porque todas dependen del peso.

¿Hay clases encimadas? ¿Qué harás?
No hay clases encimadas.

### Avance del proyecto
Qué características quedaron y cuáles descartaste, con razones.
Quedaron: media, desv, máximo, rango, meseta y sobrepaso.
 mínimo (≈0.02 en todas: todas empiezan en la base), energía (repite a la media, es casi media²) y duración (≈196 de 200 en todas). Están en la lista DESCARTADAS de features.py.

¿Cuál separa mejor? ¿Coincide con tu predicción?
La meseta (PLA 0.20, resina 0.54, MDF 0.72, con desviaciones de 0.01 a 0.03). Sí coincidió, y la duración no sirvió, como predije.

¿Recapturaste?
No hizo falta.

## Semana 6 - Características en el dominio de la frecuencia (U2)

Bloque 1

Tu frecuencia de muestreo fs.
fs = 50 Hz (200 muestras en 4 s, una cada 20 ms).

Tu frecuencia de Nyquist y qué significa.
25 Hz. No puedo ver nada que oscile más rápido que 25 Hz; si apareciera, sería aliasing.

Tu resolución Δf.
Δf = fs/N = 50/200 = 0.25 Hz.

¿Esperas que tus clases se distingan en frecuencia?
Poco. Mi señal es casi un escalón (cae y se queda), así que casi toda la energía está en frecuencias bajas. Quizá solo aporte el rebote del golpe (6 a 9 Hz).

Bloque 2

Frecuencia dominante y si tiene sentido físico.
Salta entre 0.25 y 9 Hz sin patrón por clase; no tiene sentido físico porque el espectro de un escalón no tiene un pico claro.

¿Las features de frecuencia separan tus clases?
El centroide no (≈7.2 Hz en las tres). La energía total y la banda baja sí, pero solo porque repiten el peso. La banda alta (3–25 Hz) sí aporta algo nuevo: la energía del rebote (PLA ≈ 9, resina ≈ 55, MDF ≈ 106). Elegí el corte en 3 Hz viendo mis espectros.

¿Te las quedas o las quitas?
Me quedo solo con banda_alta; quito frecuencia dominante, centroide, energía total y banda baja (están en DESCARTADAS).

### Avance del proyecto

¿La frecuencia te sirvió? Explicación física.
Poco, como predije: la señal es un escalón y lo que distingue a mis piezas es el peso. Solo la banda alta agrega el golpe.

Lista final de características para la semana 7.
media, desv, máximo, rango, meseta, sobrepaso, banda_alta.
Dataset congelado, versión 1: 7 características, 120 ventanas, 40 por clase.

Predicción de separación con el conjunto final.
Las tres clases se van a separar casi perfecto, porque la meseta ya no se encima.

## Semana 7 - Entrenamiento del clasificador (U2)

Bloque 1
Número de ejemplos de entrenamiento y de prueba.
120 ventanas -> 90 de entrenamiento y 30 de prueba (75/25, estratificado: 10 de prueba por clase).

Con qué algoritmo empiezas y por qué.
kNN (k = 5), porque mis clases se separan por distancia (el peso).Lo comparo con un árbol de decisión porque se puede leer.

¿Por qué un modelo con 100 % en entrenamiento puede ser inútil?
Porque pudo memorizar los ejemplos; lo que importa es cómo le va con datos que nunca vio.

Bloque 2
Exactitud en prueba.
 R:  (pega la tabla)

| Modelo | Entrenamiento | Prueba |
|---|---|---|
| kNN (k=5) | 1.000 | 0.967 |
| Árbol (max_depth=3) | 1.000 | 1.000 |

El par de clases que más se confunde.
El árbol no confunde nada. El kNN confundió una ventana de MDF con resina (el MDF más ligero queda cerca de la resina más pesada).


¿Coincide con tu predicción de la semana 6?
Sí, predije separación casi perfecta.

### Avance del proyecto

 P1: Algoritmo elegido y por qué ganó.
 R:  Árbol de decisión (max_depth = 3): mejor en prueba que kNN y se puede
     leer. Aprendió 3 preguntas: si banda_alta es baja -> PLA; si no, si
     la media es baja -> resina; si no -> MDF.

Exactitud de entrenamiento y de prueba (y si hay diferencia grande).
1.000 y 1.000; no hay diferencia.

¿Qué confunde el modelo y por qué?
Nada en prueba. El riesgo está en el MDF más ligero, que se acerca a resina.

Si el resultado es muy bueno, ¿qué evidencia hay de que no es fuga de datos?
Quité la columna ventana, el escalador se ajustó solo con  entrenamiento y la prueba nunca se usó para entrenar. El 100 %   explica físicamente: los materiales pesan 14, 40 y 55 g y el ruido esnde ±1 g. El riesgo real es que todo se capturó igual (simulado); lo veré en la banda.

## Semana 8 - Redes neuronales y primer bucle de control (U2)

Bloque 1
Tabla: modelo semana 7, red de 10 y red de 50 neuronas.

| Modelo | Entrenamiento | Prueba |
|---|---|---|
| Árbol (semana 7) | 1.000 | 1.000 |
| Red de 10 neuronas | 1.000 | 1.000 |
| Red de 50 neuronas | 1.000 | 1.000 |

¿Qué modelo se queda y por qué?
El árbol: empata con las redes y es más simple y explicable.

¿Por qué la red no necesariamente gana con 90 ejemplos?
Porque no hay más patrón que aprender: el árbol ya separa perfecto con 3 preguntas, y una red de 50 neuronas tiene muchos más parámetros que ejemplos, así que puede memorizar en vez de generalizar.

Bloque 2
Tabla de acciones (carácter, clase, efecto físico, justificación).

| Carácter | Clase | Efecto físico | Por qué |
|---|---|---|---|
| A | resina | se prende el LED rojo (pin 5) | un color distinto por material, fácil de ver en el video |
| B | mdf | se prende el LED amarillo (pin 6) | — |
| C | pla | se prende el LED azul (pin 7) | — |
| 0 | reposo | se apagan los LEDs | después de 0.5 s |

     Como actuador uso 3 LEDs en lugar del servo: así cada decisión se ve
     con un color y no necesito montar el mecanismo de desvío.

¿Cómo evitas que el bucle procese distinto que el entrenamiento?
Convertí limpiar.py y features.py en funciones (limpiar_ventana y calcular_features) que control.py importa. Así el bucle limpia exactamente igual (evita el training-serving skew). Comprobé que datos_limpios.csv sale idéntico que antes del cambio.

link del video: https://drive.google.com/file/d/1sZ3g2q0XMKZx1mSm2Lg9XinVb8rDgkI-/view?usp=sharing 

### Avance del proyecto
Tabla de acciones.   (la misma de arriba)
Exactitud en vivo contra la del CSV. 95%
Problemas al conectar todo y cómo los resolví.

Ya logre hacer push en GitHub

este es el procedimiento para hacer push:
- para hacer un push primero edito mi archivo
- luego hago git add
- luego git commit
- luego git push

