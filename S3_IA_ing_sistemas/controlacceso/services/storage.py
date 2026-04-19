import os
from models.registro import Registro

ARCHIVO = "contro.txt"


def guardar_registro(registro: Registro):
    """Guarda un registro en contro.txt validando serial único"""
    if registro.serial_computador and _serial_existe(registro.serial_computador):
        raise ValueError(f"Serial {registro.serial_computador} ya registrado")
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(registro.to_line() + "\n")


def obtener_registros(filtro_nombre=None, filtro_fecha=None, limite=50):
    """Obtiene registros con filtros opcionales, orden descendente"""
    if not os.path.exists(ARCHIVO):
        return []
    
    resultados = []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        for linea in f:
            if not linea.strip():
                continue
            reg = Registro.from_line(linea.strip())
            
            if filtro_nombre and filtro_nombre.lower() not in reg.nombre_empleado.lower():
                continue
            if filtro_fecha and filtro_fecha not in reg.fecha_hora_entrada:
                continue
                
            resultados.append(reg)
    
    return resultados[-limite:][::-1]


def obtener_por_indice(indice: int):
    """Obtiene un registro por su índice de línea (0-based)"""
    if not os.path.exists(ARCHIVO):
        return None
    
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]
        if 0 <= indice < len(lineas):
            return Registro.from_line(lineas[indice])
    return None


def _serial_existe(serial: str):
    """Verifica si un serial ya existe en el archivo"""
    if not serial or not os.path.exists(ARCHIVO):
        return False
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return any(f'"{serial}"' in linea for linea in f)