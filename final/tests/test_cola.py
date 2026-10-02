"""
Pruebas unitarias para la cola FIFO implementada con nodos enlazados.

Cada prueba verifica un comportamiento específico de la cola,
asegurando que las cinco operaciones funcionan correctamente
y que el manejo de la cola vacía es consistente.
"""

import pytest
from src.structures.cola import Cola


# ──────────────────────────────────────────────
# Cola nueva: estado inicial
# ──────────────────────────────────────────────

class TestColaVaciaInicial:
    """Verificar que una cola recién creada está vacía."""

    def test_cola_nueva_esta_vacia(self):
        cola = Cola()
        assert cola.is_empty() is True

    def test_cola_nueva_tiene_tamano_cero(self):
        cola = Cola()
        assert cola.size() == 0


# ──────────────────────────────────────────────
# Agregar elementos (enqueue)
# ──────────────────────────────────────────────

class TestEnqueue:
    """Verificar la operación de agregar elementos."""

    def test_agregar_un_elemento_permite_consultarlo(self):
        cola = Cola()
        cola.enqueue("solicitud_1")
        assert cola.peek() == "solicitud_1"

    def test_agregar_un_elemento_incrementa_tamano(self):
        cola = Cola()
        cola.enqueue("solicitud_1")
        assert cola.size() == 1
        assert cola.is_empty() is False

    def test_agregar_varios_elementos_conserva_orden_fifo(self):
        cola = Cola()
        cola.enqueue("primero")
        cola.enqueue("segundo")
        cola.enqueue("tercero")

        # El primero en entrar debe ser el primero en consultarse
        assert cola.peek() == "primero"
        assert cola.size() == 3


# ──────────────────────────────────────────────
# Retirar elementos (dequeue)
# ──────────────────────────────────────────────

class TestDequeue:
    """Verificar la operación de retirar elementos."""

    def test_retirar_devuelve_el_elemento_correcto(self):
        cola = Cola()
        cola.enqueue("primero")
        cola.enqueue("segundo")

        resultado = cola.dequeue()
        assert resultado == "primero"

    def test_retirar_actualiza_el_tamano(self):
        cola = Cola()
        cola.enqueue("primero")
        cola.enqueue("segundo")

        cola.dequeue()
        assert cola.size() == 1

    def test_retirar_varios_respeta_orden_fifo(self):
        cola = Cola()
        cola.enqueue("A")
        cola.enqueue("B")
        cola.enqueue("C")

        assert cola.dequeue() == "A"
        assert cola.dequeue() == "B"
        assert cola.dequeue() == "C"

    def test_retirar_todos_los_elementos_deja_cola_vacia(self):
        cola = Cola()
        cola.enqueue("unico")

        cola.dequeue()

        assert cola.is_empty() is True
        assert cola.size() == 0

    def test_retirar_ultimo_elemento_actualiza_frente_y_final(self):
        """Al retirar el último elemento, ambas referencias deben ser None."""
        cola = Cola()
        cola.enqueue("elemento")
        cola.dequeue()

        # Verificar que las referencias internas están limpias
        assert cola._frente is None
        assert cola._final is None


# ──────────────────────────────────────────────
# Consultar sin retirar (peek)
# ──────────────────────────────────────────────

class TestPeek:
    """Verificar la operación de consulta sin retiro."""

    def test_peek_no_elimina_el_elemento(self):
        cola = Cola()
        cola.enqueue("solicitud")

        resultado = cola.peek()

        assert resultado == "solicitud"
        assert cola.size() == 1  # El tamaño no cambia

    def test_peek_no_modifica_el_tamano(self):
        cola = Cola()
        cola.enqueue("A")
        cola.enqueue("B")

        cola.peek()
        cola.peek()  # Consultar múltiples veces

        assert cola.size() == 2

    def test_peek_devuelve_siempre_el_frente(self):
        cola = Cola()
        cola.enqueue("primero")
        cola.enqueue("segundo")

        assert cola.peek() == "primero"
        assert cola.peek() == "primero"  # No cambia


# ──────────────────────────────────────────────
# Operaciones en cola vacía
# ──────────────────────────────────────────────

class TestColaVaciaOperaciones:
    """Verificar el comportamiento definido al operar sobre una cola vacía."""

    def test_dequeue_en_cola_vacia_lanza_error(self):
        cola = Cola()
        with pytest.raises(IndexError, match="la cola está vacía"):
            cola.dequeue()

    def test_peek_en_cola_vacia_lanza_error(self):
        cola = Cola()
        with pytest.raises(IndexError, match="la cola está vacía"):
            cola.peek()


# ──────────────────────────────────────────────
# Reutilización después de vaciar
# ──────────────────────────────────────────────

class TestReutilizacionCola:
    """Verificar que la cola funciona correctamente después de vaciarse."""

    def test_agregar_elementos_despues_de_vaciar_la_cola(self):
        cola = Cola()

        # Fase 1: llenar y vaciar
        cola.enqueue("temporal")
        cola.dequeue()
        assert cola.is_empty() is True

        # Fase 2: volver a usar
        cola.enqueue("nuevo_1")
        cola.enqueue("nuevo_2")

        assert cola.is_empty() is False
        assert cola.size() == 2
        assert cola.peek() == "nuevo_1"
        assert cola.dequeue() == "nuevo_1"
        assert cola.dequeue() == "nuevo_2"
        assert cola.is_empty() is True
