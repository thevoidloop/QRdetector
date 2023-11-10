import cv2
import numpy as np
from pyzbar.pyzbar import decode

img = cv2.imread("img/qr1.png")


for code in decode(img):
        print(code.data.decode("utf-8")) 


cv2.imshow("image", img)
cv2.waitKey(3000)

 
