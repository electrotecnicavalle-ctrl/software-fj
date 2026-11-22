"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y Asesoria.
Aquí se aplican herencia, polimorfismo y "sobrecarga" de métodos.
"""

from abc import abstractmethod  # Para declarar métodos abstractos
from .entidad import Entidad  # Clase base abstracta
from .excepciones import (  # Excepciones personalizadas usadas aquí
    DatoInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)

IVA = 0.19  # Impuesto al valor agregado en Colombia


class Servicio(Entidad):
    """Servicio genérico. No se puede instanciar directamente."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        # Validamos que el nombre exista
        if not nombre:
            raise ParametroFaltanteError("nombre del servicio")
        # La tarifa debe ser un número positivo
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatoInvalidoError("tarifa_hora", tarifa_hora, "Debe ser un número mayor que 0.")
        self._nombre = nombre  # Atributo protegido (accesible a las subclases)
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    # ---------- Métodos que cada subclase debe sobrescribir ----------
    @abstractmethod
    def costo_base(self, horas):
        """Costo sin impuestos ni descuentos; depende del tipo de servicio."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida la duración según las reglas propias del servicio."""

    def validar(self):
        # Un servicio es válido si su tarifa es positiva
        return self._tarifa_hora > 0

    # ---------- "Sobrecarga" de calcular_costo ----------
    # Python no permite varios métodos con el mismo nombre, así que la
    # sobrecarga se simula con parámetros opcionales: el mismo método
    # se comporta distinto según los argumentos que reciba.
    def calcular_costo(self, horas, impuesto=None, descuento=None):
        """
        Variantes:
          calcular_costo(horas)                       -> costo base
          calcular_costo(horas, impuesto=True)        -> base + IVA
          calcular_costo(horas, descuento=0.1)        -> base - 10 %
          calcular_costo(horas, True, 0.1)            -> con descuento e IVA
        """
        self.validar_parametros(horas)  # Primero validamos la duración
        total = self.costo_base(horas)  # Polimorfismo: cada subclase calcula distinto
        if descuento is not None:
            # El descuento debe estar entre 0 % y 50 %
            if not 0 <= descuento <= 0.5:
                raise DatoInvalidoError("descuento", descuento, "Debe estar entre 0 y 0.5.")
            total *= (1 - descuento)
        if impuesto:
            # Si impuesto es True usamos el IVA; si es número, esa tasa
            tasa = IVA if impuesto is True else float(impuesto)
            total *= (1 + tasa)
        # Verificación de consistencia: un costo nunca puede ser negativo o cero
        if total <= 0:
            raise CalculoInconsistenteError(f"el total calculado es {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("capacidad", capacidad, "Debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, horas):
        # Las salas se reservan de 1 a 12 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise DatoInvalidoError("horas", horas, "Una sala se reserva entre 1 y 12 horas.")

    def costo_base(self, horas):
        # Salas grandes (más de 20 personas) cuestan 20 % más
        recargo = 1.2 if self.capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self):
        return f"Sala '{self.nombre}' para {self.capacidad} personas - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, video beam, etc.)."""

    def __init__(self, nombre, tarifa_hora, cantidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("cantidad", cantidad, "Debe ser un entero positivo.")
        self.cantidad = cantidad

    def validar_parametros(self, horas):
        # Los equipos se alquilan por mínimo 2 horas y máximo 72 (3 días)
        if not isinstance(horas, (int, float)) or not 2 <= horas <= 72:
            raise DatoInvalidoError("horas", horas, "Un equipo se alquila entre 2 y 72 horas.")

    def costo_base(self, horas):
        # Costo por unidad multiplicado por la cantidad de equipos
        return self._tarifa_hora * horas * self.cantidad

    def describir(self):
        return f"Equipo '{self.nombre}' x{self.cantidad} - ${self._tarifa_hora:,.0f}/h c/u"


class Asesoria(Servicio):
    """Asesoría especializada con un consultor."""

    NIVELES = {"basico": 1.0, "avanzado": 1.5, "experto": 2.0}  # Multiplicadores

    def __init__(self, nombre, tarifa_hora, nivel="basico", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel, f"Opciones: {list(self.NIVELES)}.")
        self.nivel = nivel

    def validar_parametros(self, horas):
        # Asesorías de 0.5 a 8 horas
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 8:
            raise DatoInvalidoError("horas", horas, "Una asesoría dura entre 0.5 y 8 horas.")

    def costo_base(self, horas):
        # El nivel del asesor multiplica la tarifa
        return self._tarifa_hora * horas * self.NIVELES[self.nivel]

    def describir(self):
        return f"Asesoría '{self.nombre}' nivel {self.nivel} - ${self._tarifa_hora:,.0f}/h"
