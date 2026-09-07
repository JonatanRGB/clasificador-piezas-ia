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



### Avance del proyecto

Realice pruebas en la maquina de desgaste del laboratorio de superficies y triboligia, debido a que alli es donde empece a trabajar con un sistema parecido al que estoy trabajando actualmente co esta celda de carga


Ya logre hacer push en GitHub

este es el procedimiento para hacer push:
- para hacer un push primero edito mi archivo
- luego hago git add
- luego git commit
- luego git push

