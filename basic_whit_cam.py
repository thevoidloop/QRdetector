import cv2
import numpy as np
import mysql.connector
from pyzbar.pyzbar import decode
import pygame

# Inicializar pygame
pygame.init()
pygame.mixer.init()

beep_sound = pygame.mixer.Sound("beep.mp3")

cap = cv2.VideoCapture(2)

exit_loop = False
item_shop = False

price_total = 0.00

conexion = mysql.connector.connect(
    host="localhost",
    password="arduino",
    user="voidloop",
    database="db"
)

# Crear un cursor para interacturar con la base de datos
cursor = conexion.cursor()

while True:
        success, img = cap.read()

        if not success:
                break

        for code in decode(img):
                decode_data = code.data.decode("utf-8")

                rect_pts = code.rect

                if decode_data:
                        pts = np.array([code.polygon], np.int32)
                        cv2.polylines(img,[pts], True, (0,255,0),3)
                        # cv2.putText(img, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0),2)
                        img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
                        cv2.putText(img, "Bienvenido Daniel Marroquin", (100, 250), cv2.FONT_HERSHEY_DUPLEX, 1, (51, 255, 51), 2)
                        cv2.putText(img, "Sigue el proceso de compra desde tu app", (140, 270), cv2.FONT_HERSHEY_PLAIN, 1, (51, 255, 51), 1)
                        icon = cv2.imread('successful.png')
                        h, w, _ = icon.shape
                        img[150:150+h, 300:300+w] = icon
                        exit_loop = True
                        break

        if exit_loop:
                break

        cv2.imshow("image", img)
        cv2.waitKey(1)


cv2.imshow("image", img)
cv2.waitKey(2000)

for _ in range(10):
        cap.read()

while True:


        
        success, img = cap.read()
        if not success:
            break
        
        for code in decode(img):
                decode_data = code.data.decode("utf-8")
                rect_pts = code.rect

                if decode_data:
                        pts = np.array([code.polygon], np.int32)
                        cv2.polylines(img,[pts], True, (0,255,0),3)
                        # cv2.putText(img, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (159,191,42),2)

                        item_shop = True

                        price_total += float(str(decode_data))

                        for _ in range(10):  # leer y descartar 5 fotogramas
                                cap.read()


        
        cv2.putText(img, "Presione Q para terminar compra", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (41,78,242), 2)
        cv2.putText(img, "Total: Q"+str(price_total) , (50, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        cv2.imshow("image", img)

        if exit_loop:
               price_total = 0.00
               exit_loop = False

        if item_shop:
                beep_sound.play()
                cv2.waitKey(2000)
                item_shop = False

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir con la tecla 'q'
            break

consulta = "INSERT INTO scans(user_id, `timestamp`, status, price_total) VALUES(3, NOW(), 0, %s)"
valores = (str(price_total),)
cursor.execute(consulta, valores)
conexion.commit()
print("Dato insertado en la base de datos")


cap.release()
cursor.close()
conexion.close()
cv2.destroyAllWindows()