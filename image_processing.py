import cv2
import numpy as np


def procesar_imagen(img, code):
    decode_data = code.data.decode("utf-8")
    rect_pts = code.rect
    if decode_data:
        pts = np.array([code.polygon], np.int32)
        cv2.polylines(img, [pts], True, (0, 255, 0), 3)
        cv2.putText(img, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    return decode_data

def mostrar_mensaje_bienvenida(img):
    cv2.putText(img, "Bienvenido Daniel Marroquin", (100, 250), cv2.FONT_HERSHEY_DUPLEX, 1, (51, 255, 51), 2)
    cv2.putText(img, "Sigue el proceso de compra desde tu app", (140, 270), cv2.FONT_HERSHEY_PLAIN, 1, (51, 255, 51), 1)
    icon = cv2.imread('successful.png')
    h, w, _ = icon.shape
    img[150:150 + h, 300:300 + w] = icon

