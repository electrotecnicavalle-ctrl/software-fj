"""
entidad.py
Clase abstracta que representa cualquier entidad general del sistema
(clientes, servicios y reservas heredan de ella).
"""

from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas
from datetime import datetime  # Para guardar la fecha de creación
import itertools  # Para generar identificadores consecutivos

# Contador global que asigna un id único a cada entidad creada
_contador_ids = itertools.count(1)


class Entidad(ABC):
    """Entidad general: tiene id, fecha de creación y debe saber describirse."""

    def __init__(self):
        # Id único y privado (encapsulado con doble guion bajo)
        self.__id = next(_contador_ids)
        # Fecha y hora en que se creó la entidad
        self.__creado = datetime.now()

    @property
    def id(self):
        """Id de solo lectura."""
        return self.__id

    @property
    def creado(self):
        """Fecha de creación de solo lectura."""
        return self.__creado

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe devolver una descripción en texto."""

    @abstractmethod
    def validar(self):
        """Cada entidad concreta debe validar sus propios datos."""

    def __str__(self):
        # Al imprimir cualquier entidad se muestra su descripción
        return self.describir()
