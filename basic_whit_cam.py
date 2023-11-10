import cv2
import numpy as np
import mysql.connector
from pyzbar.pyzbar import decode


cap = cv2.VideoCapture(2)

exit_loop = False

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
                        cv2.putText(img, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0),2)
                        consulta = "INSERT INTO scans(user_id, `timestamp`, status) VALUES(%s, NOW(), 0)"
                        valores = (int(str(decode_data)),)
                        cursor.execute(consulta, valores)
                        conexion.commit()
                        print("Dato insertado en la base de datos")
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
cv2.waitKey(0)

cap.release()
cursor.close()
conexion.close()
cv2.destroyAllWindows()