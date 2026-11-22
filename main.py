"""
main.py
Simulación de operaciones completas del sistema Software FJ.
Incluye casos válidos e inválidos para demostrar que el programa sigue
funcionando aunque ocurran errores.
Ejecutar con:  python main.py
"""

from software_fj.sistema import SistemaFJ
from software_fj.servicios import ReservaSala, AlquilerEquipo, Asesoria, Servicio
from software_fj.registro import log, ARCHIVO_LOG


def titulo(n, texto):
    """Imprime un encabezado para cada operación."""
    print(f"\n=== Operación {n}: {texto} ===")


def main():
    sistema = SistemaFJ()  # Creamos el gestor (listas vacías)
    log.info("===== Inicio de la simulación Software FJ =====")

    # 1. Cliente válido
    titulo(1, "Registrar cliente válido")
    ana = sistema.registrar_cliente(nombre="ana gómez", documento="1112223334",
                                    correo="Ana@correo.com", telefono="3001234567")

    # 2. Cliente con correo inválido
    titulo(2, "Registrar cliente con correo inválido")
    sistema.registrar_cliente(nombre="Luis Pérez", documento="98765432",
                              correo="luis.correo.com", telefono="3109876543")

    # 3. Cliente con parámetro faltante
    titulo(3, "Registrar cliente sin nombre")
    sistema.registrar_cliente(nombre="", documento="12345678",
                              correo="x@y.com", telefono="3201112233")

    # 4. Segundo cliente válido
    titulo(4, "Registrar segundo cliente válido")
    carlos = sistema.registrar_cliente(nombre="Carlos Ruiz", documento="1234567",
                                       correo="carlos@fj.co", telefono="6023334455")

    # 5. Servicios válidos (uno de cada tipo)
    titulo(5, "Crear servicios válidos")
    sala = sistema.agregar_servicio(ReservaSala, "Sala Pacífico", 50000, capacidad=30)
    equipo = sistema.agregar_servicio(AlquilerEquipo, "Portátil", 8000, cantidad=3)
    asesoria = sistema.agregar_servicio(Asesoria, "Python", 120000, nivel="experto")

    # 6. Servicios inválidos
    titulo(6, "Crear servicios inválidos")
    sistema.agregar_servicio(ReservaSala, "Sala Rota", -100, capacidad=10)   # tarifa negativa
    sistema.agregar_servicio(Asesoria, "Excel", 60000, nivel="maestro")      # nivel inexistente
    sistema.agregar_servicio(Servicio, "Genérico", 1000)                    # clase abstracta

    # 7. Reserva exitosa completa: crear -> confirmar -> procesar con IVA
    titulo(7, "Reserva exitosa de sala con IVA")
    r1 = sistema.crear_reserva(ana, sala, 3)
    sistema.ejecutar("Confirmar r1", r1.confirmar)
    sistema.ejecutar("Procesar r1", r1.procesar, impuesto=True)

    # 8. Reserva con duración inválida (encadenamiento de excepciones)
    titulo(8, "Reserva de equipo por 1 hora (mínimo 2)")
    sistema.crear_reserva(carlos, equipo, 1)

    # 9. Servicio no disponible
    titulo(9, "Reservar servicio no disponible")
    equipo.cambiar_disponibilidad(False)
    sistema.crear_reserva(carlos, equipo, 5)
    equipo.cambiar_disponibilidad(True)

    # 10. Procesar sin confirmar (operación no permitida)
    titulo(10, "Procesar reserva sin confirmar")
    r2 = sistema.crear_reserva(carlos, asesoria, 2)
    sistema.ejecutar("Procesar r2 sin confirmar", r2.procesar)

    # 11. Descuento inválido al procesar (try/except/else/finally en procesar)
    titulo(11, "Procesar con descuento inválido y luego válido")
    sistema.ejecutar("Confirmar r2", r2.confirmar)
    sistema.ejecutar("Procesar r2 con 80% de descuento", r2.procesar, True, 0.8)
    sistema.ejecutar("Procesar r2 con 10% de descuento", r2.procesar, True, 0.1)

    # 12. Cancelaciones válida e inválida
    titulo(12, "Cancelar reservas")
    r3 = sistema.crear_reserva(ana, equipo, 24)
    sistema.ejecutar("Cancelar r3", r3.cancelar)
    sistema.ejecutar("Cancelar r3 otra vez", r3.cancelar)
    sistema.ejecutar("Cancelar r1 ya procesada", r1.cancelar)

    # 13. Variantes del método sobrecargado calcular_costo
    titulo(13, "Variantes de calcular_costo (sobrecarga)")
    print("Solo base:          ", sala.calcular_costo(2))
    print("Con IVA:            ", sala.calcular_costo(2, impuesto=True))
    print("Con descuento 15 %: ", sala.calcular_costo(2, descuento=0.15))
    print("Con IVA y descuento:", sala.calcular_costo(2, True, 0.15))

    # 14. Error inesperado (no previsto) también se controla
    titulo(14, "Error inesperado controlado")
    sistema.ejecutar("División entre cero", lambda: 1 / 0)

    print("\n=== Resumen final ===")
    print(sistema.resumen())
    log.info("===== Fin de la simulación: el sistema siguió activo =====")
    print(f"\nLog guardado en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
