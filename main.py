import cv2
from pyzbar.pyzbar import decode
import database
from image_processing import procesar_imagen, mostrar_mensaje_bienvenida


def bucle_principal():
        conexion = database.conectar_base_datos()
        cursor = conexion.cursor()
        cap = cv2.VideoCapture(0)
        exit_loop = False
        
        while True:
            success, img = cap.read()
            if not success:
                break
            
            for code in decode(img):
                decode_data = procesar_imagen(img, code)
                if decode_data:
                    database.insertar_datos(conexion, cursor, decode_data)
                    print("Dato insertado en la base de datos")
                    mostrar_mensaje_bienvenida(img)
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

if __name__ == "__main__":
    bucle_principal()
