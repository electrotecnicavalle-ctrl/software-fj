"""
reserva.py
Clase Reserva: une cliente, servicio, duración y estado.
Implementa confirmar, cancelar y procesar con manejo de excepciones.
"""

from .entidad import Entidad
from .cliente import Cliente
from .servicios import Servicio
from .registro import log
from .excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    SoftwareFJError,
)


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE, CONFIRMADA, PROCESADA, CANCELADA = (
        "pendiente", "confirmada", "procesada", "cancelada")

    def __init__(self, cliente, servicio, horas):
        super().__init__()
        # Validamos los tipos para evitar reservas mal formadas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("el cliente no es válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("el servicio no es válido")
        # No se puede reservar un servicio desactivado
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre)
        try:
            # Validamos la duración con las reglas del servicio
            servicio.validar_parametros(horas)
        except SoftwareFJError as error:
            # Encadenamiento: la causa original queda guardada en __cause__
            raise ReservaInvalidaError(f"duración rechazada ({horas} h)") from error
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = Reserva.PENDIENTE  # Toda reserva inicia pendiente
        self.__total = None  # Se calcula al procesar

    @property
    def estado(self):
        return self.__estado

    @property
    def total(self):
        return self.__total

    def validar(self):
        return self.__estado in (self.PENDIENTE, self.CONFIRMADA, self.PROCESADA, self.CANCELADA)

    def confirmar(self):
        """Pasa de pendiente a confirmada."""
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self.__estado)
        self.__estado = Reserva.CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada."""
        if self.__estado in (Reserva.PROCESADA, Reserva.CANCELADA):
            raise OperacionNoPermitidaError("cancelar", self.__estado)
        self.__estado = Reserva.CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")

    def procesar(self, impuesto=True, descuento=None):
        """Calcula el total y deja la reserva como procesada."""
        if self.__estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError("procesar", self.__estado)
        try:
            # Intentamos calcular el costo (puede fallar por descuento inválido, etc.)
            total = self.__servicio.calcular_costo(self.__horas, impuesto, descuento)
        except SoftwareFJError:
            # Registramos y re-lanzamos para que quien llame decida qué hacer
            log.error(f"Reserva #{self.id}: error al calcular el costo.")
            raise
        else:
            # Solo si no hubo error: guardamos el total y cambiamos estado
            self.__total = total
            self.__estado = Reserva.PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            # Se ejecuta siempre, haya error o no
            log.info(f"Reserva #{self.id}: fin del intento de procesamiento.")

    def describir(self):
        total = f"${self.__total:,.2f}" if self.__total else "sin calcular"
        return (f"Reserva #{self.id}: {self.__cliente.nombre} -> {self.__servicio.nombre} "
                f"({self.__horas} h) [{self.__estado}] total {total}")
