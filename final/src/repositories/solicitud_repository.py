"""
Contrato (interfaz) del Repository de solicitudes de soporte.

Define las operaciones que cualquier implementación del repositorio
debe ofrecer, separando la lógica de negocio del mecanismo de
almacenamiento concreto.

En Python se utiliza una clase base abstracta (ABC) para definir
este contrato. Cualquier clase que herede de SolicitudRepository
está obligada a implementar todos los métodos abstractos.
"""

from abc import ABC, abstractmethod
from src.models.solicitud import Solicitud


class SolicitudRepository(ABC):
    """Contrato para el repositorio de solicitudes de soporte."""

    @abstractmethod
    def vaciar(self) -> None:
        """Elimina todas las solicitudes pendientes del almacenamiento."""
        pass

    @abstractmethod
    def guardar(self, solicitud: Solicitud) -> None:
        """
        Almacena una solicitud en el repositorio.

        Args:
            solicitud: La solicitud de soporte a almacenar.
        """
        pass

    @abstractmethod
    def obtener_siguiente(self) -> Solicitud:
        """
        Retira y devuelve la solicitud más antigua (primera en llegar).

        Returns:
            La solicitud más antigua del repositorio.

        Raises:
            IndexError: Si no hay solicitudes almacenadas.
        """
        pass

    @abstractmethod
    def consultar_siguiente(self) -> Solicitud:
        """
        Consulta la solicitud más antigua sin retirarla.

        Returns:
            La solicitud más antigua del repositorio.

        Raises:
            IndexError: Si no hay solicitudes almacenadas.
        """
        pass

    @abstractmethod
    def esta_vacio(self) -> bool:
        """
        Indica si el repositorio no contiene solicitudes.

        Returns:
            True si no hay solicitudes, False en caso contrario.
        """
        pass

    @abstractmethod
    def cantidad(self) -> int:
        """
        Devuelve la cantidad de solicitudes almacenadas.

        Returns:
            Número de solicitudes en el repositorio.
        """
        pass
