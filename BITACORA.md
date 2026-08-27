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

Qué sensor vas a usar y qué tipo de salida tiene.
voy a usar una celda de carga con modulo Hx711, con una salida de tipo digital serie de dos hilos. Cambie el sensor de color por uno de peso para tomar muestra 


Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso.
13:30:27.47	Peso: 0.272 Kg  Alto	
13:30:29.81	Peso: 0.258 kg	Medio
13:30:32.14	Peso: 0.212 kg	Bajo

Por qué el Arduino no puede mandar Serial.println("Leyendo...").
Se debe principalmente debido a que en python se espera que procese los daros de manera exacta, pero para que funcione necesita que empiece con un caracter especial y que ignore esas lineas. 
La otra manera mas facil es que Arduino se encargue de mandar los numeros y que python se encargue de imprimir los mensajes, en mi caso yo lo trabajado todo con aduino, y alli me imrime los datos y mensajes.

### Avance del proyecto

(aquí va lo que le agregaste a tu sistema)

Ya logre hacer push en GitHub

este es el procedimiento para hacer push:
- para hacer un push primero edito mi archivo
- luego hago git add
- luego git commit
- luego git push

