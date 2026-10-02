"""
Modelo de datos para una solicitud de soporte técnico.

Cada solicitud contiene un identificador único, el nombre del cliente
y una descripción del problema reportado.
"""


class Solicitud:
    """Representa una solicitud de soporte técnico."""

    def __init__(self, id_solicitud: int, nombre_cliente: str, descripcion: str):
        """
        Crea una nueva solicitud de soporte.

        Args:
            id_solicitud: Identificador único de la solicitud.
            nombre_cliente: Nombre del cliente que realiza la solicitud.
            descripcion: Descripción del problema reportado.
        """
        self.id_solicitud = id_solicitud
        self.nombre_cliente = nombre_cliente
        self.descripcion = descripcion

    def __str__(self) -> str:
        return (
            f"[Solicitud #{self.id_solicitud}] "
            f"Cliente: {self.nombre_cliente} | "
            f"Problema: {self.descripcion}"
        )

    def __repr__(self) -> str:
        return (
            f"Solicitud(id_solicitud={self.id_solicitud}, "
            f"nombre_cliente='{self.nombre_cliente}', "
            f"descripcion='{self.descripcion}')"
        )

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Solicitud):
            return False
        return self.id_solicitud == otro.id_solicitud
