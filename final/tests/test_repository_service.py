"""
Pruebas unitarias para el Repository en memoria y el servicio de soporte.

Verifican que el repositorio delega correctamente a la cola,
que el servicio genera identificadores únicos, valida entradas
y respeta el orden FIFO de atención.
"""

import pytest
from src.models.solicitud import Solicitud
from src.repositories.memory_solicitud_repository import MemorySolicitudRepository
from src.services.soporte_service import SoporteService


# ──────────────────────────────────────────────
# Pruebas del Repository en memoria
# ──────────────────────────────────────────────

class TestMemorySolicitudRepository:
    """Verificar las operaciones del repositorio en memoria."""

    def test_repositorio_nuevo_esta_vacio(self):
        repo = MemorySolicitudRepository()
        assert repo.esta_vacio() is True
        assert repo.cantidad() == 0

    def test_guardar_y_consultar_solicitud(self):
        repo = MemorySolicitudRepository()
        solicitud = Solicitud(1, "Carlos", "Mi PC no enciende")

        repo.guardar(solicitud)

        resultado = repo.consultar_siguiente()
        assert resultado.id_solicitud == 1
        assert resultado.nombre_cliente == "Carlos"

    def test_guardar_y_recuperar_solicitud(self):
        repo = MemorySolicitudRepository()
        solicitud = Solicitud(1, "Ana", "Error de red")

        repo.guardar(solicitud)
        resultado = repo.obtener_siguiente()

        assert resultado.id_solicitud == 1
        assert resultado.nombre_cliente == "Ana"
        assert repo.esta_vacio() is True

    def test_orden_fifo_en_repositorio(self):
        repo = MemorySolicitudRepository()
        repo.guardar(Solicitud(1, "Primero", "Problema 1"))
        repo.guardar(Solicitud(2, "Segundo", "Problema 2"))
        repo.guardar(Solicitud(3, "Tercero", "Problema 3"))

        assert repo.obtener_siguiente().nombre_cliente == "Primero"
        assert repo.obtener_siguiente().nombre_cliente == "Segundo"
        assert repo.obtener_siguiente().nombre_cliente == "Tercero"

    def test_consultar_siguiente_no_lo_elimina(self):
        repo = MemorySolicitudRepository()
        repo.guardar(Solicitud(1, "Luis", "Pantalla azul"))

        repo.consultar_siguiente()
        repo.consultar_siguiente()

        assert repo.cantidad() == 1  # Sigue ahí

    def test_cantidad_se_actualiza_correctamente(self):
        repo = MemorySolicitudRepository()
        assert repo.cantidad() == 0

        repo.guardar(Solicitud(1, "A", "P1"))
        assert repo.cantidad() == 1

        repo.guardar(Solicitud(2, "B", "P2"))
        assert repo.cantidad() == 2

        repo.obtener_siguiente()
        assert repo.cantidad() == 1

    def test_obtener_de_repositorio_vacio_lanza_error(self):
        repo = MemorySolicitudRepository()
        with pytest.raises(IndexError):
            repo.obtener_siguiente()

    def test_consultar_de_repositorio_vacio_lanza_error(self):
        repo = MemorySolicitudRepository()
        with pytest.raises(IndexError):
            repo.consultar_siguiente()


# ──────────────────────────────────────────────
# Pruebas del servicio de soporte
# ──────────────────────────────────────────────

class TestSoporteService:
    """Verificar la lógica de negocio del servicio de soporte."""

    def _crear_servicio(self) -> SoporteService:
        """Crea un servicio con un repositorio nuevo para cada prueba."""
        repo = MemorySolicitudRepository()
        return SoporteService(repo)

    def test_registrar_solicitud_devuelve_solicitud_valida(self):
        servicio = self._crear_servicio()
        solicitud = servicio.registrar_solicitud("María", "No tengo internet")

        assert solicitud.nombre_cliente == "María"
        assert solicitud.descripcion == "No tengo internet"
        assert solicitud.id_solicitud == 1

    def test_identificadores_unicos_secuenciales(self):
        servicio = self._crear_servicio()

        s1 = servicio.registrar_solicitud("A", "Problema 1")
        s2 = servicio.registrar_solicitud("B", "Problema 2")
        s3 = servicio.registrar_solicitud("C", "Problema 3")

        assert s1.id_solicitud == 1
        assert s2.id_solicitud == 2
        assert s3.id_solicitud == 3

    def test_atender_solicitudes_en_orden_de_llegada(self):
        servicio = self._crear_servicio()
        servicio.registrar_solicitud("Primero", "P1")
        servicio.registrar_solicitud("Segundo", "P2")

        atendida = servicio.atender_solicitud()
        assert atendida.nombre_cliente == "Primero"

        atendida = servicio.atender_solicitud()
        assert atendida.nombre_cliente == "Segundo"

    def test_consultar_siguiente_sin_eliminarla(self):
        servicio = self._crear_servicio()
        servicio.registrar_solicitud("Pedro", "Teclado roto")

        consultada = servicio.consultar_siguiente()
        assert consultada.nombre_cliente == "Pedro"

        # Sigue disponible para atender
        assert servicio.cantidad_pendientes() == 1

    def test_hay_solicitudes_pendientes_inicialmente_false(self):
        servicio = self._crear_servicio()
        assert servicio.hay_solicitudes_pendientes() is False

    def test_hay_solicitudes_pendientes_despues_de_registrar(self):
        servicio = self._crear_servicio()
        servicio.registrar_solicitud("Laura", "Monitor apagado")
        assert servicio.hay_solicitudes_pendientes() is True

    def test_cantidad_pendientes(self):
        servicio = self._crear_servicio()
        assert servicio.cantidad_pendientes() == 0

        servicio.registrar_solicitud("A", "P1")
        servicio.registrar_solicitud("B", "P2")
        assert servicio.cantidad_pendientes() == 2

        servicio.atender_solicitud()
        assert servicio.cantidad_pendientes() == 1

    def test_atender_sin_solicitudes_lanza_error(self):
        servicio = self._crear_servicio()
        with pytest.raises(IndexError):
            servicio.atender_solicitud()

    def test_consultar_sin_solicitudes_lanza_error(self):
        servicio = self._crear_servicio()
        with pytest.raises(IndexError):
            servicio.consultar_siguiente()

    # ── Validación de datos obligatorios ──

    def test_rechazar_nombre_vacio(self):
        servicio = self._crear_servicio()
        with pytest.raises(ValueError, match="nombre del cliente"):
            servicio.registrar_solicitud("", "Descripción válida")

    def test_rechazar_nombre_solo_espacios(self):
        servicio = self._crear_servicio()
        with pytest.raises(ValueError, match="nombre del cliente"):
            servicio.registrar_solicitud("   ", "Descripción válida")

    def test_rechazar_descripcion_vacia(self):
        servicio = self._crear_servicio()
        with pytest.raises(ValueError, match="descripción del problema"):
            servicio.registrar_solicitud("Cliente", "")

    def test_rechazar_descripcion_solo_espacios(self):
        servicio = self._crear_servicio()
        with pytest.raises(ValueError, match="descripción del problema"):
            servicio.registrar_solicitud("Cliente", "   ")

    def test_nombre_se_limpia_de_espacios_extra(self):
        servicio = self._crear_servicio()
        solicitud = servicio.registrar_solicitud("  Ana  ", "Problema")
        assert solicitud.nombre_cliente == "Ana"
