import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from src.models.solicitud import Solicitud
from src.repositories.solicitud_repository import SolicitudRepository
from src.structures.cola import Cola


class JsonSolicitudRepository(SolicitudRepository):
    """Repositorio que persiste solicitudes en un archivo JSON.

    Utiliza la misma interfaz que ``MemorySolicitudRepository`` pero guarda y
    carga los datos en ``filepath``. Si el archivo no existe se crea al primer
    ``guardar``.
    """

    def __init__(self, filepath: str = "datos_solicitudes.json") -> None:
        self.filepath = Path(filepath)
        self._cola: Cola = Cola()
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        """Carga las solicitudes desde ``self.filepath`` si el archivo existe.

        Cada entrada del JSON debe contener los campos ``id_solicitud``,
        ``nombre_cliente`` y ``descripcion``.
        """
        if self.filepath.exists():
            try:
                with self.filepath.open("r", encoding="utf-8") as f:
                    datos: List[dict] = json.load(f)
                for item in datos:
                    solicitud = Solicitud(
                        id_solicitud=item["id_solicitud"],
                        nombre_cliente=item["nombre_cliente"],
                        descripcion=item["descripcion"],
                    )
                    self._cola.enqueue(solicitud)
            except Exception as e:
                print(f"Error al cargar datos JSON: {e}")

    def _guardar_datos(self) -> None:
        """Serializa la cola completa a ``self.filepath``.

        Se recorre la estructura de nodos manualmente para evitar depender de
        mecanismos internos de la cola.
        """
        datos: List[dict] = []
        actual = self._cola._frente
        while actual is not None:
            solicitud: Solicitud = actual.dato
            datos.append(
                {
                    "id_solicitud": solicitud.id_solicitud,
                    "nombre_cliente": solicitud.nombre_cliente,
                    "descripcion": solicitud.descripcion,
                }
            )
            actual = actual.siguiente
        try:
            with self.filepath.open("w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar datos JSON: {e}")

    # Implementación de la interfaz abstracta
    def vaciar(self) -> None:
        """Guarda una cola vacía antes de descartar los pendientes en memoria.

        Si el archivo no se puede escribir, el error llega a la interfaz y
        se conservan los pendientes y la numeración de la sesión.
        """
        temporal = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.filepath.parent, delete=False
            ) as archivo:
                temporal = Path(archivo.name)
                json.dump([], archivo)
            os.replace(temporal, self.filepath)
        finally:
            if temporal is not None and temporal.exists():
                temporal.unlink()
        self._cola = Cola()

    def guardar(self, solicitud: Solicitud) -> None:
        self._cola.enqueue(solicitud)
        self._guardar_datos()

    def obtener_siguiente(self) -> Solicitud:
        solicitud = self._cola.dequeue()
        self._guardar_datos()
        return solicitud

    def consultar_siguiente(self) -> Solicitud:
        return self._cola.peek()

    def esta_vacio(self) -> bool:
        return self._cola.is_empty()

    def cantidad(self) -> int:
        return self._cola.size()

    def obtener_max_id(self) -> int:
        """Devuelve el mayor identificador presente en la cola.

        Es útil para que el ``SoporteService`` continúe la numeración después de
        cargar datos persistidos.
        """
        max_id = 0
        actual = self._cola._frente
        while actual is not None:
            if actual.dato.id_solicitud > max_id:
                max_id = actual.dato.id_solicitud
            actual = actual.siguiente
        return max_id
