"""
cliente.py
Clase Cliente con validaciones estrictas y datos personales encapsulados.
"""

import re  # Expresiones regulares para validar correo y teléfono
from .entidad import Entidad  # Clase abstracta base
from .excepciones import DatoInvalidoError, ParametroFaltanteError  # Errores propios

# Patrón sencillo para validar correos electrónicos
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
# Teléfono colombiano: 10 dígitos que empiezan por 3 (celular) o 60 (fijo)
PATRON_TELEFONO = re.compile(r"^(3\d{9}|60\d{8})$")


class Cliente(Entidad):
    """Cliente de Software FJ."""

    def __init__(self, nombre, documento, correo, telefono):
        # Primero inicializamos la parte común (id y fecha)
        super().__init__()
        # Asignamos usando los setters para que se validen los datos
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- Propiedades con validación (encapsulación) ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre es obligatorio
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        valor = str(valor).strip()
        # Solo letras y espacios, mínimo 3 caracteres
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise DatoInvalidoError("nombre", valor, "Solo letras, mínimo 3 caracteres.")
        self.__nombre = valor.title()

    @property
    def documento(self):
        # Por privacidad solo mostramos los últimos 4 dígitos
        return "****" + self.__documento[-4:]

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        valor = str(valor).strip()
        # Documento numérico de 6 a 10 dígitos
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise DatoInvalidoError("documento", valor, "Debe tener 6 a 10 dígitos.")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor:
            raise ParametroFaltanteError("correo")
        if not PATRON_CORREO.match(str(valor)):
            raise DatoInvalidoError("correo", valor, "Formato de correo incorrecto.")
        self.__correo = str(valor).lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor:
            raise ParametroFaltanteError("telefono")
        valor = str(valor).replace(" ", "")
        if not PATRON_TELEFONO.match(valor):
            raise DatoInvalidoError("telefono", valor, "Debe ser un número colombiano válido.")
        self.__telefono = valor

    # ---------- Métodos obligatorios de Entidad ----------
    def validar(self):
        """Revalida todos los datos (útil si se modifican desde fuera)."""
        # Volver a asignar cada valor fuerza la validación de los setters
        self.nombre = self.__nombre
        self.correo = self.__correo
        self.telefono = self.__telefono
        return True

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} (doc {self.documento}, {self.correo})"
