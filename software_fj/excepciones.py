"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de una excepción base para poder capturarlas de forma general.
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Guardamos un código para identificar el tipo de error en el log
        self.codigo = codigo
        # Llamamos al constructor de Exception con el mensaje legible
        super().__init__(f"[{codigo}] {mensaje}")


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las validaciones (nombre, correo, etc.)."""

    def __init__(self, campo, valor, detalle=""):
        # Guardamos el campo y el valor que fallaron para facilitar la depuración
        self.campo = campo
        self.valor = valor
        super().__init__(f"Dato inválido en '{campo}': {valor!r}. {detalle}", "FJ-100")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, parametro):
        self.parametro = parametro
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'.", "FJ-110")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible.", "FJ-200")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no se puede crear por datos incorrectos."""

    def __init__(self, detalle):
        super().__init__(f"Reserva inválida: {detalle}", "FJ-300")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no válida para el estado actual."""

    def __init__(self, operacion, estado):
        super().__init__(
            f"No se puede '{operacion}' una reserva en estado '{estado}'.", "FJ-310"
        )


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos da un resultado incoherente."""

    def __init__(self, detalle):
        super().__init__(f"Cálculo inconsistente: {detalle}", "FJ-400")
