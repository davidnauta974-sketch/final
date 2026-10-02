"""Pruebas del reinicio de solicitudes e identificadores."""

import json

import pytest

from src.repositories.json_solicitud_repository import JsonSolicitudRepository
from src.repositories.memory_solicitud_repository import MemorySolicitudRepository
from src.services.soporte_service import SoporteService


@pytest.mark.parametrize("tipo_repositorio", ["memoria", "json"])
def test_reiniciar_borra_pendientes_y_empieza_en_uno(tipo_repositorio, tmp_path):
    repositorio = (
        MemorySolicitudRepository()
        if tipo_repositorio == "memoria"
        else JsonSolicitudRepository(str(tmp_path / "solicitudes.json"))
    )
    servicio = SoporteService(repositorio)
    for nombre in ["Ana", "Luis", "Carlos"]:
        servicio.registrar_solicitud(nombre, "Problema anterior")

    servicio.reiniciar_ids()

    assert servicio.cantidad_pendientes() == 0
    assert servicio.hay_solicitudes_pendientes() is False
    with pytest.raises(IndexError):
        servicio.consultar_siguiente()

    primera = servicio.registrar_solicitud("Nuevo cliente", "Problema nuevo")
    segunda = servicio.registrar_solicitud("Otro cliente", "Otro problema")
    assert primera.id_solicitud == 1
    assert segunda.id_solicitud == 2
    assert servicio.atender_solicitud() is primera
    assert servicio.atender_solicitud() is segunda


@pytest.mark.parametrize("tipo_repositorio", ["memoria", "json"])
def test_reiniciar_con_cola_vacia_reinicia_la_numeracion(tipo_repositorio, tmp_path):
    repositorio = (
        MemorySolicitudRepository()
        if tipo_repositorio == "memoria"
        else JsonSolicitudRepository(str(tmp_path / "solicitudes.json"))
    )
    servicio = SoporteService(repositorio)
    for nombre in ["Ana", "Luis", "Carlos"]:
        servicio.registrar_solicitud(nombre, "Problema")
        servicio.atender_solicitud()

    servicio.reiniciar_ids()
    servicio.reiniciar_ids()

    assert servicio.registrar_solicitud("Nuevo cliente", "Problema").id_solicitud == 1


def test_reinicio_json_persiste_al_reabrir(tmp_path):
    archivo = tmp_path / "solicitudes.json"
    servicio = SoporteService(JsonSolicitudRepository(str(archivo)))
    servicio.registrar_solicitud("Ana", "Problema")
    servicio.registrar_solicitud("Luis", "Otro problema")

    servicio.reiniciar_ids()

    assert json.loads(archivo.read_text(encoding="utf-8")) == []
    reabierto = SoporteService(JsonSolicitudRepository(str(archivo)))
    assert reabierto.cantidad_pendientes() == 0
    assert reabierto.registrar_solicitud("Nuevo cliente", "Problema").id_solicitud == 1


def test_error_al_reiniciar_conserva_archivo_pendientes_y_numeracion(tmp_path, monkeypatch):
    archivo = tmp_path / "solicitudes.json"
    servicio = SoporteService(JsonSolicitudRepository(str(archivo)))
    anteriores = [
        servicio.registrar_solicitud(nombre, "Problema")
        for nombre in ["Ana", "Luis", "Carlos"]
    ]
    contenido_anterior = archivo.read_bytes()

    def reemplazo_fallido(*args):
        raise OSError("No se pudo escribir el archivo")

    with monkeypatch.context() as parche:
        parche.setattr("src.repositories.json_solicitud_repository.os.replace", reemplazo_fallido)
        with pytest.raises(OSError):
            servicio.reiniciar_ids()

    assert archivo.read_bytes() == contenido_anterior
    assert servicio.cantidad_pendientes() == 3
    assert servicio.consultar_siguiente() is anteriores[0]
    nueva = servicio.registrar_solicitud("Nuevo cliente", "Problema")
    assert nueva.id_solicitud == 4
    for solicitud in anteriores + [nueva]:
        assert servicio.atender_solicitud() is solicitud
