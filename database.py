import mysql.connector

def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        password="arduino",
        user="voidloop",
        database="db"
    )

def insertar_datos(conexion, cursor, decode_data):
    consulta = "INSERT INTO scans(user_id, `timestamp`, status) VALUES(%s, NOW(), 0)"
    valores = (int(str(decode_data)),)
    cursor.execute(consulta, valores)
    conexion.commit()
