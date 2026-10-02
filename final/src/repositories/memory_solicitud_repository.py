"""
Implementación en memoria del Repository de solicitudes.

Utiliza la cola FIFO manual (basada en nodos enlazados) como único
mecanismo de almacenamiento. No mantiene ninguna colección paralela.

Los datos se conservan solamente durante la ejecución del programa;
al cerrar la aplicación, toda la información se pierde.
"""

from src.models.solicitud import Solicitud
from src.repositories.solicitud_repository import SolicitudRepository
from src.structures.cola import Cola


class MemorySolicitudRepository(SolicitudRepository):
    """
    Repositorio de solicitudes almacenado en memoria.

    Delega todas las operaciones de almacenamiento a una instancia
    de la cola FIFO implementada con nodos enlazados.
    """

    def __init__(self):
        """Inicializa el repositorio con una cola vacía."""
        self._cola = Cola()

    def guardar(self, solicitud: Solicitud) -> None:
        """Almacena la solicitud al final de la cola."""
        self._cola.enqueue(solicitud)

    def vaciar(self) -> None:
        """Descarta los nodos de la cola de solicitudes."""
        self._cola = Cola()

    def obtener_siguiente(self) -> Solicitud:
        """Retira y devuelve la solicitud más antigua de la cola."""
        return self._cola.dequeue()

    def consultar_siguiente(self) -> Solicitud:
        """Consulta la solicitud más antigua sin retirarla."""
        return self._cola.peek()

    def esta_vacio(self) -> bool:
        """Indica si la cola de solicitudes está vacía."""
        return self._cola.is_empty()

    def cantidad(self) -> int:
        """Devuelve la cantidad de solicitudes en la cola."""
        return self._cola.size()
