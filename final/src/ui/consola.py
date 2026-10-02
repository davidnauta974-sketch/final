"""
Interfaz de consola para el sistema de gestión de turnos.

Presenta un menú interactivo al usuario y delega todas las
operaciones al servicio de soporte. No accede directamente
a la cola ni a los nodos.
"""

from src.services.soporte_service import SoporteService


def mostrar_menu() -> None:
    """Muestra las opciones disponibles en el menú principal."""
    print("\n" + "=" * 55)
    print("   SISTEMA DE GESTIÓN DE TURNOS - SOPORTE TÉCNICO")
    print("=" * 55)
    print("  1. Registrar una solicitud")
    print("  2. Atender la solicitud más antigua")
    print("  3. Consultar la siguiente solicitud")
    print("  4. Comprobar si hay solicitudes pendientes")
    print("  5. Consultar cantidad de solicitudes pendientes")
    print("  6. Salir")
    print("-" * 55)


def ejecutar(servicio: SoporteService) -> None:
    """
    Ejecuta el ciclo principal del menú de consola.

    Args:
        servicio: Instancia del servicio de soporte técnico.
    """
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            _registrar_solicitud(servicio)
        elif opcion == "2":
            _atender_solicitud(servicio)
        elif opcion == "3":
            _consultar_siguiente(servicio)
        elif opcion == "4":
            _comprobar_pendientes(servicio)
        elif opcion == "5":
            _cantidad_pendientes(servicio)
        elif opcion == "6":
            print("\n¡Hasta luego! El sistema se ha cerrado.")
            break
        else:
            print("\n⚠ Opción no válida. Ingrese un número del 1 al 6.")


def _registrar_solicitud(servicio: SoporteService) -> None:
    """Solicita datos al usuario y registra una nueva solicitud."""
    print("\n--- Registrar nueva solicitud ---")
    nombre = input("Nombre del cliente: ").strip()
    descripcion = input("Descripción del problema: ").strip()

    try:
        solicitud = servicio.registrar_solicitud(nombre, descripcion)
        print(f"\n✔ Solicitud registrada exitosamente:")
        print(f"  {solicitud}")
    except ValueError as error:
        print(f"\n⚠ Error: {error}")


def _atender_solicitud(servicio: SoporteService) -> None:
    """Atiende y retira la solicitud más antigua."""
    print("\n--- Atender solicitud ---")
    try:
        solicitud = servicio.atender_solicitud()
        print(f"✔ Solicitud atendida:")
        print(f"  {solicitud}")
    except IndexError:
        print("ℹ No hay solicitudes pendientes para atender.")


def _consultar_siguiente(servicio: SoporteService) -> None:
    """Muestra la siguiente solicitud sin retirarla."""
    print("\n--- Siguiente solicitud en espera ---")
    try:
        solicitud = servicio.consultar_siguiente()
        print(f"  {solicitud}")
    except IndexError:
        print("ℹ No hay solicitudes pendientes.")


def _comprobar_pendientes(servicio: SoporteService) -> None:
    """Informa si existen solicitudes pendientes."""
    if servicio.hay_solicitudes_pendientes():
        print("\n✔ Sí, hay solicitudes pendientes por atender.")
    else:
        print("\nℹ No hay solicitudes pendientes.")


def _cantidad_pendientes(servicio: SoporteService) -> None:
    """Muestra la cantidad de solicitudes en espera."""
    cantidad = servicio.cantidad_pendientes()
    if cantidad == 0:
        print("\nℹ No hay solicitudes pendientes.")
    elif cantidad == 1:
        print(f"\n📋 Hay 1 solicitud pendiente.")
    else:
        print(f"\n📋 Hay {cantidad} solicitudes pendientes.")
