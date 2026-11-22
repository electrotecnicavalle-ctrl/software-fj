"""
registro.py
Configura el archivo de logs donde se guardan todos los eventos y errores.
No se usa base de datos: el único archivo que se escribe es el log.
"""

import logging  # Módulo estándar de Python para registrar eventos
import os  # Para construir la ruta del archivo de logs

# Ruta del archivo de logs: carpeta "logs" junto a la raíz del proyecto
RUTA_LOGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe en archivo y en consola."""
    # Creamos la carpeta de logs si no existe
    os.makedirs(RUTA_LOGS, exist_ok=True)
    # Obtenemos (o creamos) el logger con el nombre dado
    logger = logging.getLogger(nombre)
    # Si ya tiene manejadores, no los duplicamos
    if logger.handlers:
        return logger
    # Nivel mínimo: registramos desde INFO en adelante
    logger.setLevel(logging.INFO)
    # Formato: fecha, nivel y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    # Manejador de archivo (UTF-8 para tildes y eñes)
    archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)
    # Manejador de consola para ver los eventos mientras se ejecuta
    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(consola)
    return logger


# Logger compartido por todos los módulos
log = obtener_logger()
