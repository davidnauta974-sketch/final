"""
Servicio de gestión de turnos de soporte técnico.

Contiene la lógica de negocio: generar identificadores únicos,
validar datos de entrada y coordinar las operaciones sobre el
repositorio de solicitudes.

Recibe el repositorio mediante inyección de dependencias en el
constructor, lo que permite cambiar la implementación de
almacenamiento sin modificar este servicio.
"""

from src.models.solicitud import Solicitud
from src.repositories.solicitud_repository import SolicitudRepository


class SoporteService:
    """Servicio que administra los turnos de soporte técnico."""

    def __init__(self, repositorio: SolicitudRepository):
        """
        Inicializa el servicio con un repositorio inyectado.

        Args:
            repositorio: Implementación del repositorio de solicitudes.
        """
        self._repositorio = repositorio
        self._contador_id = 0  # Generador de identificadores secuenciales
        
        # Si el repositorio tiene persistencia y puede darnos el max_id, lo usamos
        if hasattr(self._repositorio, "obtener_max_id"):
            self._contador_id = self._repositorio.obtener_max_id()

    def registrar_solicitud(self, nombre_cliente: str, descripcion: str) -> Solicitud:
        """
        Registra una nueva solicitud de soporte.

        Valida que el nombre y la descripción no estén vacíos,
        genera un identificador único y almacena la solicitud
        en el repositorio.

        Args:
            nombre_cliente: Nombre del cliente.
            descripcion: Descripción del problema.

        Returns:
            La solicitud creada y almacenada.

        Raises:
            ValueError: Si el nombre o la descripción están vacíos.
        """
        if not nombre_cliente or not nombre_cliente.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")

        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción del problema no puede estar vacía.")

        self._contador_id += 1
        solicitud = Solicitud(
            id_solicitud=self._contador_id,
            nombre_cliente=nombre_cliente.strip(),
            descripcion=descripcion.strip(),
        )
        self._repositorio.guardar(solicitud)
        return solicitud

    def atender_solicitud(self) -> Solicitud:
        """
        Atiende y retira la solicitud más antigua.

        Returns:
            La solicitud atendida.

        Raises:
            IndexError: Si no hay solicitudes pendientes.
        """
        return self._repositorio.obtener_siguiente()

    def reiniciar_ids(self) -> None:
        """Borra los pendientes y hace que la próxima solicitud tenga ID 1."""
        self._repositorio.vaciar()
        self._contador_id = 0

    def consultar_siguiente(self) -> Solicitud:
        """
        Consulta la próxima solicitud sin retirarla.

        Returns:
            La solicitud que será atendida a continuación.

        Raises:
            IndexError: Si no hay solicitudes pendientes.
        """
        return self._repositorio.consultar_siguiente()

    def hay_solicitudes_pendientes(self) -> bool:
        """
        Indica si existen solicitudes por atender.

        Returns:
            True si hay solicitudes pendientes, False si no.
        """
        return not self._repositorio.esta_vacio()

    def cantidad_pendientes(self) -> int:
        """
        Devuelve el número de solicitudes en espera.

        Returns:
            Cantidad de solicitudes pendientes.
        """
        return self._repositorio.cantidad()
