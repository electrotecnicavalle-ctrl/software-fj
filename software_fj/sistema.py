"""
sistema.py
Gestor central: guarda clientes, servicios y reservas en listas internas
(sin base de datos) y envuelve cada operación en manejo de excepciones
para que el programa nunca se detenga.
"""

from .cliente import Cliente
from .reserva import Reserva
from .registro import log
from .excepciones import SoftwareFJError


class SistemaFJ:
    """Administra todas las entidades de Software FJ en memoria."""

    def __init__(self):
        # Listas internas que reemplazan a la base de datos
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, **datos):
        """Crea un cliente; si falla, registra el error y devuelve None."""
        try:
            cliente = Cliente(**datos)
        except SoftwareFJError as error:
            # Error previsto por nuestras validaciones
            log.error(f"Cliente rechazado: {error}")
            return None
        except TypeError as error:
            # Faltan argumentos o sobran: error de programación/uso
            log.error(f"Cliente rechazado por parámetros incorrectos: {error}")
            return None
        else:
            # Sin errores: lo guardamos en la lista
            self.clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente}")
            return cliente

    def agregar_servicio(self, clase, *args, **kwargs):
        """Crea un servicio del tipo indicado (ReservaSala, AlquilerEquipo, Asesoria)."""
        try:
            servicio = clase(*args, **kwargs)
        except (SoftwareFJError, TypeError) as error:
            log.error(f"Servicio rechazado ({clase.__name__}): {error}")
            return None
        self.servicios.append(servicio)
        log.info(f"Servicio creado: {servicio}")
        return servicio

    def crear_reserva(self, cliente, servicio, horas):
        """Crea una reserva y la deja pendiente."""
        try:
            reserva = Reserva(cliente, servicio, horas)
        except SoftwareFJError as error:
            # Si hubo encadenamiento mostramos también la causa original
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
            log.error(f"Reserva fallida: {error}{causa}")
            return None
        self.reservas.append(reserva)
        log.info(f"Reserva creada: {reserva}")
        return reserva

    def ejecutar(self, descripcion, accion, *args, **kwargs):
        """Ejecuta cualquier operación de forma segura (confirmar, procesar...)."""
        try:
            resultado = accion(*args, **kwargs)
        except SoftwareFJError as error:
            log.error(f"{descripcion} -> falló: {error}")
            return None
        except Exception as error:  # Cualquier error inesperado
            log.critical(f"{descripcion} -> error inesperado: {error!r}")
            return None
        else:
            log.info(f"{descripcion} -> OK")
            return resultado
        finally:
            # Siempre dejamos constancia de que la operación terminó
            log.info(f"{descripcion} -> operación finalizada")

    def resumen(self):
        """Devuelve un texto con el estado final del sistema."""
        lineas = [f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} "
                  f"| Reservas: {len(self.reservas)}"]
        lineas += [f"  - {r}" for r in self.reservas]
        return "\n".join(lineas)
