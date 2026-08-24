import cv2
import numpy as np

# Abrir cámara
camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("No se pudo abrir la cámara")
    exit()

print("Cámara iniciada")
print("Presiona Q para salir")

while True:

    ret, frame = camara.read()

    if not ret:
        break

    # Suavizar un poco la imagen
    frame_suave = cv2.GaussianBlur(
        frame,
        (5, 5),
        0
    )

    # Convertir BGR a HSV
    hsv = cv2.cvtColor(
        frame_suave,
        cv2.COLOR_BGR2HSV
    )

    # ==============================
    # RANGO DE COLOR AZUL
    # ==============================

    azul_bajo = np.array([90, 80, 50])
    azul_alto = np.array([135, 255, 255])

    mascara = cv2.inRange(
        hsv,
        azul_bajo,
        azul_alto
    )

    # Limpiar pequeños puntos
    kernel = np.ones((5, 5), np.uint8)

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_OPEN,
        kernel
    )

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Buscar contornos
    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detectado = False

    for contorno in contornos:

        area = cv2.contourArea(contorno)

        # Ignorar objetos demasiado pequeños
        if area > 500:

            x, y, w, h = cv2.boundingRect(contorno)

            # Una lapicera suele ser alargada
            relacion = max(w, h) / max(1, min(w, h))

            if relacion > 2:

                detectado = True

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "Posible lapicera punta azul",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

    if not detectado:

        cv2.putText(
            frame,
            "Buscando lapicera con punta azul...",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    # Mostrar cámara
    cv2.imshow(
        "Reconocimiento de lapicera",
        frame
    )

    # Mostrar máscara de azul
    cv2.imshow(
        "Deteccion de color azul",
        mascara
    )

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break

camara.release()
cv2.destroyAllWindows()