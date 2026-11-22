# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso **Programación (213023)** – UNAD – Fase 4, componente práctico.

Aplicación en Python orientada a objetos, **sin base de datos**, que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías) y reservas, con manejo avanzado de excepciones.
Toda la información vive en listas internas; el único archivo que se escribe es el log.

## Ejecución

```bash
python main.py
```

Requiere Python 3.10 o superior. No usa librerías externas.
Los eventos y errores quedan en `logs/software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `software_fj/entidad.py` | Clase abstracta `Entidad` (id, fecha, `describir`, `validar`) |
| `software_fj/cliente.py` | `Cliente` con datos encapsulados y validaciones (nombre, documento, correo, teléfono) |
| `software_fj/servicios.py` | Clase abstracta `Servicio` y subclases `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `software_fj/reserva.py` | `Reserva` con estados y métodos `confirmar`, `cancelar`, `procesar` |
| `software_fj/sistema.py` | `SistemaFJ`: listas internas y ejecución segura de operaciones |
| `software_fj/excepciones.py` | Excepciones personalizadas (`DatoInvalidoError`, `ServicioNoDisponibleError`, etc.) |
| `software_fj/registro.py` | Configuración del archivo de logs |
| `main.py` | Simulación de 14 operaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `costo_base`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados (`__documento`, `__estado`…) con propiedades y setters que validan.
- **Sobrecarga:** `calcular_costo(horas, impuesto=None, descuento=None)` tiene varias variantes según los argumentos.
- **Excepciones:** jerarquía propia, `try/except`, `try/except/else`, `try/except/finally`
  y encadenamiento con `raise ... from ...`.
